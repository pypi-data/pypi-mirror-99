# IBM Confidential - OCO Source Materials
# (C) Copyright IBM Corp. 2020
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.

__author__ = "IBM"

import os

WINDOWS_OS_STR = "nt"
IS_WINDOWS_OS = (os.name == WINDOWS_OS_STR)

TOKEN_SOURCE_IP = "source_address"  # must be sync with feature.json
TOKEN_DESTINATION_IP = "destination_address"  # must be sync with feature.json

TOKEN_RANGE = "range"
TOKEN_RANGE_START = "range_start"
TOKEN_RANGE_STOP = "range_stop"
TOKEN_1D_HIST = "1D_hist"
TOKEN_2D_HIST = "2D_hist"
TOKEN_X_CUT_POINTS = "x_cut_points"
TOKEN_Y_CUT_POINTS = "y_cut_points"
TOKEN_COST = "cost"
TOKEN_OUT_OF_RANGE_COST = "out_of_range_cost"
TOKEN_AVG = "avg"
TOKEN_STD = "std"
TOKEN_MAX = "max"
TOKEN_MIN = "min"
TOKEN_ALLOWLIST = "allowlist"
TOKEN_HIST_LENGTH = "hist_length"
TOKEN_X_RANGE = "x_range"
TOKEN_Y_RANGE = "y_range"
#
TOKEN_DEFAULT = "Default"

