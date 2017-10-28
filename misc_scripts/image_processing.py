# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 10:26:09 2017

@author: Gabe Madonna
"""

import os
import sys
import cv2
import numpy as np
import serial, time
from matplotlib import pyplot as plt

#user_in = 'x'
#while user_in.lower() not in ['h', 'y']:
#    print('Cube face images uploaded?')
#    user_in = input('[H]elp [Y]es')
#if user_in.lower() == 'h':
#    print('photograph the cube (using square-shaped photos, if possible)')
#    print('in the order of faces with center pieces of')
#    print('red, white, yellow, blue, orange, green, respectively,' )
#    print('with orientation of the white-centered face such that the bottom edge')
#    print('is shared with the red face and orientation of the yellow_centered face')
#    print('such that the top edge is shared with the red face, and')
#    print('orientation of the remaining faces such that the top edge is')
#    print('shared with the white face.')
#    print('Then upload these pictures to the pictures folder in the rubix folder')
#    print('of Google Drive.')
#    print()
#    input('Press enter to continue')

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

def match_color(pixel):
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
    
def get_color_matrix(image, side_length = -1):
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
#            print(av_pixel)
            color_matrix[y + 1].append(match_color(av_pixel))
    return color_matrix 

def cube_is_valid(cube):
    '''
    counts the number of occurances for each tile color
    and returns true if each is exactly 9
    cube: list of face color matricies
    '''
    freq_dict = {}
    for tile in np.array(cube).flatten():
        freq_dict[tile] = freq_dict.get(tile, 0) + 1
#    print(freq_dict)
    return sum(list(map(lambda count: count != 9, freq_dict.values()))) == 0


def print_cube(cube):
    '''
    prints easy to read visualizeation of cube
    '''
    for face in cube:
        print(np.array(face))
        print()

colors = ('R', 'W', 'Y', 'B', 'O', 'G')

while os.getcwd() != 'C:\\':
    os.chdir("..")

os.chdir('Users\\Gabe Madonna\\Google Drive\\rubix project\\pictures')
face_files = os.listdir()
face_images = list(map(cv2.imread, face_files))
ref_pixels = list(map(get_av_pixel, face_images))
ref_dict = dict(zip(colors, ref_pixels))
rubix_cube = list(map(get_color_matrix, face_images))
print_cube(rubix_cube)
print('valid cube:', cube_is_valid(rubix_cube))

print(rubix_cube)
