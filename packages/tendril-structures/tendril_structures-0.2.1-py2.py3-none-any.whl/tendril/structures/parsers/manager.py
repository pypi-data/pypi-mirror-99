#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2021 Chintalagiri Shashank
#
# This file is part of tendril.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Tendril Structure Parsers Manager (:mod:`tendril.structure.parsers.manager`)
============================================================================
"""


import importlib

from tendril.utils.versions import get_namespace_package_names
from tendril.utils import log
logger = log.get_logger(__name__, log.DEBUG)


class StructureParsersManager(object):
    def __init__(self, prefix):
        self._prefix = prefix
        self._parsers = {}
        self._docs = []
        self._load_parsers()

    def _load_parsers(self):
        logger.debug("Loading structure parsers from {0}".format(self._prefix))
        modules = list(get_namespace_package_names(self._prefix))
        for m_name in modules:
            if m_name == __name__:
                continue
            m = importlib.import_module(m_name)
            m.install(self)
        logger.debug("Done loading structure parsers from {0}".format(self._prefix))

    def install(self, name, parser, doc):
        logger.debug("Installing structure parser {0}".format(name))
        self._parsers[name] = parser
        self._docs.append((name, doc))

    def __getattr__(self, item):
        if item == '__file__':
            return None
        if item == '__path__':
            return None
        if item == '__len__':
            return len(self._parsers.keys())
        if item == '__all__':
            return list(self._parsers.keys()) + \
                   ['install_parser', 'doc_render']
        return self._parsers[item]

    def doc_render(self):
        return self._docs

    def __repr__(self):
        return "<StructureParsersManager>"
