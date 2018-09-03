# median_color_quantifier.py
# Author: Kenneth Diogo
#
# This file provides functions to reduce the number of distinct colors used in an image to a palette of size 2^n
# The program accomplishes this by implementing the median cut algorithm


from PIL import Image
import math
import numpy as np
import scipy.misc as smp


# Returns a new sorted list from the given parameter that is sorted by the color value (r, g, or b) that has the greatest range
def median_cut_sorter(bucket):
    # -----Find the max and mins in the color bucket----
    redMin = bucket[0][0]
    greenMin = bucket[0][1]
    blueMin = bucket[0][2]

    redMax = bucket[0][0]
    greenMax = bucket[0][1]
    blueMax = bucket[0][2]
    for color in bucket:
        if color[0] < redMin:
            redMin = color[0]
        if color[1] < greenMin:
            greenMin = color[1]
        if color[2] < blueMin:
            blueMin = color[2]

        if color[0] > redMax:
            redMax = color[0]
        if color[1] > greenMax:
            greenMax = color[1]
        if color[2] > blueMax:
            blueMax = color[2]
    # -----------------------------------------------

    # -----Determine which color value to sort by----
    redRange = redMax - redMin
    greenRange = greenMax - greenMin
    blueRange = blueMax - blueMin
    if (redRange > greenRange and redRange > blueRange):
        sortKey = 0
    elif (greenRange > redRange and greenRange > blueRange):
        sortKey = 1
    else:
        sortKey = 2
    # -----------------------------------------------

    return sorted(bucket, key=lambda x: x[sortKey],
                  reverse=False)  # return a new list that is sorted by the determined color value


# Helper function that returns the average of all colors in a given color bucket
def average_color(bucket):
    red = 0
    green = 0
    blue = 0
    size = len(bucket)
    for color in bucket:
        red += color[0]
        green += color[1]
        blue += color[2]

    return (int(red / size), int(green / size), int(blue / size))


# Implemented with median cut algorithm
def color_quantify(palette_size, im):
    """
    Returns a list of rgb values of length palette_size that is created from an image

    :param palette_size: Number of colors in palette
    :param im: PIL loaded image
    :return: List of rgb values
    """

    iterations = int(math.log(palette_size, 2))  # x = how many times each bucket must be duplicated Where 2^x = palette_size
    pixel_img = im.load()
    # ------Create the first bucket which contains all rgb values in the given image------
    color_buckets = []
    firstBucket = []
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            firstBucket.append(pixel_img[i, j])
    color_buckets.append(firstBucket)
    # -------------------------------------------------------------------------------------

    # Move, sort, and add the upper half of each bucket into the list
    for i in range(iterations):
        for index in range(len(color_buckets)):
            color_buckets.append(median_cut_sorter(color_buckets[index][len(color_buckets[index]) // 2:]))
            color_buckets[index] = color_buckets[index][0:len(color_buckets[index]) // 2]

    color_palette = []
    for bucket in color_buckets:
        color_palette.append(average_color(bucket))
    return color_palette


# Helper function
def closest_color(color_palette, rgb):
    """
    Maps a given rgb value to the closest rgb value in a given color palette

    :param color_palette: List of rgb colors used
    :param rgb: Rgb value being mapped
    :return: Mapped rgb value from color_palette
    """

    # "Closeness" of color is defined as the lowest 3-D euclidean distance
    # Euclidean distance uses bias scalars to account for color sensitivities from the human eye
    RED_BIAS = 0.3
    GREEN_BIAS = 0.59
    BLUE_BIAS = 0.11
    # Find lowest euclidean distance
    closest_color = color_palette[0]
    lowest_dist = math.sqrt(int((rgb[0] - color_palette[0][0]) * RED_BIAS) ** 2 + int(
        (rgb[1] - color_palette[0][1]) * GREEN_BIAS) ** 2 + int((rgb[2] - color_palette[0][2]) * BLUE_BIAS) ** 2)
    for color in color_palette:
        distance = math.sqrt(
            int((rgb[0] - color[0]) * RED_BIAS) ** 2 + int((rgb[1] - color[1]) * GREEN_BIAS) ** 2 + int(
                (rgb[2] - color[2]) * BLUE_BIAS) ** 2)
        if (distance < lowest_dist):
            lowest_dist = distance
            closest_color = color

    return closest_color


def create_reduced_image(filename, outputName, palette_size):
    """
    Saves a color quantified png image to the current directory

    :param filename: Directory of image to be simplified
    :param outputName: Name of image that will be outputted
    :param palette_size: Number of distinct colors in output image
    :return:
    """

    im = Image.open(filename)
    pix = im.load()

    color_pal = color_quantify(palette_size, im)
    img_data = np.zeros((im.size[0], im.size[1], 3), dtype=np.uint8)
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            img_data[i, j] = closest_color(color_pal, pix[i, j])

    # img = smp.toimage(img_data)
    smp.imsave(outputName, img_data)
    # img.show()


# Test tool
def distinct_colors(fileName):
    colors = {}
    im = Image.open(fileName)
    pix = im.load()
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            colors[pix[i, j]] = 1

    return len(colors)
