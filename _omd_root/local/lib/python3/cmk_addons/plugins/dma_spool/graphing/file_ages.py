#!/usr/bin/env python3
# Copyright (C) 2023 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.graphing.v1 import metrics, perfometers, Title

UNIT_TIME = metrics.Unit(metrics.TimeNotation())

metric_age_oldest_spool = metrics.Metric(
    name="age_oldest_spool",
    title=Title("Age of oldest spool file"),
    unit=UNIT_TIME,
    color=metrics.Color.YELLOW,
)

metric_age_flush = metrics.Metric(
    name="age_flush",
    title=Title("Age of flush marker"),
    unit=UNIT_TIME,
    color=metrics.Color.BLUE,
)

perfometer_age_flush = perfometers.Perfometer(
    name="age_flush",
    focus_range=perfometers.FocusRange(perfometers.Closed(0), perfometers.Open(5000000)),
    segments=["age_flush"],
)
