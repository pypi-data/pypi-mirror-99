import glob
import sys
import os
import numpy as np
import csv
import copy
import re
from cryolo import CoordsIO, utils
from cryoloBM import boxmanager_tools as bmtools

def read_eman1_helicon_micrgraph_name(path):
    with open(path, "r") as csvfile:
        csvlines = csvfile.readlines()
        for index, row in enumerate(csvlines):
            if row.startswith("#micrograph"):
                pat = "#micrograph:\s(.+)"
                reexp_res = re.findall(pat,row)
                return reexp_res[0]

def write_coords_file(path, array):
    np.savetxt(path, array, delimiter=" ", fmt="%10.5f")

    '''
    with open(path, "w") as coordsfile:
        boxwriter = csv.writer(
            coordsfile, delimiter=" ", quotechar="|", quoting=csv.QUOTE_NONE
        )

        for row in array:
            boxwriter.writerow([row[0], row[1], row[2]])
    '''


def scale(input_path,
          output_path,
          scale_factor):
    '''
    This function reads the coordinates in the input_type given the input_type, scales them
    according the scale_factor and write them back into the output_path
    :param input_path:
    :param output_path:
    :param scale_factor:
    :return:
    '''

    # 1. Read data according input_type.
    # 2. Call respective scale function
    # 3. Write to disk

    os.makedirs(output_path, exist_ok=True)
    if os.path.isfile(input_path):
        files = [input_path]
    else:
        path = os.path.join(os.path.abspath(input_path), "*")
        files = glob.glob(path)

    for pth in files:
        if bmtools.get_file_type(pth) == bmtools.TYPE_COORDS:
            coords = [np.atleast_2d(np.genfromtxt(pth))]
            scaled_coords = scale_coords(coords, scale_factor)
            output_file_path = os.path.join(output_path,os.path.basename(pth))
            write_coords_file(output_file_path,scaled_coords[0])
        elif bmtools.get_file_type(pth) == bmtools.TYPE_EMAN_HELICON:
            filaments_per_file = CoordsIO.read_eman1_helicon(pth)
            mic_name = read_eman1_helicon_micrgraph_name(pth)
            scaled_filaments = scale_filament(filaments_per_file,scale_factor)
            output_file_path = os.path.join(output_path, os.path.basename(pth))
            CoordsIO.write_eman1_helicon(scaled_filaments, output_file_path, mic_name)
        elif bmtools.get_file_type(pth) == bmtools.TYPE_CBOX:
            coords = CoordsIO.read_cbox_boxfile(pth)
            addinclude = CoordsIO.read_cbox_include_list(pth)
            scaled_coords = []
            for elem in coords:
                if isinstance(elem,utils.Filament):
                    scaled_elem = scale_filament([elem], scale_factor)[0]
                else:
                    scaled_elem = scale_boxes([elem],scale_factor)[0]
                scaled_coords.append(scaled_elem)
            output_file_path = os.path.join(output_path, os.path.basename(pth))
            CoordsIO.write_cbox_file(path=output_file_path, coordinates=scaled_coords,additional_slice_include=addinclude)


        else:
            print("File type not supported yet", pth)

def scale_boxes(boxes, scale):
    scaled_boxes = []
    for box in boxes:
        sbox = copy.deepcopy(box)
        sbox.x = sbox.x * scale
        sbox.y = sbox.y * scale
        if sbox.z is not None:
            sbox.z = sbox.z * scale
        sbox.h = sbox.h * scale
        sbox.w = sbox.w * scale
        scaled_boxes.append(sbox)
    return scaled_boxes

def scale_filament(filaments, scale):
    scaled_filaments = []
    for fil in filaments:
        sfil = copy.deepcopy(fil)
        sfil.boxes = scale_boxes(sfil.boxes,scale)
        scaled_filaments.append(sfil)

    return scaled_filaments

def scale_coords(list_of_coords, scale):
    scaled = []
    for coords in list_of_coords:
        coords[:,:3] = coords[:,:3] * scale
        scaled.append(coords)
    return scaled


def scale_fil_seg():
    pass