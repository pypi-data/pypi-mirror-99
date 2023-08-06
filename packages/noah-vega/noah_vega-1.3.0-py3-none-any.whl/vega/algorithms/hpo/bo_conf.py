# -*- coding:utf-8 -*-

# Copyright (C) 2020. Huawei Technologies Co., Ltd. All rights reserved.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the MIT License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# MIT License for more details.

"""Defined Configs."""
from zeus.common import ConfigSerializable


class BoPolicyConfig(ConfigSerializable):
    """Bo Policy Config."""

    total_epochs = 10
    max_epochs = 1
    warmup_count = 5
    alg_name = 'SMAC'

    @classmethod
    def rules(cls):
        """Return rules for checking."""
        rules_BoPolicyConfig = {"total_epochs": {"type": int},
                                "max_epochs": {"type": int},
                                "warmup_count": {"type": int},
                                "alg_name": {"type": str}
                                }
        return rules_BoPolicyConfig


class BoConfig(ConfigSerializable):
    """Bo Config."""

    policy = BoPolicyConfig
    objective_keys = 'accuracy'

    @classmethod
    def rules(cls):
        """Return rules for checking."""
        rules_BoConfig = {"policy": {"type": dict},
                          "objective_keys": {"type": (list, str)}
                          }
        return rules_BoConfig

    @classmethod
    def get_config(cls):
        """Get sub config."""
        return {
            "policy": cls.policy
        }
