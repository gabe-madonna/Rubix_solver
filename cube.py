# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 12:45:12 2017

@author: Gabe Madonna
"""
import numpy as np
import pandas as pd
import copy
from string import digits
import random
import os
import cv2
import graphics

COLORS = ('R', 'W', 'Y', 'B', 'O', 'G')
SIDES = ('F', 'U', 'D', 'R', 'B', 'L')
opposite_side = {'U': 'D', 'D':'U', 'L':'R', 'R':'L', 'F':'B', 'B':'F'}

class Cube(object):
    def __init__(self, new_cube):
        self.cube = new_cube
        self.turns = []
        self.directions = []
        
        
    def __str__(self):
        for face in SIDES:
            print(pd.DataFrame.__str__(self.cube[face]))
            print()
        return ''
        
    def turn(self, face, d = 1):
        '''
        face: face as 'F', 'B', 'L', 'R', 'U', 'D'
        d: 1 or -1 multiplier (1 is clockwise, -1 is counter-clockwise)
        '''
        if d == 1:
            self.directions.append(face + '+')
        else: 
            self.directions.append(face + '-')
        r_copy = self.cube[face].copy()
        for row in [-1, 0, 1]:
            for col in [-1, 0, 1]:
                if row == col:
                    self.cube[face].loc[row, col] = r_copy.loc[d * row, -1 * d * col]
                elif row == -1 * col:
                    self.cube[face].loc[row, col] = r_copy.loc[-1 * d * row, d * col]
                elif row == 0:
                    self.cube[face].loc[row, col] = r_copy.loc[d * col, 0]
                elif col == 0:
                    self.cube[face].loc[row, col] = r_copy.loc[0, -1 * d * row]
                    
        self.help_turn(face, d)
    
    def help_turn(self, face, d):
        
        front = self.cube['F'] 
        back = self.cube['B']         
        right = self.cube['R']           
        left = self.cube['L']  
        up = self.cube['U'] 
        down = self.cube['D']
        
        front_copy = front.copy()
        back_copy = back.copy()
        left_copy = left.copy()
        right_copy = right.copy()
        up_copy = up.copy()
        down_copy = down.copy()
        
        if face in ['U', 'D']:
            x = 0
            if face == 'U':
                faces = [right, back, left, front]
                x = 1
            else:
                faces = [right, front, left, back]
                x = -1
            faces_copy = copy.deepcopy(faces)
            
            for i in range(0, len(faces)):
                if i + d == 4:
                    d = -3
                faces[i].loc[x, [-1, 0, 1]]  = faces_copy[i + d].loc[x, [-1, 0, 1]] 
        
        if face == 'F':
            if d == 1:
                up.loc[-1, [-1, 0, 1]] = left_copy.loc[[-1, 0, 1], 1].values
                down.loc[1, [-1, 0, 1]] = right_copy.loc[[-1, 0, 1], -1].values
                right.loc[[-1, 0, 1], -1] = up_copy.loc[-1, [1, 0, -1]].values
                left.loc[[-1, 0, 1], 1] = down_copy.loc[1, [1, 0, -1]].values

            else:
                up.loc[-1, [-1, 0, 1]] = right_copy.loc[[1, 0, -1], -1].values
                down.loc[1, [-1, 0, 1]] = left_copy.loc[[1, 0, -1], 1].values
                right.loc[[-1, 0, 1], -1] = down_copy.loc[1, [-1, 0, 1]].values
                left.loc[[-1, 0, 1], 1] = up_copy.loc[-1, [-1, 0, 1]].values
                
        if face == 'B':
            if d == 1:
                up.loc[1, [1, 0, -1]] = right_copy.loc[[-1, 0, 1], 1].values
                down.loc[-1, [1, 0, -1]] = left_copy.loc[[-1, 0, 1], -1].values
                right.loc[[1, 0, -1], 1] = down_copy.loc[-1, [1, 0, -1]].values
                left.loc[[1, 0, -1], -1] = up_copy.loc[1, [1, 0, -1]].values
            else:
                up.loc[1, [1, 0, -1]] = left_copy.loc[[1, 0, -1], -1].values
                down.loc[-1, [1, 0, -1]] = right_copy.loc[[1, 0, -1], 1].values
                right.loc[[1, 0, -1], 1] = up_copy.loc[1, [-1, 0, 1]].values
                left.loc[[1, 0, -1], -1] = down_copy.loc[-1, [-1, 0, 1]].values
                
        if face == 'R':
            if d == 1:
                up.loc[[-1, 0, 1], 1] = front_copy.loc[[-1, 0, 1], 1].values
                down.loc[[-1, 0, 1], 1] = back_copy.loc[[1, 0, -1], -1].values
                front.loc[[-1, 0, 1], 1] = down_copy.loc[[-1, 0, 1], 1].values
                back.loc[[1, 0, -1], -1] = up_copy.loc[[-1, 0, 1], 1].values
            else:
                up.loc[[-1, 0, 1], 1] = back_copy.loc[[1, 0, -1], -1].values
                down.loc[[-1, 0, 1], 1] = front_copy.loc[[-1, 0, 1], 1].values
                front.loc[[-1, 0, 1], 1] = up_copy.loc[[-1, 0, 1], 1].values
                back.loc[[1, 0, -1], -1] = down_copy.loc[[-1, 0, 1], 1].values
                
        if face == 'L':
            if d == 1:
                up.loc[[-1, 0, 1], -1] = back_copy.loc[[1, 0, -1], 1].values
                down.loc[[-1, 0, 1], -1] = front_copy.loc[[-1, 0, 1], -1].values
                front.loc[[-1, 0, 1], -1] = up_copy.loc[[-1, 0, 1], -1].values
                back.loc[[1, 0, -1], 1] = down_copy.loc[[-1, 0, 1], -1].values
            else:
                up.loc[[-1, 0, 1], -1] = front_copy.loc[[-1, 0, 1], -1].values
                down.loc[[-1, 0, 1], -1] = back_copy.loc[[1, 0, -1], 1].values
                front.loc[[-1, 0, 1], -1] = down_copy.loc[[-1, 0, 1], -1].values
                back.loc[[1, 0, -1], 1] = up_copy.loc[[-1, 0, 1], -1].values
            
        self.cube['F'] = front   
        self.cube['B'] = back
        self.cube['L'] = left
        self.cube['R'] = right       
        self.cube['U'] = up
        self.cube['D'] = down
        
    def solve(self):
        #white cross:
        edges = (('F2', 'U8'), ('R2', 'U6'), ('B2', 'U2'), ('L2', 'U4'))
        for edge in edges:
            if self.to_colors(edge) != rubix_key.to_colors(edge):
                self.solve_white_cross(edge)
        
        #white corners:
        corners = (('U1', 'L1', 'B3'), ('U3', 'B1', 'R3'),
                    ('U7', 'F1', 'L3'), ('U9', 'R1', 'F3'))
        for corner in corners:
            if self.to_colors(corner) != rubix_key.to_colors(corner):
                self.solve_white_corners(corner)
        
        #horizontal edges:
        edges = (('F6', 'R4'), ('R6', 'B4'), ('B6', 'L4'), ('L6', 'F4'))
        for edge in edges:
            if self.to_colors(edge) != rubix_key.to_colors(edge):
                self.solve_horizontal_edges(edge)
        
        #yellow_cross:
        tiles = ('D2', 'D6', 'D8', 'D4')
        for tile in tiles:
            if self.to_colors([tile]) != ['Y']:
                self.solve_yellow_cross()
                continue
        
        #yellow corners:
        tiles = ('D1', 'D3', 'D7', 'D9')
        for tile in tiles:
            if self.to_colors([tile]) != ['Y']:
                self.solve_yellow_corners()
                continue
        
        #final corners:
        corners = (('D1', 'L9', 'F7'), ('D3', 'F9', 'R7'),
                   ('D7', 'B9', 'L7'), ('D9', 'R9', 'B7'))
        for corner in corners:
            if self.to_colors(corner) != rubix_key.to_colors(corner):
                self.solve_final_corners()
                continue
        
        #final edges:
        edges = (('F8', 'D2'), ('R8', 'D6'), ('B8', 'D8'), ('L8', 'D4'))
        for edge in edges:
            if self.to_colors(edge) != rubix_key.to_colors(edge):
                self.solve_final_edges()
                continue
        
        self.prune_directions()
        return self.directions
    
    def solve_white_cross(self, edge):
        def update(self, edge):
            old_edge = self.find_edge(colors)
            self.white_index = old_edge.pop(colors.index('W'))
            self.color_index = old_edge[0]        
        
        colors = ''.join(rubix_key.to_colors(edge))
        col = colors.replace('W', '')         
        col_face = self.get_target_face(col)      
        update(self, edge)      
            
        if self.color_index[0] == 'D':
            while self.white_index[0] != col_face:
                self.turn('D')
                update(self, edge)
            self.turn(col_face, 1)
            update(self, edge)
        
        if self.color_index[0] == 'U': 
            self.turn(self.white_index[0])
            update(self, edge)
            
        if self.white_index[0] == 'U':
            self.turn(self.color_index[0])
            update(self, edge)
            
        if self.white_index[1] in '46' and self.color_index[0] not in col_face:
            face_to_turn = self.color_index[0]
            if self.color_index[1] == '4':
                self.turn(face_to_turn, -1)
                self.turn('D')
                self.turn(face_to_turn, 1)
            else:
                self.turn(face_to_turn, 1)
                self.turn('D', -1)
                self.turn(face_to_turn, -1)
            update(self, edge)
            
        if self.white_index[0] == 'D':
            while self.color_index[0] != col_face:
                self.turn('D')
                update(self, edge)
            self.turn(col_face)
            self.turn(col_face)
            return
            
        if self.color_index[1] in '46':
            if self.color_index[1] == '4':
                self.turn(col_face, 1)
            else:
                self.turn(col_face, -1)
            return   
    
    def solve_white_corners(self, corner):
        

        def update(self, corner):
            old_corner = self.find_corner(colors)
            self.white_index = old_corner[colors.index('W')]
            self.color_index_a = old_corner[colors.index(col_a)]
            self.color_index_b = old_corner[colors.index(col_b)]
        
        remove_digits = str.maketrans('', '', digits)
        colors = ''.join(rubix_key.to_colors(corner)).translate(remove_digits)
        
        if 'R' in colors:
            if 'G' in colors:
                col_a = 'R'
                col_b = 'G'
            else:
                col_a = 'B'
                col_b = 'R'
        else:
            if 'B' in colors:
                col_a = 'O'
                col_b = 'B'
            else:
                col_a = 'G'
                col_b = 'O'
                        
        col_face_a = self.get_target_face(col_a)
        col_face_b = self.get_target_face(col_b)   
        update(self, corner)   
        
        #Scenarios
        #1: white on bottom face
        #2: white in top face but wrong position
        #2: white in a 1 spot on horizontal faces
        #3: white in a 3 spot on horizontal faces
        #3: white in a 7 spot on horizontal faces incorrect spot
        #4: white in a 9 spot on horizontal faces incorrect spot
        #3: white in a 7 spot on horizontal faces correct spot
        #4: white in a 9 spot on horizontal faces correct spot
        
        if self.white_index[0] == 'D':
            while self.color_index_a[0] != col_face_b:
                self.turn('D',  1)
                update(self, corner)
            self.turn(col_face_a, -1)
            self.turn('D', -1)
            self.turn('D', -1)
            self.turn(col_face_a, 1)
            self.turn('D',  1)
            update(self, corner)
            
        if self.white_index[0] == 'U':
            self.turn(self.color_index_a[0], -1)
            self.turn('D', -1)
            self.turn(self.color_index_a[0], 1)
            update(self, corner)
            
        if self.white_index[1] == '1':
            self.turn(self.white_index[0], -1)
            self.turn('D', -1)
            self.turn(self.white_index[0], 1)
            update(self, corner)
            
        if self.white_index[1] == '3':
            self.turn(self.white_index[0], 1)
            self.turn('D', 1)
            self.turn(self.white_index[0], -1)
            update(self, corner)
            
        if self.white_index[1] == '7': 
            while self.color_index_b != col_face_b + '9':
                self.turn('D',  1)
                update(self, corner)
        
        if self.white_index[1] == '9': 
            while self.color_index_a != col_face_a + '7':
                self.turn('D',  1)
                update(self, corner)
            update(self, corner)
        
        if self.color_index_b == col_face_b + '9':
            self.turn(col_face_a, -1)
            self.turn('D', -1)
            self.turn(col_face_a, 1)
            return
            
        if self.color_index_a == col_face_a + '7':
            self.turn('D', -1)
            self.turn(col_face_a, -1)
            self.turn('D', 1)
            self.turn(col_face_a, 1)
            return

    def solve_horizontal_edges(self, edge):
        def update(self, edge):
            old_edge = self.find_edge(colors)
            self.color_index_a = old_edge[colors.index(col_a)]
            self.color_index_b = old_edge[colors.index(col_b)]  
            
        def turn_seq(self, side, face):
            faces = ('F', 'R', 'B', 'L')
            if (faces.index(face) == faces.index(side) - 1) or \
               (faces.index(face) == faces.index(side) + 3):
                   d = 1
            else: d = -1
            self.turn('D', -1 * d)
            self.turn(side,   -1 * d)
            self.turn('D',  1 * d)
            self.turn(side,   1 * d)
            self.turn('D',  1 * d)
            self.turn(face,  1 * d)
            self.turn('D', -1 * d)
            self.turn(face, -1 * d)
            
        remove_digits = str.maketrans('', '', digits)
        colors = ''.join(rubix_key.to_colors(edge)).translate(remove_digits)
        if 'R' in colors:
            if 'B' in colors:
                col_a = 'R'
                col_b = 'B'
            else:
                col_a = 'G'
                col_b = 'R'
        else:
            if 'B' in colors:
                col_a = 'B'
                col_b = 'O'
            else:
                col_a = 'O'
                col_b = 'G' 
              
        col_face_a = self.get_target_face(col_a) 
        col_face_b = self.get_target_face(col_b) 
        update(self, edge)      
        
        #SCENARIOS
        #1: edge is in horizontal position but not correct one
        #2: edge in bottom layer not over corresponding color 
        #3: edge in bottom layer and over corresponding color
        
        if self.color_index_a[0] in 'FBLR' and self.color_index_a[1] in '46':
            side = self.color_index_a[0]
            face = self.color_index_b[0]
            turn_seq(self, side, face)
            update(self, edge)
            
        if self.color_index_a[0] != 'D': #not bottom face
            nonB_loc = self.color_index_a 
            targ_face = col_face_a
            non_targ_face = col_face_b
        else: 
            nonB_loc = self.color_index_b
            targ_face = col_face_b
            non_targ_face = col_face_a
        
        while nonB_loc[0] != targ_face:
            self.turn('D')
            update(self, edge)
            if self.color_index_a[0] != 'D': #not bottom face
                nonB_loc = self.color_index_a 
                targ_face = col_face_a
                non_targ_face = col_face_b
            else: 
                nonB_loc = self.color_index_b
                targ_face = col_face_b
                non_targ_face = col_face_a
        
        face = targ_face
        side = non_targ_face
        turn_seq(self, side, face)
        update(self, edge)
    
    def solve_yellow_cross(self):
        def get_yellows(self):
            yellow_edges = []
            for index in ['D2', 'D4', 'D6', 'D8']:
                if self.to_colors([index]) == ['Y']:
                    yellow_edges.append(index)
            return yellow_edges
            
        #Scenarios
        #1: no yellow edges
        #2: yellow stripe perpendicular
        #3: yellow stripe parallel
        #4: yellow right angle not aligned
        #5: yellow right angle aligned
            
        yellow_edges = get_yellows(self)
        if len(yellow_edges) == 0:
            self.turn('F',  1)
            self.turn('D',  1)
            self.turn('L',  1)
            self.turn('D', -1)
            self.turn('L', -1)
            self.turn('F', -1)
            yellow_edges = get_yellows(self)
            
        if 'D2' in yellow_edges and 'D8' in yellow_edges and 'D4' not in yellow_edges:
            self.turn('D',  1)
            yellow_edges = get_yellows(self)
            
        if 'D4' in yellow_edges and 'D6' in yellow_edges and 'D2' not in yellow_edges:
            self.turn('F',  1)
            self.turn('L',  1)
            self.turn('D',  1)
            self.turn('L', -1)
            self.turn('D', -1)
            self.turn('F', -1)
            return
        if 'D2' not in yellow_edges or 'D4' not in yellow_edges:
            while 'D2' not in yellow_edges or 'D4' not in yellow_edges:
                self.turn('D', 1)
                yellow_edges = get_yellows(self)
                
        if len(yellow_edges) != 4:
            self.turn('F',  1)
            self.turn('D',  1)
            self.turn('L',  1)
            self.turn('D', -1)
            self.turn('L', -1)
            self.turn('F', -1)
        return
        
    def solve_yellow_corners(self):
        def get_yellows(self):
            yellow_corners = []
            for index in ['D1', 'D3', 'D7', 'D9']:
                if self.to_colors([index]) == ['Y']:
                    yellow_corners.append(index)
            return yellow_corners
            
        def turn_seq(self):
            self.turn('L', 1)
            self.turn('D', 1)
            self.turn('L', -1)
            self.turn('D', 1)
            self.turn('L', 1)
            self.turn('D', 1)
            self.turn('D', 1)
            self.turn('L', -1)
            
        #Scenarios
        #1: no yellow corners, not in position
        #2: one yellow corner, not in position
        #3: more than one yellow corner, not in position
        while len(get_yellows(self)) != 4:
            yellow_corners = get_yellows(self)
            
            if len(yellow_corners) == 0:
                while self.to_colors(['R7']) != ['Y']:
                    self.turn('D', 1)
                turn_seq(self)
                continue
            
            if len(yellow_corners) == 1:
                while self.to_colors(['D3']) != ['Y']:
                    self.turn('D', 1)
                turn_seq(self)
                continue
            
            if len(yellow_corners) > 1:
                while self.to_colors(['F9']) != ['Y']:
                    self.turn('D', 1)
                turn_seq(self)
                continue
        return
    
    def solve_final_corners(self):
        def turn_seq(self, F, B, L, D):
            self.turn(L, -1)
            self.turn(F,  1)
            self.turn(L, -1)
            self.turn(B,  1)
            self.turn(B,  1)
            self.turn(L,  1)
            self.turn(F, -1)
            self.turn(L, -1)
            self.turn(B,  1)
            self.turn(B,  1)
            self.turn(L,  1)
            self.turn(L,  1)
            self.turn(D, -1)
        def get_correct_corners(self):
            corners = (('D1', 'L9', 'F7'), ('D3', 'F9', 'R7'),
                       ('D7', 'B9', 'L7'), ('D9', 'R9', 'B7'))
            correct_corners = []
            for corner in corners:
                if self.to_colors(corner) == rubix_key.to_colors(corner):
                    correct_corners.append(corner[0][1]) #only append yellow tile's position
            return correct_corners
            
    #Scenarios
    #1: two corners diagonal to eachother 
    #2: two adjacent corners
            
        correct_corners = get_correct_corners(self)
        
        if ('1' in correct_corners and '9' in correct_corners) or \
           ('3' in correct_corners and '7' in correct_corners):
           turn_seq(self, 'F', 'B', 'L', 'D')
           correct_corners = get_correct_corners(self)
        
        if len(correct_corners) == 4:
            return
        
        while self.to_colors(['B7']) != self.to_colors(['B9']):
            self.turn('D', 1)
        turn_seq(self, 'F', 'B', 'L', 'D')
        
        while self.to_colors(['F9']) != ['R']:
            self.turn('D')
        return
    
    def solve_final_edges(self):
        def turn_seq(self, F, L, R, U, d):
            self.turn(F,  1)
            self.turn(F,  1)
            self.turn(U,  1 * d)
            self.turn(L,  1)
            self.turn(R, -1)
            self.turn(F,  1)
            self.turn(F,  1)
            self.turn(L, -1)
            self.turn(R,  1)
            self.turn(U,  1 * d)
            self.turn(F,  1)
            self.turn(F,  1)
            
        def get_correct_edge(self, edges):
            for edge in edges:
                if self.to_colors(edge) == rubix_key.to_colors(edge):
                    return edge
            return 0 
            
        #Scenarios:
        #1: no correct edges
        #2: one correct edge, must turn clockwise
        #3: one correct edge, must turn counter clockwise
        edges = (('F8', 'D2'), ('R8', 'D6'), ('B8', 'D8'), ('L8', 'D4'))
        correct_edge = get_correct_edge(self, edges)
        
        if correct_edge == 0:
            turn_seq(self, 'F', 'R', 'L', 'D', 1)
            correct_edge = get_correct_edge(self, edges)
            
        if self.to_colors(['F8']) == ['G'] or self.to_colors(['B8']) == ['B']: d = -1   #check direction         
        else: d = 1
            
        F = opposite_side[correct_edge[0][0]]
        
        R_index = edges.index(correct_edge) - 1
        if R_index < 0: R_index = 3
        R = edges[R_index][0][0]
        
        L_index = edges.index(correct_edge) + 1
        if L_index > 3: L_index = 0
        L = edges[L_index][0][0]

        turn_seq(self, F, R, L, 'D', d)
        return

    def find_edge(self, colors):
        '''
        finds location of edge based on colors 
        and returns edge in order that colors appear
        ex: 'WG' -> ('F6', 'R4')
        if W on F6 and G on R4
        '''
        edges = (('F6', 'R4'), ('R6', 'B4'), ('B6', 'L4'), ('L6', 'F4'), 
                 ('F2', 'U8'), ('R2', 'U6'), ('B2', 'U2'), ('L2', 'U4'),
                 ('F8', 'D2'), ('R8', 'D6'), ('B8', 'D8'), ('L8', 'D4'))

        for edge in edges:
            edge_cols = self.to_colors(edge)
            if colors[0] in edge_cols and colors[1] in edge_cols:
                found_edge = []
                found_edge.append(edge[edge_cols.index(colors[0])])
                found_edge.append(edge[edge_cols.index(colors[1])])
                return found_edge
                    
    def find_corner(self, colors):
        '''
        finds location of corner based on colors 
        and returns corner in order that colors appear
        ex: 'WGR' -> 
        if 
        '''
        corners = (('U1', 'L1', 'B3'), ('U3', 'B1', 'R3'),
                   ('U7', 'F1', 'L3'), ('U9', 'R1', 'F3'),
                   ('D1', 'L9', 'F7'), ('D3', 'F9', 'R7'),
                   ('D7', 'B9', 'L7'), ('D9', 'R9', 'B7'))

        for corner in corners:
            cor_cols = self.to_colors(corner)
            if colors[0] in cor_cols and colors[1] in cor_cols and colors[2] in cor_cols:
                found_corner = []
                found_corner.append(corner[cor_cols.index(colors[0])])
                found_corner.append(corner[cor_cols.index(colors[1])])
                found_corner.append(corner[cor_cols.index(colors[2])])
                return found_corner
        
    def to_colors(self, tiles):
        '''
        takes tiles as list of 'side, number'
        and returns colors at positions
        ex: ['U7', 'R3'] -> ['W', 'Y']
        '''
        indices = {1: (1, -1),  2: (1, 0),  3:(1, 1), 
                   4: (0, -1),  5: (0, 0),  6:(0, 1), 
                   7: (-1, -1), 8: (-1, 0), 9:(-1, 1)}
         
        colors = []
        for tile in tiles:
            side = tile[0]
            index = indices[int(tile[1])]
            colors.append(self.cube[side].loc[index])
            
        return colors
    
    def get_target_face(self, color):
        '''
        return the face that corresponds with a color
        based on which face the color will be on when
        the cube is completed
        '''
        faces = 'FBLRUP'
        colors = 'ROGBWY'
        return faces[colors.index(color)]
    
    def prune_directions(self, recurse_num = 3):
        '''
        optimize directions slightly by
        -replacing triple turns with single turn in opposite direction
        -switching orders of rotations which occur on opposite faces 
         to search for more triple turn optimizeations
        -removing canceling out turns
        '''
        dirs = ' '.join(self.directions)
        
        for side in SIDES: #replace triple turns with single turn other direction
            repeat = 3 * (side + '+ ')
            dirs = dirs.replace(repeat, side + '- ')
            repeat = 3 * (side + '- ')
            dirs = dirs.replace(repeat, side + '+ ')
  
        for side in SIDES:#remove self-cancling turns
            cancel = side + '+ ' + side + '- '
            dirs = dirs.replace(cancel, "")
            cancel = side + '- ' + side + '+ '
            dirs = dirs.replace(cancel, "")
        
        self.directions = dirs.split()
        
        for step in range(0, len(self.directions) - 1): #shuffle things up
            if self.directions[step][0] ==  opposite_side[self.directions[step+1][0]]:
                self.directions[step], self.directions[step+1] = self.directions[step+1], self.directions[step]
        
        if recurse_num > 0:
            self.prune_directions(recurse_num-1)
    
    def randomize(self, num_turns = 500):
        '''
        randomize cube
        '''
        signs = [-1, 1]
        for i in range(num_turns):
            self.turn(SIDES[random.randint(0, 5)], signs[random.randint(0, 1)])

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

def import_cube(interact = False):
    if interact:
        user_in = 'x'
        while user_in.lower() not in ['h', 'y']:
            print('Cube face images uploaded?')
            user_in = input('[H]elp [Y]es')
        if user_in.lower() == 'h':
            print('photograph the cube (using square-shaped photos, if possible)')
            print('in the order of faces with center pieces of')
            print('red, white, yellow, blue, orange, green, respectively,' )
            print('with orientation of the white-centered face such that the bottom edge')
            print('is shared with the red face and orientation of the yellow_centered face')
            print('such that the top edge is shared with the red face, and')
            print('orientation of the remaining faces such that the top edge is')
            print('shared with the white face.')
            print('Then upload these pictures to the pictures folder in the rubix folder')
            print('of Google Drive.')
            print()
            input('Press enter to continue')    
    
    while os.getcwd() != 'C:\\':
        os.chdir("..")
    
    os.chdir('C:\\Users\\Gabe Madonna\\Google Drive\\Code_CAD\\Rubix_solver\\pictures')
    face_files = os.listdir()
    face_images = list(map(cv2.imread, face_files))
    ref_pixels = list(map(graphics.get_av_pixel, face_images))
    ref_dict = dict(zip(COLORS, ref_pixels))
    rubix_cube = list(map(lambda img: graphics.get_color_matrix(img, ref_dict = ref_dict), face_images))
    print('valid cube:', cube_is_valid(rubix_cube))
    rubix_cube = dict(zip(SIDES, rubix_cube))
    rubix_cube = dict_to_cube(rubix_cube)
    return rubix_cube

def dict_to_cube(cube_dict):
    '''
    takes in cube dictionary and returns a Cube object
    '''
    for face in cube_dict:
        cube_dict[face] = pd.DataFrame(cube_dict[face], index = [1, 0, -1], columns = [-1, 0, 1])
    return Cube(cube_dict)

def gen_rubix_key(with_nums = False):
    '''
    generates cube object of completed rubix cube
    with or withour numbers
    '''
    if with_nums:     
        u_face = np.array(list("W" + str(i) for i in range(1, 10))).reshape(3, 3)
        d_face = np.array(list("Y" + str(i) for i in range(1, 10))).reshape(3, 3)
        l_face = np.array(list("G" + str(i) for i in range(1, 10))).reshape(3, 3)
        r_face = np.array(list("B" + str(i) for i in range(1, 10))).reshape(3, 3)
        f_face = np.array(list("R" + str(i) for i in range(1, 10))).reshape(3, 3)
        b_face = np.array(list("O" + str(i) for i in range(1, 10))).reshape(3, 3)
        
    else:
        u_face = np.array(9 * ['W']).reshape(3, 3)
        d_face = np.array(9 * ['Y']).reshape(3, 3)
        l_face = np.array(9 * ['G']).reshape(3, 3)
        r_face = np.array(9 * ['B']).reshape(3, 3)
        f_face = np.array(9 * ['R']).reshape(3, 3)
        b_face = np.array(9 * ['O']).reshape(3, 3)
    
    rubix_key = {"U":u_face, "D":d_face, "L":l_face, "R":r_face, "F":f_face, "B":b_face}
    rubix_key = dict_to_cube(rubix_key)
    return rubix_key

rubix_key = gen_rubix_key()