#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains tool definition for tpRigToolkit-tools-jointorient
"""

from __future__ import print_function, division, absolute_import

import os
import sys
import logging

from tpDcc.core import tool

from tpRigToolkit.tools.jointorient.core import consts, client, toolset

LOGGER = logging.getLogger(consts.TOOL_ID)


class JointOrientTool(tool.DccTool, object):

    ID = consts.TOOL_ID
    CLIENT_CLASS = client.JointOrientClient
    TOOLSET_CLASS = toolset.JointOrientToolset

    def __init__(self, *args, **kwargs):
        super(JointOrientTool, self).__init__(*args, **kwargs)

    @classmethod
    def config_dict(cls, file_name=None):
        base_tool_config = tool.DccTool.config_dict(file_name=file_name)
        tool_config = {
            'name': 'Joint Orient',
            'id': JointOrientTool.ID,
            'supported_dccs': {'maya': ['2017', '2018', '2019', '2020']},
            'logo': 'jointorient',
            'icon': 'jointorient',
            'tooltip': ' Tool to orient joints quickly',
            'tags': ['tpRigToolkit', 'joint', 'orient'],
            'is_checkable': False,
            'is_checked': False,
            'menu_ui': {'label': 'Joint Orient', 'load_on_startup': False, 'color': '', 'background_color': ''},
            'size': [430, 660],

        }
        base_tool_config.update(tool_config)

        return base_tool_config

    def launch(self, *args, **kwargs):
        return self.launch_frameless(*args, **kwargs)


if __name__ == '__main__':
    import tpRigToolkit.loader
    from tpDcc.managers import tools

    tool_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
    if tool_path not in sys.path:
        sys.path.append(tool_path)

    tpRigToolkit.loader.init()
    tools.ToolsManager().launch_tool_by_id(consts.TOOL_ID)
