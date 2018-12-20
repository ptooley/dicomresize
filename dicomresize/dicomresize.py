#!/usr/bin/env python3

import argparse
import pydicom
import scipy.ndimage as sn


def dicomresize_parse_args():
    parser = argparse.ArgumentParser("Dicom resizing")
    parser.add_argument("input_file", metavar="input.dcm", type=str,
                        help="Input dicom image")
    parser.add_argument("output_file", metavar="output.dcm", type=str,
                        help="Output dicom image")
    parser.add_argument("new_size", nargs='+', metavar="NNN",
                        type=int, help="Target dimensions in pixels")

    args = parser.parse_args()
    return args


def dicomresize():
    args = dicomresize_parse_args()

    try:
        dcm_in = pydicom.dcmread(args.input_file)
    except (FileNotFoundError, PermissionError):
        print("Error: failed to open file \"{}\" (Does it exist and "
              "are the permissions correct?)".format(args.input_file))
        return -1
    except pydicom.errors.InvalidDicomError:
        print("Error: \"{}\" is not a valid DICOM file."
              "".format(args.input_file))
        return -2

    shape_in = dcm_in.pixel_array.shape
    shape_out = args.new_size
    if len(shape_out) != len(shape_in):
        print("Error: Output shape must have same dimensions as input image,"
              "(got Input: {}, Output {})".format(shape_in, shape_out))

    scale = [so/si for so, si in zip(shape_out, shape_in)]
    pix_out = sn.zoom(dcm_in.pixel_array, scale)

    dcm_in.PixelData = pix_out.tobytes()
    if len(shape_out) == 2:
        dcm_in.Rows, dcm_in.Columns = shape_out
    else:
        dcm_in.Rows, dcm_in.Columns, dcm_in.Slices = shape_out

    dcm_in.save_as(args.output_file)
