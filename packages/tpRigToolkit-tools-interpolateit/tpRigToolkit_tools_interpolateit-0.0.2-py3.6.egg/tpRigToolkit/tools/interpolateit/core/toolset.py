#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tool to store/blend interpolate states of objects
"""

from __future__ import print_function, division, absolute_import

from tpDcc.libs.qt.widgets import toolset


class InterpolateItToolset(toolset.ToolsetWidget):
    def __init__(self, *args, **kwargs):
        super(InterpolateItToolset, self).__init__(*args, **kwargs)

    def contents(self):

        from tpRigToolkit.tools.interpolateit.core import model, view, controller

        interpolate_it_model = model.InterpolateItModel()
        interpolate_it_controller = controller.InterpolateItController(client=self._client, model=interpolate_it_model)
        interpolate_it_view = view.InterpolateItView(
            model=interpolate_it_model, controller=interpolate_it_controller, parent=self)

        return [interpolate_it_view]
