# -*- coding: utf-8 -*-
"""
Module to prepare the training datasets.
"""

from __future__ import print_function
import logging
import os
import shutil
import math
import datetime
from pathlib import Path
import pprint
from typing import List, Optional, Tuple

from geofileops import geofile
import pandas as pd
import geopandas as gpd
import numpy as np
import owslib
import owslib.wms
from PIL import Image
import rasterio as rio
import rasterio.features as rio_features
import rasterio.profiles as rio_profiles
import shapely.geometry as sh_geom

from orthoseg.util import ows_util

#-------------------------------------------------------------
# First define/init some general variables/constants
#-------------------------------------------------------------
# Get a logger...
logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

#-------------------------------------------------------------
# The real work
#-------------------------------------------------------------

class LabelInfo:
    def __init__(self,
            locations_path: Path,
            polygons_path: Path,
            image_layer: str):
        self.locations_path = locations_path
        self.polygons_path = polygons_path
        self.image_layer = image_layer
    def __repr__(self):
       return f"LabelInfo with image_layer: {self.image_layer}, locations_path: {self.locations_path}, polygons_path: {self.polygons_path}"

def prepare_traindatasets(
        label_infos: List[LabelInfo],
        classes: dict,
        image_layers: dict,
        training_dir: Path,
        training_imagedata_dir: Path,
        labelname_column: str,
        image_pixel_x_size: float = 0.25,
        image_pixel_y_size: float = 0.25,
        image_pixel_width: int = 512,
        image_pixel_height: int = 512,
        force: bool = False) -> Tuple[Path, int]:
    """
    This function prepares training data for the vector labels provided.

    It will:
        * get orthophoto's from a WMS server
        * create the corresponding label mask for each orthophoto
        
    Returns a tuple with (output_dir, dataversion):
        output_dir: the dir where the traindataset was created/found
        dataversion: a version number for the dataset created/found

    Args
        label_infos (List[LabelInfo]): paths to the files with label polygons and locations to generate images for
        labelname_column: the column wqhere the label names are stored in the polygon files
        wms_server_url: WMS server where the images can be fetched from
        wms_layername: layername on the WMS server to use
        output_basedir: the base dir where the train dataset needs to be written to 

    """
    # Init stuff
    image_crs_width = math.fabs(image_pixel_width*image_pixel_x_size)   # tile width in units of crs => 500 m
    image_crs_height = math.fabs(image_pixel_height*image_pixel_y_size) # tile height in units of crs => 500 m

    # Determine the current data version based on existing output data dir(s),
    # but ignore dirs ending on _ERROR
    output_dirs = training_dir.glob(f"[0-9]*/")
    output_dirs = [output_dir for output_dir in output_dirs if not '_BUSY' in output_dir.name]
    logger.info(f"output_dirs: {output_dirs}")
    if len(output_dirs) == 0:
        dataversion_new = 1
    else:
        # Get the output dir with the highest version (=first if sorted desc)
        output_dir_mostrecent = sorted(output_dirs, reverse=True)[0]
        dataversion_mostrecent = int(output_dir_mostrecent.name)
        
        # If none of the input files changed since previous run, reuse dataset
        reuse = False
        for label_file in label_infos:
            reuse = True
            labellocations_output_mostrecent_path = (
                    output_dir_mostrecent / label_file.locations_path.name)
            labeldata_output_mostrecent_path = output_dir_mostrecent / label_file.polygons_path.name
            if(not (labellocations_output_mostrecent_path.exists()
                    and labeldata_output_mostrecent_path.exists()
                    and geofile.cmp(label_file.locations_path, labellocations_output_mostrecent_path)
                    and geofile.cmp(label_file.polygons_path, labeldata_output_mostrecent_path))):
                logger.info(f"RETURN: input label file(s) changed since last prepare_traindatasets, recreate")
                reuse = False
                break
        if reuse == True:
            dataversion_new = dataversion_mostrecent
        else:
            dataversion_new = dataversion_mostrecent + 1
        
    # Process all input files
    output_dir = training_dir / f"{dataversion_new:02d}"
    output_dir.mkdir(parents=True, exist_ok=True)
    labellocations_gdf = None
    labelpolygons_gdf = None
    logger.info(f"Label info: \n{pprint.pformat(label_infos, indent=4)}")
    for label_file in label_infos:

        # Copy the vector files to the dest dir so we keep knowing which files 
        # were used to create the dataset
        geofile.copy(label_file.locations_path, output_dir)
        geofile.copy(label_file.polygons_path, output_dir)

        # Read label data and append to general dataframes
        logger.debug(f"Read label locations from {label_file.locations_path}")
        file_labellocations_gdf = geofile.read_file(label_file.locations_path)
        if file_labellocations_gdf is not None and len(file_labellocations_gdf) > 0:
            file_labellocations_gdf.loc[:, 'filepath'] = str(label_file.locations_path)
            file_labellocations_gdf.loc[:, 'image_layer'] = label_file.image_layer
            # Remark: geopandas 0.7.0 drops the fid column internaly, so cannot be retrieved
            file_labellocations_gdf.loc[:, 'row_nb_orig'] = file_labellocations_gdf.index
            if labellocations_gdf is None:
                labellocations_gdf = file_labellocations_gdf
            else:
                labellocations_gdf = gpd.GeoDataFrame(
                        pd.concat([labellocations_gdf, file_labellocations_gdf], ignore_index=True),
                        crs=file_labellocations_gdf.crs)
        else:
            logger.warn(f"No label locations data found in {label_file.locations_path}")
        logger.debug(f"Read label data from {label_file.polygons_path}")
        file_labelpolygons_gdf = geofile.read_file(label_file.polygons_path)
        if file_labelpolygons_gdf is not None and len(file_labelpolygons_gdf) > 0:
            file_labelpolygons_gdf.loc[:, 'image_layer'] = label_file.image_layer
            if labelpolygons_gdf is None:
                labelpolygons_gdf = file_labelpolygons_gdf
            else:
                labelpolygons_gdf = gpd.GeoDataFrame(
                        pd.concat([labelpolygons_gdf, file_labelpolygons_gdf], ignore_index=True),
                        crs=file_labelpolygons_gdf.crs)
        else:
            logger.warn(f"No label data found in {label_file.polygons_path}")

    # Get the crs to use from the input vectors...
    img_crs = None
    try:
        img_crs = labellocations_gdf.crs
    except Exception as ex:
        logger.exception(f"Error getting crs from labellocations, labellocation_gdf.crs: {labellocations_gdf.crs}")
        raise ex
    if img_crs is None:
        raise Exception(f"Error getting crs from labellocations, labellocation_gdf.crs: {labellocations_gdf.crs}")

    # Create list with only the input labels that need to be burned in the mask
    # TODO: think about a mechanism to ignore label_name's if specified...
    if labelpolygons_gdf is not None and labelname_column in labelpolygons_gdf.columns:
        # If there is a column labelname_column (default='label_name'), use the 
        # burn values specified in the configuration
        labels_to_burn_gdf = labelpolygons_gdf
        labels_to_burn_gdf['burn_value'] = None
        for classname in classes:
            labels_to_burn_gdf.loc[(labels_to_burn_gdf[labelname_column].isin(classes[classname]['labelnames'])),
                                   'burn_value'] = classes[classname]['burn_value']
        
        # If there are burn_values that are not filled out, log + stop!
        invalid_labelnames_gdf = labels_to_burn_gdf.loc[labels_to_burn_gdf['burn_value'].isnull()]
        if len(invalid_labelnames_gdf) > 0:
            raise Exception(f"Unknown labelnames (not in config) were found in {len(invalid_labelnames_gdf)} rows, so stop: {invalid_labelnames_gdf[labelname_column].unique()}")
        
        # Filter away rows that are going to burn 0, as this is useless...
        labels_to_burn_gdf = labels_to_burn_gdf.loc[labels_to_burn_gdf['burn_value'] != 0]

    elif len(classes) == 2:
        # There is no column with label names, but there are only 2 classes (background + subsject), so no problem...
        logger.info(f'Column with label names ({labelname_column}) not found, so use all polygons')
        labels_to_burn_gdf = labelpolygons_gdf
        labels_to_burn_gdf.loc[:, 'burn_value'] = 1

    else:
        # There is no column with label names, but more than two classes, so stop...
        raise Exception(f"Column {labelname_column} is mandatory in labeldata if multiple classes specified: {classes}")

    # Prepare the different traindata types
    output_imagedata_dir = training_imagedata_dir / f"{dataversion_new:02d}"
    for traindata_type in ['train', 'validation', 'test']:

        # If traindata exists already... continue
        output_imagedatatype_dir = output_imagedata_dir / traindata_type
        if output_imagedatatype_dir.exists():
            continue

        # If not, prepare tmp output imagedata dir...
        output_imagedatatype_tmp_dir = None
        for i in range(100):
            output_imagedatatype_tmp_dir = output_imagedata_dir / f"{traindata_type}_BUSY_{i:02d}"
            if output_imagedatatype_tmp_dir.exists():
                try:
                    shutil.rmtree(output_imagedatatype_tmp_dir)
                except:
                    output_imagedatatype_tmp_dir = None
            if not output_imagedatatype_tmp_dir.exists():
                try:
                    output_imagedatatype_tmp_dir.mkdir(parents=True)
                    break
                except:
                    output_imagedatatype_tmp_dir = None
            else:
                output_imagedatatype_tmp_dir = None
        
        # If no output tmp dir could be found... stop...
        if output_imagedatatype_tmp_dir is None:
            raise Exception(f"Error creating output_imagedata_tmp_dir in {training_imagedata_dir}")

        output_imagedata_tmp_image_dir = output_imagedatatype_tmp_dir / 'image'
        output_imagedata_tmp_mask_dir = output_imagedatatype_tmp_dir / 'mask'

        # Create output dirs...
        for dir in [output_imagedatatype_tmp_dir, output_imagedata_tmp_mask_dir, output_imagedata_tmp_image_dir]:
            if dir and not dir.exists():
                dir.mkdir(parents=True)

        try:
            # Get the label locations for this traindata type
            labels_to_use_for_bounds_gdf = (
                    labellocations_gdf[labellocations_gdf['traindata_type'] == traindata_type])
            
            # Loop trough all locations labels to get an image for each of them
            nb_todo = len(labels_to_use_for_bounds_gdf)
            nb_processed = 0
            logger.info(f"Get images for {nb_todo} {traindata_type} labels")
            created_images_gdf = gpd.GeoDataFrame()
            created_images_gdf['geometry'] = None
            start_time = datetime.datetime.now()
            wms_imagelayer_layersources = {}
            for i, label_tuple in enumerate(labels_to_use_for_bounds_gdf.itertuples()):
                
                # TODO: update the polygon if it doesn't match the size of the image...
                # as a start... ideally make sure we use it entirely for cases with
                # no abundance of data
                # Make sure the image requested is of the correct size
                label_geom = label_tuple.geometry
                if label_geom is None:
                    logger.warn(f"No geometry found in file {label_tuple.filepath}, (zero based) row_nb_orig: {label_tuple.row_nb_orig}")
                    continue
                geom_bounds = label_geom.bounds
                xmin = geom_bounds[0]-(geom_bounds[0]%image_pixel_x_size)
                ymin = geom_bounds[1]-(geom_bounds[1]%image_pixel_y_size)
                xmax = xmin + image_crs_width
                ymax = ymin + image_crs_height
                img_bbox = sh_geom.box(xmin, ymin, xmax, ymax)
                image_layer = getattr(label_tuple, 'image_layer')

                # If the wms to be used hasn't been initialised yet
                if image_layer not in wms_imagelayer_layersources:
                    wms_imagelayer_layersources[image_layer] = []
                    for layersource in image_layers[image_layer]['layersources']:
                        wms_service = owslib.wms.WebMapService(
                                url=layersource['wms_server_url'], 
                                version=layersource['wms_version'])
                        wms_imagelayer_layersources[image_layer].append(
                                ows_util.LayerSource(
                                        wms_service=wms_service,
                                        layernames=layersource['layernames'],
                                        layerstyles=layersource['layerstyles'],
                                        bands=layersource['bands'],
                                        random_sleep=layersource['random_sleep']))
                                                
                # Now really get the image
                logger.debug(f"Get image for coordinates {img_bbox.bounds}")
                image_filepath = ows_util.getmap_to_file(
                        layersources=wms_imagelayer_layersources[image_layer],
                        output_dir=output_imagedata_tmp_image_dir,
                        crs=img_crs,
                        bbox=img_bbox.bounds,
                        size=(image_pixel_width, image_pixel_height),
                        image_format=ows_util.FORMAT_PNG,
                        #image_format_save=ows_util.FORMAT_TIFF,
                        image_pixels_ignore_border=image_layers[image_layer]['image_pixels_ignore_border'],
                        transparent=False,
                        layername_in_filename=True)

                # Create a mask corresponding with the image file
                # image_filepath can be None if file existed already, so check if not None...
                if image_filepath is not None:
                    # Mask should not be in a lossy format!
                    mask_filepath = Path(str(image_filepath)
                            .replace(str(output_imagedata_tmp_image_dir), str(output_imagedata_tmp_mask_dir))
                            .replace('.jpg', '.png'))
                    nb_classes = len(classes)
                    # Only keep the labels that are meant for this image layer
                    labels_gdf = (labels_to_burn_gdf.loc[
                                        labels_to_burn_gdf['image_layer'] == image_layer]).copy()
                    # assert to evade pyLance warning
                    assert isinstance(labels_gdf, gpd.GeoDataFrame)
                    if len(labels_gdf) == 0:
                        logger.info("No labels to be burned for this layer, this is weird!")
                    _create_mask(
                            input_image_filepath=image_filepath,
                            output_mask_filepath=mask_filepath,
                            labels_to_burn_gdf=labels_gdf,
                            nb_classes=nb_classes,
                            force=force)
                
                # Log the progress and prediction speed
                nb_processed += 1
                time_passed = (datetime.datetime.now()-start_time).total_seconds()
                if time_passed > 0 and nb_processed > 0:
                    processed_per_hour = (nb_processed/time_passed) * 3600
                    hours_to_go = (int)((nb_todo - i)/processed_per_hour)
                    min_to_go = (int)((((nb_todo - i)/processed_per_hour)%1)*60)
                    print(f"\r{hours_to_go:3d}:{min_to_go:2d} left for {nb_todo-i} of {nb_todo} at {processed_per_hour:0.0f}/h", 
                          end="", flush=True)
        
            # If everything went fine, rename output_imagedata_tmp_dir to the final output_imagedata_dir
            os.rename(output_imagedatatype_tmp_dir, output_imagedatatype_dir)
        except Exception as ex:
            raise ex

    return (output_imagedata_dir, dataversion_new)

''' Not maintained!
def create_masks_for_images(
        input_vector_label_filepath: str,
        input_image_dir: str,
        output_basedir: str,
        image_subdir: str = 'image',
        mask_subdir: str = 'mask',
        burn_value: int = 255,
        force: bool = False):

    # Check if the input file exists, if not, return
    if not os.path.exists(input_vector_label_filepath):
        message = f"Input file doesn't exist, so do nothing and return: {input_vector_label_filepath}"
        raise Exception(message)
    # Check if the input file exists, if not, return
    if not os.path.exists(input_image_dir):
        message = f"Input image dir doesn't exist, so do nothing and return: {input_image_dir}"
        raise Exception(message)
    
    # Determine the current data version based on existing output data dir(s), but ignore dirs ending on _ERROR
    output_dirs = glob.glob(f"{output_basedir}_*")
    output_dirs = [output_dir for output_dir in output_dirs if output_dir.endswith('_BUSY') is False]
    if len(output_dirs) == 0:
        dataversion_new = 1
    else:
        # Get the output dir with the highest version (=first if sorted desc)
        output_dir_mostrecent = sorted(output_dirs, reverse=True)[0]
        output_subdir_mostrecent = os.path.basename(output_dir_mostrecent)
        dataversion_mostrecent = int(output_subdir_mostrecent.split('_')[1])
        dataversion_new = dataversion_mostrecent + 1
        
        # If the input vector label file didn't change since previous run 
        # dataset can be reused
        output_vector_mostrecent_filepath = os.path.join(
                output_dir_mostrecent, os.path.basename(input_vector_label_filepath))
        if(os.path.exists(output_vector_mostrecent_filepath)
           and geofile.cmp(input_vector_label_filepath, 
                                  output_vector_mostrecent_filepath)):
            logger.info(f"RETURN: input vector label file isn't changed since last prepare_traindatasets, so no need to recreate")
            return output_dir_mostrecent, dataversion_mostrecent

    # Create the output dir's if they don't exist yet...
    output_dir = f"{output_basedir}_{dataversion_new:02d}"
    output_tmp_dir = f"{output_basedir}_{dataversion_new:02d}_BUSY"
    output_tmp_image_dir = os.path.join(output_tmp_dir, image_subdir)
    output_tmp_mask_dir = os.path.join(output_tmp_dir, mask_subdir)

    # Prepare the output dir...
    if os.path.exists(output_tmp_dir):
        shutil.rmtree(output_tmp_dir)
    for dir in [output_tmp_dir, output_tmp_mask_dir, output_tmp_image_dir]:
        if dir and not os.path.exists(dir):
            os.makedirs(dir)

    # Copy the vector file(s) to the dest dir so we keep knowing which file was
    # used to create the dataset
    geofile.copy(input_vector_label_filepath, output_tmp_dir)
    
    # Open vector layer
    logger.debug(f"Open vector file {input_vector_label_filepath}")
    input_label_gdf = gpd.read_file(input_vector_label_filepath)

    # Create list with only the input labels that are positive examples, as 
    # are the only ones that will need to be burned in the mask
    labels_to_burn_gdf = input_label_gdf[input_label_gdf['burninmask'] == 1]
    
    # Loop trough input images
    input_image_filepaths = glob.glob(f"{input_image_dir}/*.tif")
    logger.info(f"process {len(input_image_filepaths)} input images")
    for input_image_filepath in input_image_filepaths:
        _, input_image_filename = os.path.split(input_image_filepath)
        
        image_filepath = os.path.join(output_tmp_image_dir, input_image_filename)
        shutil.copyfile(input_image_filepath, image_filepath)

        mask_filepath = os.path.join(output_tmp_mask_dir, input_image_filename)
        _create_mask(
                input_image_filepath=image_filepath,
                output_mask_filepath=mask_filepath,
                labels_to_burn_gdf=labels_to_burn_gdf,
                force=force)
'''

def _create_mask(
        input_image_filepath: Path,
        output_mask_filepath: Path,
        labels_to_burn_gdf: gpd.GeoDataFrame,
        nb_classes: int = 1,
        output_imagecopy_filepath: Optional[Path] = None,
        minimum_pct_labeled: float = 0.0,
        force: bool = False) -> Optional[bool]:

    # If file exists already and force is False... stop.
    if(force is False
       and output_mask_filepath.exists()):
        logger.debug(f"Output file already exist, and force is False, return: {output_mask_filepath}")
        return

    # Create a mask corresponding with the image file
    # First read the properties of the input image to copy them for the output
    logger.debug(f"Create mask to {output_mask_filepath}")
    with rio.open(input_image_filepath) as image_ds:
        image_input_profile = image_ds.profile
        image_transform_affine = image_ds.transform

    # Prepare the file profile for the mask depending on output type
    output_ext_lower = output_mask_filepath.suffix.lower()
    if output_ext_lower == '.tif':
        image_output_profile = rio_profiles.DefaultGTiffProfile(
                count=1, transform=image_transform_affine, crs=image_input_profile['crs'])
    if output_ext_lower == '.png':
        image_output_profile = rio_profiles.Profile(driver='PNG', count=1)
    else:
        raise Exception(f"Unsupported mask extension (should be a lossless format!): {output_ext_lower}")
    image_output_profile.update(
            width=image_input_profile['width'], height=image_input_profile['height'], 
            dtype=rio.uint8)

    # Burn the vectors in a mask
    burn_shapes = ((geom, value) 
            for geom, value in zip(labels_to_burn_gdf.geometry, labels_to_burn_gdf.burn_value) if geom is not None)
    try:
        mask_arr = rio_features.rasterize(
                shapes=burn_shapes, transform=image_transform_affine,
                dtype=rio.uint8, fill=0, 
                out_shape=(image_output_profile['width'], image_output_profile['height']))
    except Exception as ex:
        raise Exception(f"Error creating mask for {image_transform_affine}") from ex

    # Check if the mask meets the requirements to be written...
    if minimum_pct_labeled > 0:
        nb_pixels = np.size(mask_arr, 0) * np.size(mask_arr, 1)
        nb_pixels_data = nb_pixels - np.sum(mask_arr == 0)  #np.count_nonnan(image == NoData_value)
        logger.debug(f"nb_pixels: {nb_pixels}, nb_pixels_data: {nb_pixels_data}, pct data: {nb_pixels_data / nb_pixels}")

        if (nb_pixels_data / nb_pixels < minimum_pct_labeled):
            return False

    # Write the labeled mask as .png (so without transform/crs info)
    im = Image.fromarray(mask_arr)
    im.save(output_mask_filepath)
    
    return True

if __name__ == "__main__":
    raise Exception('Not implemented!')
