from os import listdir, path
from os.path import isfile, join

from PIL import Image

"""
AliPic  

"""
# Structure
"""
.\original -> original pictures
.\resize -> resized pictures
.\out - > file output
.\watermark -> File to watermark mask with
"""
main_folder = path.realpath(path.dirname(__file__))
out_folder = path.join(main_folder, "out")
resize = path.join(main_folder, "resized")
picture_folder = path.join(main_folder, "original")
watermark_path = path.join(main_folder, "watermark")


def watermark_it(input_image_path,
                 output_image_path,
                 watermark_image_path,
                 position):
    base_image = Image.open(input_image_path).convert("RGBA")
    watermark = Image.open(watermark_image_path).convert("RGBA")
    width, height = base_image.size

    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, position, mask=watermark)
    transparent = transparent.convert("RGB")
    transparent.save(output_image_path)


def ResizeOriginal(PictureFile):
    """
    Given the Picture file 
    Resize and save in the resize folder with the prefix of Miteko_

    Parameters: 
    string: Picture Name
    """
    # Resize it 1000 pixel
    basewidth = 1000
    img = Image.open(path.join(picture_folder, PictureFile))
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save(path.join(resize, "Miteko_" + PictureFile))


def GetMeThePictures(mypath):
    """
    Get the Pictures in the Original Folder. 
    Parameters: 
    Folder / Location
    Returns: 
    List: Files in the folder as in list 
    TODO : filter the files . 
    """
    OriginalPictures = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return OriginalPictures


if __name__ == '__main__':

    # Get the original files.
    TheOriginalPictures = GetMeThePictures(picture_folder)

    # Resize the Original files.
    for each_picture in TheOriginalPictures:
        ResizeOriginal(each_picture)

    # Work on Resized images and add watermark
    TheResizedPictures = GetMeThePictures(resize)
    watermark_img = path.join(watermark_path, "watermark.png")
    for eachResizedPicture in TheResizedPictures:
        img = path.join(resize, eachResizedPicture)
        out_img = path.join(out_folder, eachResizedPicture)
        watermark_it(img, out_img, watermark_img, position=(0, 0))

    print ("Done")
