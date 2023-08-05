"""
********************************************************************************
robots
********************************************************************************

.. currentmodule:: compas.robots


Model
=====

.. inheritance-diagram:: RobotModel Joint Link ToolModel
    :parts: 1

The root of the model is the :class:`RobotModel` class, which
describes a robot consisting of a set of link elements, and a set of joint
elements connecting the links together.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    RobotModel
    Joint
    Link
    ToolModel


Geometric description
=====================

.. inheritance-diagram:: Origin Geometry Box Cylinder Sphere Capsule MeshDescriptor Material Texture Color
    :parts: 1

The robot itself as well as its links can be geometrically described
using the following classes.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Origin
    Geometry
    Box
    Cylinder
    Sphere
    Capsule
    MeshDescriptor
    Material
    Texture
    Color


Link
====

.. inheritance-diagram:: Visual Collision Inertial Mass Inertia
    :parts: 1

The link is described as a rigid body with inertial, visual and collision values.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Visual
    Collision
    Inertial
    Mass
    Inertia


Joint
=====

.. inheritance-diagram:: ParentLink ChildLink Calibration Dynamics Limit Axis Mimic SafetyController
    :parts: 1

The joint describes the kinematics and dynamics of the robot's joint.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ParentLink
    ChildLink
    Calibration
    Dynamics
    Limit
    Axis
    Mimic
    SafetyController


Resources
=========

.. inheritance-diagram:: AbstractMeshLoader DefaultMeshLoader GithubPackageMeshLoader LocalPackageMeshLoader
    :parts: 1

Model descriptions usually do not contain embedded geometry information but only
descriptions, filenames or URLs for externally hosted resources.
For that purpose, this package provides various loader classes that help automate
the processing of these resources.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    AbstractMeshLoader
    DefaultMeshLoader
    GithubPackageMeshLoader
    LocalPackageMeshLoader

"""
from __future__ import absolute_import

from .model import (
    Axis,
    Box,
    Calibration,
    Capsule,
    ChildLink,
    Collision,
    Color,
    Cylinder,
    Dynamics,
    Geometry,
    Inertia,
    Inertial,
    Joint,
    Limit,
    Link,
    Mass,
    Material,
    MeshDescriptor,
    Mimic,
    Origin,
    ParentLink,
    RobotModel,
    SafetyController,
    Sphere,
    Texture,
    ToolModel,
    Visual
)
from .resources import (
    AbstractMeshLoader,
    DefaultMeshLoader,
    GithubPackageMeshLoader,
    LocalPackageMeshLoader
)

__all__ = [
    'Geometry',
    'Box',
    'Cylinder',
    'Sphere',
    'Capsule',
    'MeshDescriptor',
    'Color',
    'Texture',
    'Material',
    'Origin',

    'Joint',
    'ParentLink',
    'ChildLink',
    'Calibration',
    'Dynamics',
    'Limit',
    'Axis',
    'Mimic',
    'SafetyController',

    'Link',
    'Inertial',
    'Visual',
    'Collision',
    'Mass',
    'Inertia',

    'RobotModel',
    'ToolModel',

    'AbstractMeshLoader',
    'DefaultMeshLoader',
    'LocalPackageMeshLoader',
    'GithubPackageMeshLoader'
]
