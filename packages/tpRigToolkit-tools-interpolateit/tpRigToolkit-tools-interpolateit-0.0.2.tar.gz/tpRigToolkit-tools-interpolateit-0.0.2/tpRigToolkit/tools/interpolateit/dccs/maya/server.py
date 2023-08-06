#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains tpRigToolkit-tools-interpolateit server implementation for Maya
"""

import logging

from tpDcc import dcc
from tpDcc.core import server
from tpDcc.dccs.maya.core import constants

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

        attributes_to_store = list()
        if transform_attributes:
            xform_attribute_names = [
                constants.TRANSLATION_ATTR_NAME, constants.ROTATION_ATTR_NAME, constants.SCALE_ATT_NAME]
            for xform in xform_attribute_names:
                for axis in constants.AXES:
                    channel = '{}{}'.format(xform, axis.upper())
                    if dcc.is_attribute_locked(node, channel):
                        continue
                    attributes_to_store.append(channel)

        if user_attributes:
            for attr in dcc.list_user_attributes(node):
                attr_name = dcc.node_attribute_name(attr)
                if dcc.get_attribute_type(node, attr_name) in ('double', 'int'):
                    continue
                if dcc.is_attribute_locked(node, attr_name):
                    continue
                attributes_to_store.append(attr_name)

        for attr in attributes_to_store:
            attributes_data[attr] = dcc.get_attribute_value(node, attr)

        reply['result'] = attributes_data
        reply['success'] = True

    @dcc.undo_decorator()
    def reset_attributes(self, data, reply):
        node = data['node']
        attributes_dict = data['attributes_dict']
        if not node or not attributes_dict:
            reply['msg'] = 'Impossible to reset node "{}" attributes!'.format(node)
            reply['success'] = False
            return

        for attr_name, _ in attributes_dict.items():
            default_value = dcc.attribute_default_value(node, attr_name)
            dcc.set_attribute_value(node, attr_name, default_value)

        reply['success'] = True

    def set_stored_attribute_value(self, data, reply):
        node = data['node']
        attribute_name = data['attribute_name']
        attribute_value = data['attribute_value']

        dcc.set_attribute_value(node, attribute_name, attribute_value)

        reply['success'] = True
