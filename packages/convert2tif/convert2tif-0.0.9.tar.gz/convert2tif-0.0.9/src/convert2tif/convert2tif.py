import os
import glob
from PIL import Image, UnidentifiedImageError


def convert(input_path=".", output_path=None):
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
    print("Converting...")
    # Iterate through every item in the provided directory
    for file in glob.glob(input_path+"/*"):

        try:
            # Open each image
            tif = Image.open(file)

        # Skip over unrecognized files/directories and return error to user
        except UnidentifiedImageError:
            print(f"Skipping {file.split('/')[-1]}: file not supported")
        except IsADirectoryError:
            print(f"Skipping {file}: is a directory")

        else:
            # Get image base filename (name minus file extension)
            basename = "".join(tif.filename.split("/")[-1].split(".")[:-1])
            # Create output directory if no output path is provided
            if output_path is None:
                # Create 'output' directory if one does not exist
                if not os.path.exists("./output"):
                    os.mkdir("./output")
                # Set output_path to output folder
                output_path = "./output"

            # Save image with basename to output path
            tif.save(f"{output_path}/{basename}.tif")
