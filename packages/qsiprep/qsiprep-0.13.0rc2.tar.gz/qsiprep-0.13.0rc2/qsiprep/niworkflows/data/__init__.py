#!/usr/bin/env python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
""" Data fetchers module """
from __future__ import absolute_import, division, print_function, unicode_literals

from .getters import (
    get_brainweb_1mm_normal,
    get_ds003_downsampled,
    get_dataset,
    get_template,
    get_bids_examples,
    TEMPLATE_ALIASES,
)
