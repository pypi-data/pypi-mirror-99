#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains toolset definition for tpRigToolkit-tools-jointorient
"""

from __future__ import print_function, division, absolute_import

import logging


from tpDcc.libs.qt.widgets import toolset

LOGGER = logging.getLogger('tpRigToolkit-tools-jointorient')


class JointOrientToolset(toolset.ToolsetWidget, object):

    def __init__(self, *args, **kwargs):
        super(JointOrientToolset, self).__init__(*args, **kwargs)

    def contents(self):

        from tpRigToolkit.tools.jointorient.core import model, view, controller

        joint_orient_model = model.JointOrientModel()
        joint_orient_controller = controller.JointOrientController(client=self._client, model=joint_orient_model)
        joint_orient_view = view.JointOrientView(
            model=joint_orient_model, controller=joint_orient_controller, parent=self)

        return [joint_orient_view]
