#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains rig base control implementation
"""

import logging

from tpDcc import dcc
from tpDcc.libs.python import decorators

from tpRigToolkit.managers import names
from tpRigToolkit.libs.controlrig.core import controllib

logger = logging.getLogger('tpRigToolkit-core')


class _MetaRigControl(type):

    def __call__(self, *args, **kwargs):
        if dcc.client().is_maya():
            from tpRigToolkit.dccs.maya.core import control
            return type.__call__(control.MayaRigControl, *args, **kwargs)
        else:
            return type.__call__(BaseRigControl, *args, **kwargs)


class BaseRigControl(object):

    axis_map = {
        'X': 'XYZ',
        'Y': 'YXZ',
        'Z': 'ZYX'
    }

    def __init__(self, name, **kwargs):
        super(BaseRigControl, self).__init__()

        self._name = name or 'newCtrl'
        self._curve_type = kwargs.pop('control_type', '')
        self._controls_path = kwargs.pop('controls_path', '')
        self._naming_file = kwargs.pop('naming_file', '')
        self._name_rule = kwargs.pop('rule_name', '')
        self._name_data = kwargs.pop('name_data', dict())
        self._side = kwargs.pop('side', None)

        if self._naming_file:
            self._name = self.solve_name(self._name, unique_name=False)

        if not dcc.node_exists(self._name):
            self._create(**kwargs)

    def __repr__(self):
        return '{} | {}'.format(self.__class__.__name__, self._name)

    # =================================================================================================================
    # PROPERTIES
    # =================================================================================================================

    @property
    def name(self):
        return self._name

    @property
    def side(self):
        return self._side

    # =================================================================================================================
    # ABSTRACT
    # =================================================================================================================

    @decorators.abstractmethod
    def get_rgb_color(self, linear=True):
        """
        Returns the RGB color of the given control, looking in the first shape node
        :param linear: bool, Whether or not the RGB should be in linear space (matches viewport color)
        :return: tuple(float, float, float), new control color in float linear values (between 0.0 and 1.0)
        """

        return 1.0, 1.0, 1.0

    @decorators.abstractmethod
    def set_color(self, value):
        """
        Sets the color of the control shapes
        :param value: int or list, color defined by its RGB color or by its index
        """

        pass

    @decorators.abstractmethod
    def translate_cvs(self, x, y, z):
        """
        Translates control curve CVs in object space
        :param x: float
        :param y: float
        :param z: float
        """

        pass

    @decorators.abstractmethod
    def rotate_cvs(self, x, y, z):
        """
        Rotates control curve CVs in object space
        :param x: float
        :param y: float
        :param z: float
        """

        pass

    @decorators.abstractmethod
    def scale_cvs(self, x, y, z, use_pivot=True):
        """
        Scales control curve CVs in object space
        :param x: float
        :param y: float
        :param z: float
        :param use_pivot: bool
        """

        pass

    # =================================================================================================================
    # BASE
    # =================================================================================================================

    def get(self):
        """
        Returns name of the control
        :return: str
        """

        return self._name

    def get_top(self):
        """
        Returns top control (taking into account root and auto buffer groups)
        :return: str
        """

        # Used by DCCs that cannot store transform offset inside the "transform" node such as Maya

        return self.get()

    def has_root_buffer(self):
        """
        Returns whether or not control has a a root buffer
        :return: bool
        """

        # Used by DCCs that cannot store transform offset inside the "transform" node such as Maya

        pass

    def has_auto_buffer(self):
        """
        Returns whether or not control has a a root buffer
        :return: bool
        """

        # Used by DCCs that cannot store transform offset inside the "transform" node such as Maya

        pass

    def create_root(self, name=None, *args, **kwargs):
        """
        Creates a root buffer group above the control
        :return: str
        """

        # Used by DCCs that cannot store transform offset inside the "transform" node such as Maya

        pass

    def create_auto(self, name=None, *args, **kwargs):
        """
        Creates an auto buffer group above the control
        :return: str
        """

        # Used by DCCs that cannot store transform offset inside the "transform" node such as Maya

        pass

    def set_parent(self, parent, **kwargs):
        """
        Sets the parent of the control
        :param parent:
        """

        dcc.set_parent(self.get_top(), parent)

    def set_naming_file(self, naming_file, name_rule=None):
        """
        Sets the naming file and rule used to manage the nomenclature of the control
        :param naming_file: str
        :param name_rule: str
        :return:
        """

        self._naming_file = naming_file
        self._name_rule = name_rule

    def set_curve_type(self, type_name=None, keep_color=True, **kwargs):
        """
        Updates the curves of the control with the given control type
        :param type_name: str
        :param keep_color: bool
        """

        color = kwargs.get('color', None)
        control_size = kwargs.get('control_size', 1.0)
        auto_scale = kwargs.get('auto_scale', True)
        auto_scale = auto_scale if control_size is None else False
        axis = kwargs.pop('axis', None)
        if axis:
            kwargs['axis_order'] = self.axis_map.get(axis, None)
        if color:
            keep_color = False
        control_type = kwargs.pop('control_type', 'circle')
        kwargs['control_type'] = type_name or control_type
        kwargs['keep_color'] = keep_color
        kwargs['auto_scale'] = auto_scale
        kwargs['parent'] = self._name

        new_control = controllib.replace_control_curves(self._name, **kwargs)

        dcc.clear_selection()

        return new_control

    def solve_name(self, *args, **kwargs):
        """
        Solves the given name using stored control naming file and rule
        :param args:
        :param kwargs:
        :return:
        """

        kwargs['naming_file'] = self._naming_file
        kwargs['rule_name'] = self._name_rule
        node_id = kwargs.pop('id', None)
        if not node_id:
            node_id = self._name_data.pop('id', None)
        node_type = kwargs.pop('node_type', 'control')
        kwargs.update(self._name_data)

        solved_name = names.solve_name(node_type=node_type, id=node_id, *args, **kwargs)

        return solved_name

    def parse_name(self, name):
        """
        Parse a current solved name and return its different fields (metadata information)
        :param name: str
        :return: dict(str)
        """

        return names.parse_name(node_name=name, rule_name=self._name_rule, naming_file=self._naming_file)

    def match_translation(self, target):
        """
        Matches control translation to given target
        :param target:
        """

        dcc.match_translation(target, self.get_top())

    def match_rotation(self, target):
        """
        Matches control rotation to given target
        :param target:
        """

        dcc.match_rotation(target, self.get_top())

    def match_scale(self, target):
        """
        Matches control scale to given target
        :param target:
        """

        dcc.match_scale(target, self.get_top())

    def match_translation_rotation(self, target):
        """
        Matches control translation and scale to given target
        :param target:
        """

        dcc.match_translation_rotation(target, self.get_top())

    def match_transform(self, target):
        """
        Matches control translation, rotation and scale to given target
        :param target:
        """

        dcc.match_transform(target, self.get_top())

    def hide_translate_attributes(self):
        """
        Locks and hide translate attributes on the control
        """

        dcc.hide_translate_attributes(self.get())

    def hide_rotate_attributes(self):
        """
        Locks and hide rotate attributes on the control
        """

        dcc.hide_rotate_attributes(self.get())

    def hide_scale_attributes(self):
        """
        Locks and hide scale attributes on the control
        """

        dcc.hide_scale_attributes(self.get())

    def hide_visibility_attribute(self):
        """
        Locks and hide the visibility attribute on the control
        """

        dcc.hide_visibility_attribute(self.get())

    def hide_scale_and_visibility_attributes(self):
        """
        Locks and hide the visibility and scale attributes on the control
        """

        self.hide_scale_attributes()
        self.hide_visibility_attribute()

    def hide_keyable_attributes(self):
        """
        Locks and hide all keyable attributes on the control
        """

        dcc.hide_keyable_attributes(self.get())

    # =================================================================================================================
    # INTERNAL
    # =================================================================================================================

    def _get_name(self, *args, **kwargs):
        """
        Internal function that returns a proper name for elements of the rig control
        :param name: str
        :param node_type: str
        :return: str
        """

        name_data = self._name_data.copy()
        name_data.update(**kwargs)
        return names.solve_name(naming_file=self._naming_file, rule_name=self._name_rule, *args, **name_data)

    def _create(self, **kwargs):
        """
        Internal function that forces the creation of the control curve
        """

        return self.set_curve_type(type_name=self._curve_type, keep_color=False, **kwargs)


@decorators.add_metaclass(_MetaRigControl)
class RigControl(object):
    pass
