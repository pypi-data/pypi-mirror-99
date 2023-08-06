# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Manage datasets of benchmarks."""
from compiler_gym.datasets.dataset import (
    LegacyDataset,
    activate,
    deactivate,
    delete,
    require,
)

__all__ = ["LegacyDataset", "require", "activate", "deactivate", "delete"]
