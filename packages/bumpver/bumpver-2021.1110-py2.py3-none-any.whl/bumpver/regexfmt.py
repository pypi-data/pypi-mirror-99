# -*- coding: utf-8 -*-
# This file is part of the bumpver project
# https://github.com/mbarkhau/bumpver
#
# Copyright (c) 2018-2021 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import re
import logging
import textwrap
from . import pysix
logger = logging.getLogger('bumpver.regexfmt')


def format_regex(regex):
    """Format a regex pattern suitible for flags=re.VERBOSE.

    >>> regex = r"\\[CalVer v(?P<year_y>[1-9][0-9]{3})(?P<month>(?:1[0-2]|0[1-9]))"
    >>> print(format_regex(regex))
    \\[CalVer[ ]v
    (?P<year_y>[1-9][0-9]{3})
    (?P<month>
        (?:1[0-2]|0[1-9])
    )
    """
    re.compile(regex)
    tmp_regex = regex.replace(' ', '[ ]')
    tmp_regex = tmp_regex.replace('"', '\\"')
    tmp_regex, _ = re.subn('([^\\\\])?\\)(\\?)?', '\\1)\\2\n', tmp_regex)
    tmp_regex, _ = re.subn('([^\\\\])\\(', '\\1\n(', tmp_regex)
    tmp_regex, _ = re.subn('^\\)\\)', ')\n)', tmp_regex, flags=re.MULTILINE)
    lines = tmp_regex.splitlines()
    indented_lines = []
    level = 0
    for line in lines:
        if line.strip():
            increment = line.count('(') - line.count(')')
            if increment >= 0:
                line = '    ' * level + line
                level += increment
            else:
                level += increment
                line = '    ' * level + line
            indented_lines.append(line)
    formatted_regex = '\n'.join(indented_lines)
    re.compile(formatted_regex)
    return formatted_regex


def pyexpr_regex(regex):
    try:
        formatted_regex = format_regex(regex)
        formatted_regex = textwrap.indent(formatted_regex.rstrip(), '    ')
        return ('re.compile(r"""\n' + formatted_regex +
            '\n""", flags=re.VERBOSE)')
    except re.error:
        return 're.compile({0})'.format(repr(regex))


URL_TEMPLATE = 'https://regex101.com/?flavor=python&flags=gmx&regex='


def regex101_url(regex_pattern):
    try:
        regex_pattern = format_regex(regex_pattern)
    except re.error:
        logger.warning("Error formatting regex '{0}'".format(repr(
            regex_pattern)))
    return URL_TEMPLATE + pysix.quote(regex_pattern)
