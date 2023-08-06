#!/usr/bin/env python
# Software License Agreement (GNU GPLv3  License)
#
# Copyright (c) 2020, Roland Jung (roland.jung@aau.at) , AAU, KPK, NAV
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Requirements:
# sudo pip install numpy pandas
########################################################################################################################
import os
import math
import pandas as pandas
import numpy as np
from cnspy_spatial_csv_formats.CSVFormatPose import CSVFormatPose


class CSV2DataFrame:
    format = CSVFormatPose.none
    data_frame = None
    data_loaded = False
    fn = None

    def __init__(self, filename=None, fmt=None):
        if filename is None:
            pass  # Do nothing.. data can be loaded later on!
        else:
            self.load_from_CSV(fn=filename, fmt=fmt)

    def subsample(self, step=None, num_max_points=None):
        if self.data_loaded:
            self.data_frame = CSV2DataFrame.subsample_DataFrame(self.data_frame, step=step,
                                                                num_max_points=num_max_points)
        else:
            print("CSV2DataFrame: data was not loaded!")

    def load_from_CSV(self, fn, fmt=None):
        if os.path.exists(fn):
            if fmt is not None:
                fmt_ = fmt
            elif fmt is None and self.format is not CSVFormatPose.none:
                fmt_ = self.format
            else:
                fmt_ = CSVFormatPose.identify_format(fn)

            if fmt_ is not CSVFormatPose.none:
                self.data_frame = CSV2DataFrame.load_CSV(filename=fn, fmt=fmt_)
                self.fn = fn
                self.data_loaded = True
                self.format = fmt_
                return True
        else:
            print("CSV2DataFrame.load_from_CSV(): file does not exist: {0}".format(fn))
        return False

    def save_to_CSV(self, fn, fmt=None):
        if fmt is None:
            fmt_ = self.format

        if self.data_loaded:
            CSV2DataFrame.save_CSV(data_frame=self.data_frame, filename=fn, fmt=fmt_)
        else:
            print("CSV2DataFrame: data was not loaded!")

    @staticmethod
    def load_CSV(filename, fmt):
        data = pandas.read_csv(filename, sep='\s+|\,', comment='#', header=None, names=CSVFormatPose.get_format(fmt),
                               engine='python')
        return data

    @staticmethod
    def save_CSV(data_frame, filename, fmt, save_index=False):
        head = os.path.dirname(os.path.abspath(filename))
        if not os.path.exists(head):
            os.makedirs(head)

        data_frame.to_csv(filename, sep=',', index=save_index,
                          header=CSVFormatPose.get_header(fmt),
                          columns=CSVFormatPose.get_format(fmt))

    @staticmethod
    def subsample_DataFrame(df, step=None, num_max_points=None, verbose=False):

        num_elems = len(df.index)

        if num_max_points:
            step = 1
            if (int(num_max_points) > 0) and (int(num_max_points) < num_elems):
                step = int(math.ceil(num_elems / float(num_max_points)))

        sparse_indices = np.arange(start=0, stop=num_elems, step=step)

        if (num_max_points or step):
            if verbose:
                print("CSV2DataFrame.subsample_DataFrame():")
                print("* len: " + str(num_elems) + ", max_num_points: " + str(
                    num_max_points) + ", subsample by: " + str(step))

            df_sub = df.loc[sparse_indices]
            df_sub.reset_index(inplace=True)

            return df_sub

        else:
            return df

