#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions and classes related with Maya API maths
"""

from __future__ import print_function, division, absolute_import

import maya.cmds
import maya.api.OpenMaya

from tpDcc.dccs.maya import api


def magnitude(vector=(0, 0, 0)):
    """
    Returns the magnitude (length) or a given vector
    :param vector:  tuple, vector to return the length of
    :return: float
    """

    return maya.api.OpenMaya.MVector(vector[0], vector[1], vector[2]).length()


def get_axis_vector(transform, axis_vector):
    """
    Returns the vector matrix product
    If you give a vector [1, 0, 0], it will return the transform's X point
    If you give a vector [0, 1, 0], it will return the transform's Y point
    If you give a vector [0, 0, 1], it will return the transform's Z point
    :param transform: str, name of a transforms. Its matrix will be checked
    :param axis_vector: list<int>, A vector, X = [1,0,0], Y = [0,1,0], Z = [0,0,1]
    :return: list<int>, the result of multiplying the vector by the matrix
    Useful to get an axis in relation to the matrix
    """

    xform = api.TransformFunction(transform)
    new_vector = xform.get_vector_matrix_product(axis_vector)

    return new_vector


def normalize_vector(vector=(0, 0, 0)):
    """
    Returns normalized version of the input vector
    :param vector: tuple, vector to normalize
    :return: tuple
    """

    normal = maya.api.OpenMaya.MVector(vector[0], vector[1], vector[2]).normal()

    return normal.x, normal.y, normal.z


def dot_product(vector1=(0.0, 0.0, 0.0), vector2=(0.0, 0.0, 0.0)):
    """
    Returns the dot product (inner product) of two given vectors
    :param vector1: tuple, first vector for the dot product operation
    :param vector2: tuple, second vector for the dot product operation
    :return: float
    """

    vec1 = maya.api.OpenMaya.MVector(vector1[0], vector1[1], vector1[2])
    vec2 = maya.api.OpenMaya.MVector(vector2[0], vector2[1], vector2[2])

    return vec1 * vec2


def cross_product(vector1=(0.0, 0.0, 0.0), vector2=(0.0, 0.0, 0.0)):
    """
    Returns the cross product of two given vectors
    :param vector1: tuple, first vector for the dot product operation
    :param vector2: tuple, second vector for the dot product operation
    :return: tuple
    """

    vec1 = maya.api.OpenMaya.MVector(vector1[0], vector1[1], vector1[2])
    vec2 = maya.api.OpenMaya.MVector(vector2[0], vector2[1], vector2[2])
    cross_product = vec1 ^ vec2

    return cross_product.x, cross_product.y, cross_product.z


def distance_between(point1=[0.0, 0.0, 0.0], point2=[0.0, 0.0, 0.0]):
    """
    Returns the distance between two given points
    :param point1: tuple, start point of the distance calculation
    :param point2: tuple, end point of the distance calculation
    :return: float
    """

    pnt1 = maya.api.OpenMaya.MVector(point1[0], point1[1], point1[2])
    pnt2 = maya.api.OpenMaya.MVector(point2[0], point2[1], point2[2])

    return maya.api.OpenMaya.MVector(pnt1 - pnt2).length()


def offset_vector(point1=[0.0, 0.0, 0.0], point2=[0.0, 0.0, 0.0]):
    """
    Returns the offset vector between point1 and point2
    :param point1: tuple, start point of the offset calculation
    :param point2: tuple, end point of the offset calculation
    :return: tuple
    """

    pnt1 = maya.api.OpenMaya.MVector(point1[0], point1[1], point1[2])
    pnt2 = maya.api.OpenMaya.MVector(point2[0], point2[1], point2[2])
    vec = pnt2 - pnt1

    return vec.x, vec.y, vec.z


def closest_point_on_line(pnt, line1, line2, clamp_segment=False):
    """
    Find the closest point (to a given position) on the line given by the given inputs
    :param pnt: tuple, we will try to find the closes line point from this position
    :param line1: tuple, start point of line
    :param line2: tuple, end point of line
    :param clamp_segment: bool, Whether to return clamped value or not
    :return: tuple
    """

    pnt_offset = offset_vector(line1, pnt)
    line_offset = offset_vector(line1, line2)

    # Vector comparison
    dot = dot_product(pnt_offset, line_offset)

    if clamp_segment:
        if dot < 0.0:
            return line1
        if dot > 1.0:
            return line2

    # Project Vector
    return [line1[0] + (line_offset[0] * dot), line1[1] + (line_offset[1] * dot), line1[2] + (line_offset[2] * dot)]


def inverse_distance_weight_3d(point_array, sample_point):
    """
    Returns the inverse distance weight for a given sample point given an array of scalar values
    :param point_array: variant, tuple || list, point array to calculate weights from
    :param sample_point: variant, tuple || list, sample point to calculate weights for
    :return: float
    """

    dst_array = list()
    total_inv_dst = 0.0

    for i in range(len(point_array)):
        dst = distance_between(sample_point, point_array[i])
        # Check zero distance
        if dst < 0.00001:
            dst = 0.00001

        dst_array.append(dst)
        total_inv_dst += 1.0 / dst

    # Normalize value weights
    weight_array = [(1.0 / d) / total_inv_dst for d in dst_array]

    return weight_array


def multiply_matrix(matrix4x4_list1, matrix4x4_list2):
    """
    matrix1 and matrix2 are just the list of numbers of a 4x4 matrix
    (like the ones returned by cmds.getAttr('transform.worldMatrix) for example
    :param matrix4x4_list1:
    :param matrix4x4_list2:
    :return: OpenMaya.MMatrix
    """

    mat1 = maya.api.OpenMaya.MMatrix(matrix4x4_list1)
    mat2 = maya.api.OpenMaya.MMatrix(matrix4x4_list2)

    return mat1 * mat2


def distance_between_nodes(source_node=None, target_node=None):
    """
    Returns the distance between 2 given nodes
    :param str source_node: first node to start measuring distance from. If not given, first selected node will be used.
    :param str target_node: second node to end measuring distance to. If not given, second selected node will be used.
    :return: distance between 2 nodes.
    :rtype: float
    """

    if source_node is None or target_node is None:
        sel = maya.cmds.ls(sl=True, type='transform')
        if len(sel) != 2:
            return 0
        source_node, target_node = sel

    source_pos = maya.api.OpenMaya.MPoint(*maya.cmds.xform(source_node, query=True, worldSpace=True, translation=True))
    target_pos = maya.api.OpenMaya.MPoint(*maya.cmds.xform(target_node, query=True, worldSpace=True, translation=True))

    return source_pos.distanceTo(target_pos)


def direction_vector_between_nodes(source_node=None, target_node=None):
    """
    Returns the direction vector between 2 given nodes
    :param str source_node: first node to start getting direction. If not given, first selected node will be used.
    :param str target_node: second node to end getting direction. If not given, second selected node will be used.
    :return: direction vector between 2 nodes.
    :rtype: OpenMaya.MVector
    """

    if source_node is None or target_node is None:
        sel = maya.cmds.ls(sl=True, type='transform')
        if len(sel) != 2:
            return 0
        source_node, target_node = sel

    source_pos = maya.api.OpenMaya.MPoint(*maya.cmds.xform(source_node, query=True, worldSpace=True, translation=True))
    target_pos = maya.api.OpenMaya.MPoint(*maya.cmds.xform(target_node, query=True, worldSpace=True, translation=True))

    return target_pos - source_pos
