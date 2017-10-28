# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 22:50:07 2017

@author: Gabe Madonna
"""
import numpy as np


def get_av_pixel(image, center = (-1, -1), radius = 250, num = 10):
    '''
    make array of pixels at center that is radius wide 
    and has num pixels to a side
    average values,
    return averaged pixel
    
    image: frame
    center: 2d list (y, x)
    radius: int
    num: int
    
    returns pxls_av
    '''
    if center == (-1, -1): 
        center = (len(image)//2, len(image[0])//2) 
    
    blue, green, red = [], [], []
    for y in range(-num, num + 1):
        for x in range(-num, num + 1):
            y_coord = int(center[0] + y * radius / num)
            x_coord = int(center[1] + x * radius / num)
            [b,g,r] = image[y_coord][x_coord]
            blue += [b]
            green += [g]
            red += [r]
            
    return [np.mean(blue), np.mean(green), np.mean(red)]

def match_color(pixel, ref_dict):
    '''
    takes given color and uses euclidean distance to 
    match the color to the nearest reference color and returns
    that reference color
    
    color: 3d list (pixel):
    returns: color letter
    '''
    colors = list(ref_dict.keys())
    color_vals = (ref_dict.values())
    dists = list(map(lambda ref: np.linalg.norm(np.array(pixel) - ref), color_vals))
    return colors[dists.index(min(dists))]
    
def get_color_matrix(image, ref_dict, side_length = -1):
    '''
    takes the image of a face and gets average pixel value for each 
    tile (using side_length as bounds) and then assigns a color to 
    each tile and returns a matrix of those colors
    image: matrix of pixels
    side_length: int
    returns color_matrix: 2d matric of color letters
    '''
    if side_length == -1: 
        side_length = len(image[0])
    
    center_y, center_x = len(image)//2, len(image[0])//2 
    tile_width = side_length // 3
    color_matrix = [[], [], []]
    
    for y in [-1, 0, 1]:
        for x in [-1, 0, 1]:
            tile_center_y = center_y + y * tile_width
            tile_center_x = center_x + x * tile_width
            av_pixel = get_av_pixel(image, center = (tile_center_y, tile_center_x), 
                                    radius = 250, num = 10)
            color_matrix[y + 1].append(match_color(av_pixel, ref_dict))
    return color_matrix 