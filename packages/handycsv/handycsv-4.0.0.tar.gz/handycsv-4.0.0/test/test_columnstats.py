"""
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * - Redistributions of source code must retain the above copyright notice, this
 * list of conditions and the following disclaimer.
 *
 * - Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * - Neither the name of prim nor the names of its contributors may be used to
 * endorse or promote products derived from this software without specific prior
 * written permission.
 *
 * See the NOTICE file distributed with this work for additional information
 * regarding copyright ownership.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
"""

# Python 3 compatibility
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
import handycsv
import unittest
import tempfile


class TestColumnStats(unittest.TestCase):

  @staticmethod
  def make_str(raw_vals):
    return ''.join(','.join([str(v) for v in row]) + '\n' for row in raw_vals)

  k4x2 = [
    ['-', 'a'],
    ['d', 0],
    ['e', 3],
    ['f', 6]
  ]

  def test_handy(self):
    text = TestColumnStats.make_str(TestColumnStats.k4x2)

    stats = handycsv.ColumnStats.load(text)
    self.assertEqual(stats.row_names(), ['-', 'd', 'e', 'f'])
    self.assertEqual(stats.get('d'), 0)
    self.assertEqual(stats.get('f'), 6)

    with self.assertRaises(IndexError):
      stats.get('z')

    self.assertEqual(str(stats), text)

    with self.assertRaises(IndexError):
      stats.set('z', 99)

    stats.set('d', 20)
    stats.set('f', 70)
    self.assertEqual(stats.row_names(), ['-', 'd', 'e', 'f'])
    self.assertEqual(stats.get('d'), 20)
    self.assertEqual(stats.get('f'), 70)

    with self.assertRaises(IndexError):
      stats.remove_row('z')

    stats.remove_row('e')
    self.assertEqual(stats.row_names(), ['-', 'd', 'f'])
    self.assertEqual(stats.get('d'), 20)
    self.assertEqual(stats.get('f'), 70)
    with self.assertRaises(IndexError):
      stats.get('e')

    stats = handycsv.ColumnStats.load(text)

    self.assertEqual(stats.filter_rows('3'), ['e'])
    self.assertEqual(stats.row_names(), ['-', 'd', 'f'])
    self.assertEqual(stats.get('d'), 0)
    self.assertEqual(stats.get('f'), 6)
    with self.assertRaises(IndexError):
      stats.get('e')

    stats = handycsv.ColumnStats.load(text)
    self.assertEqual(stats.filter_rows('\d'), ['d', 'e', 'f'])

    stats = handycsv.ColumnStats.load(text)
    self.assertEqual(stats.filter_rows('\d', invert=True), ['-'])

    stats = handycsv.ColumnStats.load(text)
    self.assertEqual(stats.filter_rows('foo'), [])

    stats = handycsv.ColumnStats.load(text)
    with self.assertRaises(IndexError):
      stats.filter_rows('foo', invert=True)

    for ext in ['.csv', '.csv.gz']:
      _, csvfile1 = tempfile.mkstemp(prefix='TestColumnStats', suffix=ext)
      stats.write(csvfile1, transpose=True)

      newstats = handycsv.ColumnStats.read(csvfile1, transpose=True)
      self.assertEqual(newstats.source, csvfile1)
      self.assertEqual(stats, newstats)

      os.remove(csvfile1)

    skeleton = handycsv.ColumnStats.create(['-', 'd', 'e', 'f'])
    stats = handycsv.ColumnStats.load(text)
    self.assertEqual(skeleton.row_names(), stats.row_names())
