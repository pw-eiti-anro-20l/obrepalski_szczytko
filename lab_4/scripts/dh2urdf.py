#! /usr/bin/python

import json
from tf.transformations import *

x_axis, y_axis, z_axis = (1, 0, 0), (0, 1, 0), (0, 0, 1)

def convertToFile():

    with open('../yaml/dh.json', 'r') as file:

        parameters = json.loads(file.read())

    with open('../yaml/urdf.yaml', 'w') as file:

        for key in parameters.keys():

            a, d, alpha, theta = parameters[key]
            a=float(a)
            d=float(d)
            alpha=float(alpha)
            theta=float(theta)

            tz = translation_matrix((0, 0, d))
            rz = rotation_matrix(theta, z_axis)
            tx = translation_matrix((a, 0, 0))
            rx = rotation_matrix(alpha, x_axis)

            matrix = concatenate_matrices(tz, rz, tx, rx)

            rpy = euler_from_matrix(matrix)
            xyz = translation_from_matrix(matrix)

            file.write(key + ":\n")
            file.write("  j_xyz: {} {} {}\n".format(*xyz))
            file.write("  j_rpy: {} {} {}\n".format(*rpy))
            file.write("  l_xyz: {} 0 0\n".format(xyz[0] / 2))
            file.write("  l_rpy: 0 0 0\n")
            file.write("  l_len: {}\n".format(a))
if __name__ == '__main__':

    convertToFile()
    print "URDF WAS MADE"
