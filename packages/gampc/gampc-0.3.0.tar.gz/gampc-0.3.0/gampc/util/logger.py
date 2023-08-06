# coding: utf-8
#
# Graphical Asynchronous Music Player Client
#
# Copyright (C) 2015 Itaï BEN YAACOV
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import logging
import os


root = logging.getLogger()
root.setLevel(os.environ.get('LOGLEVEL', 'INFO'))

handler = logging.StreamHandler()
# handler.setFormatter(logging.Formatter(fmt='%(levelname)s: %(name)s: %(message)s (%(pathname)s %(lineno)d)'))
handler.setFormatter(logging.Formatter(fmt='%(levelname)s: %(name)s: %(message)s'))
root.addHandler(handler)

logger = logging.getLogger(__name__.split('.')[0])
