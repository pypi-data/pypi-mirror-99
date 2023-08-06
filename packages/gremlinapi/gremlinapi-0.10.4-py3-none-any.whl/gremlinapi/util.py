# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging


log = logging.getLogger("GremlinAPI.client")

_version = "0.10.4"


def get_version():
    return _version
