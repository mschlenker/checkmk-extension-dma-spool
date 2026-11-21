#!/usr/bin/env python3
# encoding: utf-8

from cmk.agent_based.v2 import AgentSection, CheckPlugin, Service, Result, State, Metric, check_levels, render
import time

def parse_dma_spool(string_table):
    parsed = {}
    for line in string_table:
        if len(line) > 1:
            if line[0] == "spooldir":
                parsed["spooldir"] = line[1]
            else:
                parsed[line[0]] = int(line[1])
    return parsed

def discover_dma_spool(section):
    yield Service()
    
def check_dma_spool(params, section):
    now = int(time.time())
    # yield Result(state=State.OK, summary="Everything is fine")
    # Metrics for occupied space etc.
    yield from check_levels(
        section["spoolcount"],
        levels_upper=params["length"],
        metric_name = "mail_queue_deferred_length",
        notice_only = True,
    )
    yield from check_levels(
        section["spoolsize"],
        levels_upper=params["size"],
        metric_name = "mail_queue_deferred_size",
        notice_only = True,
    )
    if section["spoolcount"] > 0:
        s_age = now - section["spoololdest"]
        yield from check_levels(
            s_age,
            levels_upper = params["age_spool"],
            metric_name = "age_oldest_spool",
            render_func=render.timespan,
            notice_only = True,
        )
    if section["flushmtime"] > 0:
        f_age = now - section["flushmtime"]
        yield from check_levels(
            f_age,
            levels_upper = params["age_flush"],
            metric_name = "age_flush",
            render_func=render.timespan,
            notice_only = True,
        )
        
agent_section_myhostgroups = AgentSection(
    name = "dma_spool",
    parse_function = parse_dma_spool,
)

check_plugin_myhostgroups = CheckPlugin(
    name = "dma_spool",
    service_name = "Dragonfly Mail Agent spool",
    discovery_function = discover_dma_spool,
    check_function = check_dma_spool,
    check_default_parameters = {
        "length": ("fixed", (10, 20)),
        "size": ("fixed", (10 * 1024 * 1024, 20 * 1024 * 1024)),
        "age_spool": ("fixed", (24.0 * 3600.0, 48 * 3600.0)),
        "age_flush": ("fixed", (1.0 * 3600.0, 2 * 3600.0)),
    },
    check_ruleset_name = "dma_spool",
)
