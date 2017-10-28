# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 22:39:55 2017

@author: Gabe Madonna
"""
import cube

if __name__ == '__main__':
    rubix_key = cube.gen_rubix_key(with_nums = False)
    rubix_cube = cube.import_cube(interact = False)
    print(rubix_cube)
    #test_cube = copy.deepcopy(rubix_key)
    #test_cube.randomize()
    #print(test_cube)
    rubix_cube.solve()
    print(rubix_cube.directions)
