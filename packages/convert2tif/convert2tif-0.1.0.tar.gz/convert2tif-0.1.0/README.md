# Convert to Tif

## Description

This is a small package that will change any image file that [Pillow](https://pillow.readthedocs.io/en/stable/) supports to a [tif](https://fileinfo.com/extension/tif) file format.

## Installation

Copy the link above to install.

## Documentation

To import the `convert` function:
`from convert2tif.convert2tif import convert`

convert2tif.convert(input_path=".", output_path=None)
Args:
-----

    input_path: str
        String indicating path to directory of images to be converted. Uses
        current directory if no input path is provided.

    output_path: str
        String indicating path to directory where converted images will be
        saved. Creates a new 'output' directory within the current
        directory if no output path is provided.
