# Contains utility functions that are used by the routes in this package
import os
import secrets              # Package that generates a random hex value
from PIL import Image       # Pillow package that helps to resize image
from flask import render_template, url_for  # Not needed here but commonly used, clean up if not used on submission!
from boostly import application



# This function saves/updates images in our database
def saveImage(formUploadedImage):
    # Renaming the image to a unique/random 8 byte hex so that there won't be any conflicting file names in the database
    randomHexImage = secrets.token_hex(8)
    # Splitting the file name from file extension so I can grab the extension and append it to my new hex value
    # I'm not using the file name variable, so I'm using '_' as a throwaway variable name
    _, fileExtension = os.path.splitext(formUploadedImage.filename)
    randomHexImage = randomHexImage + fileExtension
    # Concats the os path to the image
    imagePath = os.path.join(application.root_path, 'static/profilePics', randomHexImage)
    # Resizing image so that it's no more than 125px -- This allows us to save space and run more efficiently
    outputSize = (125, 125)
    imageThumb = Image.open(formUploadedImage)
    imageThumb.thumbnail(outputSize)
    # Saving the thumbnail image to the image path
    imageThumb.save(imagePath)
    # Returning the image for updating in the database
    return randomHexImage

