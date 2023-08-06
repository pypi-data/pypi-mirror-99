#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = """
    pySART - Simplified AUTOSAR-Toolkit for Python.

   (C) 2009-2019 by Christoph Schueler <cpu12.gems@googlemail.com>

   All Rights Reserved

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License along
  with this program; if not, write to the Free Software Foundation, Inc.,
  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import struct


def makeWordPacker(byteorder="@"):
    """"""
    return struct.Struct("{}H".format(byteorder)).pack


def makeWordUnpacker(byteorder="@"):
    """"""
    return struct.Struct("{}H".format(byteorder)).unpack


def makeDWordPacker(byteorder="@"):
    """"""
    return struct.Struct("{}I".format(byteorder)).pack


def makeDWordUnpacker(byteorder="@"):
    """"""
    return struct.Struct("{}I".format(byteorder)).unpack
