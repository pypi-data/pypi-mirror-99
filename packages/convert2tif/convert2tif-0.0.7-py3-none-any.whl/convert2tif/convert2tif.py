import os
import glob
from PIL import Image, UnidentifiedImageError


def convert(input_path="*", output_path=None):
    """
    Converts image(s) to .tif/.tiff file format.

    Args:
    -----

        input_path: str
            String indicating path to directory of images to be converted. Uses
            current directory if no input path is provided.

        output_path: str
            String indicating path to directory where converted images will be
            saved. Creates a new 'output' directory within the current
            directory if no output path is provided.
    """
    # Iterate through every item in the provided directory
    for image in glob.glob(input_path):

        try:
            # Open each image
            tif = Image.open(image)

        except UnidentifiedImageError:
            print("File not supported.")

        else:
            # Get image base filename (name minus file extension)
            basename = "".join(tif.filename.split("/")[-1].split(".")[:-1])
            print(basename)

            # Create output directory if not output path is provided
            if output_path is None:
                output_path = "./output"
                os.mkdir(output_path)

            # Save image with basename to output path
            tif.save(f"{output_path}/{basename}.tif")
