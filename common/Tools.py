#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Name: Tools.py
Author: [Author]
Email: [Author Email]
Creation Date: 2025-03-25
Last Modified Date: 2025-03-25
Description: This module initializes and provides access to various tools.
Version: [Version]
License: [License]
"""

from tools.MajorPlanTool import MajorPlanTool
from tools.AnnualScoresTool import AnnualScoresTool

class CustomTools:
    def __init__(self):
        """
        Initializes instances of MajorPlanTool and AnnualScoresTool,
        and stores them in a list for easy access and management.
        """
        major_plan = MajorPlanTool()
        annual_scores = AnnualScoresTool()
        
        self.tools = [
            major_plan.tool,
            annual_scores.tool
        ]

    def initialize(self):
        """
        Returns a list of initialized tool instances.

        Returns:
        - list: A list containing initialized tools [MajorPlanTool, AnnualScoresTool].
        """
        return self.tools