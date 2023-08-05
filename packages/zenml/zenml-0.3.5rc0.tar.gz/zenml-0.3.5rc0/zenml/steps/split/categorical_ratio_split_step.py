#  Copyright (c) maiot GmbH 2020. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""Implementation of the ratio-based categorical split."""

from typing import Text, List, Dict, Union

from zenml.steps.split import constants
from zenml.steps.split import BaseSplit
from zenml.steps.split.categorical_domain_split_step import \
    CategoricalPartitionFn
from zenml.steps.split.utils import partition_cat_list

CategoricalValue = Union[Text, int]


def lint_split_map(split_map: Dict[Text, float]):
    """Small utility to lint the split_map"""
    if constants.TRAIN not in split_map.keys():
        raise AssertionError(f'You have to define some values for '
                             f'the {constants.TRAIN} split.')
    if len(split_map) <= 1:
        raise AssertionError('Please specify more than 1 split name in the '
                             'split_map!')


class CategoricalRatioSplit(BaseSplit):
    """
    Categorical ratio split. Use this to split data based on a list of values
    of interest in a single categorical column. A categorical column is
    defined here as a column with finitely many values of type `integer` or
    `string`. In contrast to the categorical domain split, here categorical
    values are assigned to different splits by the corresponding percentages,
    defined inside a split ratio object.
    """

    def __init__(
            self,
            categorical_column: Text,
            categories: List[CategoricalValue],
            split_ratio: Dict[Text, float],
            unknown_category_policy: Text = constants.SKIP,
            statistics=None,
            schema=None,
    ):
        """
        Categorical domain split constructor.

        Use this class to split your data based on values in
        a single categorical column. A categorical column is defined here as a
        column with finitely many values of type `integer` or `string`.

        Example usage:

        # Split on a categorical attribute called "color", with a defined list
        of categories of interest

        # half of the categories go entirely into the train set,
          the other half into the eval set. Other colors, e.g. "purple",
           are discarded due to the "skip" flag.

        >>> split = CategoricalRatioSplit(
        ... categorical_column="color",
        ... categories = ["red", "green", "blue", "yellow"],
        ... split_ratio = {"train": 0.5,
        ...                "eval": 0.5},
        ... unknown_category_policy="skip")

        Supply the unknown_category_policy flag to set the unknown category
        handling policy. There are two main options:

        Setting unknown_category_policy to any key in the split map indicates
        that any missing categories should be put into that particular split.
        For example, supplying ``unknown_category_policy="train"`` indicates
        that all missing categories should go into the training dataset, while
        ``unknown_category_policy="eval"`` indicates that all missing
        categories should go into the evaluation dataset.

        Setting ``unknown_category_policy="skip"`` indicates that data points
        with unknown categorical values (i.e., values not present in the
        categorical value list) should be taken out of the data set.

        Args:
            statistics: Parsed statistics from a preceding StatisticsGen.
            schema: Parsed schema from a preceding SchemaGen.
            categorical_column: Name of the categorical column used for
             splitting.
            categories: List of categorical values found in the categorical
             column on which to split.
            split_ratio: A dict mapping { split_name: percentage of categories
                                    in split }.
            unknown_category_policy: String, indicates how to handle categories
             in the data that are not present in the supplied category list.
        """
        self.categorical_column = categorical_column

        split_map = partition_cat_list(categories, split_ratio)
        lint_split_map(split_map)
        self.split_map = split_map

        if unknown_category_policy in self.split_map:
            self.unknown_category_policy = unknown_category_policy
        else:
            self.unknown_category_policy = constants.SKIP

        super().__init__(statistics=statistics,
                         schema=schema,
                         categorical_column=categorical_column,
                         split_ratio=split_ratio,
                         categories=categories,
                         unknown_category_policy=unknown_category_policy)

    def partition_fn(self):
        return CategoricalPartitionFn, {
            'split_map': self.split_map,
            'categorical_column': self.categorical_column,
            'unknown_category_policy': self.unknown_category_policy
        }

    def get_split_names(self) -> List[Text]:
        split_names = list(self.split_map.keys())
        if self.unknown_category_policy in self.split_map:
            return split_names
        else:
            return split_names + [constants.SKIP]
