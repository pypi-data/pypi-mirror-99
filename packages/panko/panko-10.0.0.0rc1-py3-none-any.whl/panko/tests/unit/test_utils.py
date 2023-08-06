#
# Copyright 2012 New Dream Network, LLC (DreamHost)
# Copyright (c) 2013 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Tests for panko/utils.py
"""
import datetime
import decimal

from oslotest import base

from panko import utils


class TestUtils(base.BaseTestCase):

    def test_datetime_to_decimal(self):
        expected = 1356093296.12
        utc_datetime = datetime.datetime.utcfromtimestamp(expected)
        actual = utils.dt_to_decimal(utc_datetime)
        self.assertAlmostEqual(expected, float(actual), places=5)

    def test_decimal_to_datetime(self):
        expected = 1356093296.12
        dexpected = decimal.Decimal(str(expected))  # Python 2.6 wants str()
        expected_datetime = datetime.datetime.utcfromtimestamp(expected)
        actual_datetime = utils.decimal_to_dt(dexpected)
        # Python 3 have rounding issue on this, so use float
        self.assertAlmostEqual(utils.dt_to_decimal(expected_datetime),
                               utils.dt_to_decimal(actual_datetime),
                               places=5)

    def test_recursive_keypairs(self):
        data = {'a': 'A', 'b': 'B',
                'nested': {'a': 'A', 'b': 'B'}}
        pairs = list(utils.recursive_keypairs(data))
        self.assertEqual([('a', 'A'), ('b', 'B'),
                          ('nested:a', 'A'), ('nested:b', 'B')],
                         pairs)

    def test_recursive_keypairs_with_separator(self):
        data = {'a': 'A',
                'b': 'B',
                'nested': {'a': 'A',
                           'b': 'B',
                           },
                }
        separator = '.'
        pairs = list(utils.recursive_keypairs(data, separator))
        self.assertEqual([('a', 'A'),
                          ('b', 'B'),
                          ('nested.a', 'A'),
                          ('nested.b', 'B')],
                         pairs)

    def test_recursive_keypairs_with_list_of_dict(self):
        small = 1
        big = 1 << 64
        expected = [('a', 'A'),
                    ('b', 'B'),
                    ('nested:list', [{small: 99, big: 42}])]
        data = {'a': 'A',
                'b': 'B',
                'nested': {'list': [{small: 99, big: 42}]}}
        pairs = list(utils.recursive_keypairs(data))
        self.assertEqual(len(expected), len(pairs))
        for k, v in pairs:
            # the keys 1 and 1<<64 cause a hash collision on 64bit platforms
            if k == 'nested:list':
                self.assertIn(v,
                              [[{small: 99, big: 42}],
                               [{big: 42, small: 99}]])
            else:
                self.assertIn((k, v), expected)

    def test_decimal_to_dt_with_none_parameter(self):
        self.assertIsNone(utils.decimal_to_dt(None))
