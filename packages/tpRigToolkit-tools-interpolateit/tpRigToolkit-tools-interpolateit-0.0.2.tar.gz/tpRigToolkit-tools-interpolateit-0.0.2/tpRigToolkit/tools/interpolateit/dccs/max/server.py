#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains tpRigToolkit-tools-interpolateit server implementation for 3ds Max
"""

import logging

from pymxs import runtime as rt

from tpDcc import dcc
from tpDcc.core import server
from tpDcc.dccs.max.core import constants

LOGGER = logging.getLogger('tpRigToolkit-tools-interpolateit')


class InterpolateItServer(server.DccServer, object):

    PORT = 18231

    def _process_command(self, command_name, data_dict, reply_dict):
        if command_name == 'get_attributes_data_to_store':
            self.get_attributes_data_to_store(data_dict, reply_dict)
        elif command_name == 'reset_attributes':
            self.reset_attributes(data_dict, reply_dict)
        elif command_name == 'set_stored_attribute_value':
            self.set_stored_attribute_value(data_dict, reply_dict)
        else:
            super(InterpolateItServer, self)._process_command(command_name, data_dict, reply_dict)

    def get_attributes_data_to_store(self, data, reply):
        node = data['node']
        transform_attributes = data['transform_attributes']
        user_attributes = data['user_attributes']
        if not node:
            reply['msg'] = 'No note given to retrieve attributes to store of'
            reply['success'] = False
            return

        attributes_data = dict()

        if transform_attributes:
            xform_attribute_names = [
                constants.TRANSLATION_ATTR_NAME, constants.ROTATION_ATTR_NAME, constants.SCALE_ATTR_NAME]
            for xform in xform_attribute_names:
                xform_value = dcc.get_attribute_value(node, xform)
                if xform == constants.ROTATION_ATTR_NAME:
                    rotation_as_euler = rt.quatToEuler(xform_value)
                    xform_value = [rotation_as_euler.x, rotation_as_euler.y, rotation_as_euler.z]
                else:
                    xform_value = list(xform_value)
                for i, axis in enumerate(constants.AXES):
                    channel = '{}{}'.format(xform, axis.upper())
                    attributes_data[channel] = xform_value[i]
                    if dcc.is_attribute_locked(node, channel):
                        attributes_data[channel][i] = None

        if user_attributes:
            pass

        reply['result'] = attributes_data
        reply['success'] = True

    @dcc.undo_decorator()
    def reset_attributes(self, data, reply):
        # TODO: Add support for reset attributes
        # NOTE: In Max, we need to store extra data attribute when saving start values (store default values)
        reply['success'] = True

    def set_stored_attribute_value(self, data, reply):
        node = data['node']
        attribute_name = data['attribute_name']
        attribute_value = data['attribute_value']

        dcc.set_attribute_value(node, attribute_name, attribute_value)
        dcc.refresh_viewport()

        reply['success'] = True
