#!/usr/bin/env python3

from cmk.rulesets.v1 import Label, Title, Help
from cmk.rulesets.v1.form_specs import Percentage, BooleanChoice, DefaultValue, DictElement, Dictionary, Float, Integer, LevelDirection, SimpleLevels, IECMagnitude, DataSize, TimeSpan, TimeMagnitude
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic

def parameter_form_dma_queue():
    return Dictionary(
        elements = {
            "length": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Length of mail queue"),
                    form_spec_template = Integer(),
                    level_direction = LevelDirection.UPPER,
                    prefill_fixed_levels = DefaultValue(value=(10, 20)),
                ),
                required = True,
            ),
            "size": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Size of mail queue"),
                    form_spec_template=DataSize(
                        displayed_magnitudes=[IECMagnitude.MEBI],
                    ),
                    level_direction = LevelDirection.UPPER,
                    prefill_fixed_levels = DefaultValue(value=(10, 20)),
                ),
                required = True,
            ),
            "age_spool": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Maximum age of spool files"),
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=[
                            TimeMagnitude.DAY,
                            TimeMagnitude.HOUR,
                            TimeMagnitude.MINUTE,
                        ],
                    ),
                    level_direction = LevelDirection.UPPER,
                    prefill_fixed_levels = DefaultValue(value=(24.0 * 3600.0, 48 * 3600.0)),
                ),
                required = True,
            ),
            "age_flush": DictElement(
                parameter_form = SimpleLevels(
                    title = Title("Maximum age of flush marker"),
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=[
                            TimeMagnitude.DAY,
                            TimeMagnitude.HOUR,
                            TimeMagnitude.MINUTE,
                        ],
                    ),
                    level_direction = LevelDirection.UPPER,
                    prefill_fixed_levels = DefaultValue(value=(3600.0, 2 * 3600.0)),
                ),
                required = True,
            ),
        },
    )
    
rule_spec_watterott_co2_special_co2 = CheckParameters(
    name = "dma_spool",
    title = Title("Dragonfly Mail Agent spool directory"),
    topic = Topic.ENVIRONMENTAL,
    parameter_form = parameter_form_dma_queue,
    condition = HostCondition(),
)
