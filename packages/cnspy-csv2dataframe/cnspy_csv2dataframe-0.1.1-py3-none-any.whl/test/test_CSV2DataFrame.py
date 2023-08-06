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
########################################################################################################################
import os
import unittest
from cnspy_csv2dataframe.CSV2DataFrame import CSV2DataFrame
from cnspy_spatial_csv_formats.CSVFormatPose import CSVFormatPose

SAMPLE_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_data')

class CSV2DataFrame_Test(unittest.TestCase):
    def test_CTOR(self):
        d1 = CSV2DataFrame(str(SAMPLE_DATA_DIR + '/ID1-pose-gt.csv'))
        self.assertTrue(d1.format == CSVFormatPose.TUM)
        self.assertTrue(d1.data_loaded)
        d2 = CSV2DataFrame(str(SAMPLE_DATA_DIR + '/ID1-pose-est-cov.csv'), fmt=CSVFormatPose.PoseCov)
        self.assertTrue(d2.format == CSVFormatPose.PoseCov)
        self.assertTrue(d2.data_loaded)

        d3 = CSV2DataFrame()
        d3.load_from_CSV(fn=str(SAMPLE_DATA_DIR + '/ID1-pose-est-cov.csv'))
        self.assertTrue(d3.data_loaded)
        d3.save_to_CSV(fn=str(SAMPLE_DATA_DIR + '/results/ID1-pose-est-cov.COPY.csv'))


if __name__ == '__main__':
    unittest.main()
