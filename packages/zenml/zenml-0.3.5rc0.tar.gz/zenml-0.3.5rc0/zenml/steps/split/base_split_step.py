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

from abc import abstractmethod
from typing import Text, List

from tensorflow_metadata.proto.v0.schema_pb2 import Schema
from tensorflow_metadata.proto.v0.statistics_pb2 import \
    DatasetFeatureStatisticsList

from zenml.steps import BaseStep
from zenml.enums import StepTypes


class BaseSplit(BaseStep):
    """
    Base split class. Each custom data split should derive from this.
    In order to define a custom split, override the base split's partition_fn
    method.
    """

    STEP_TYPE = StepTypes.split.name

    def __init__(self,
                 statistics: DatasetFeatureStatisticsList = None,
                 schema: Schema = None,
                 **kwargs):
        """
        Base Split constructor.

        Args:
            statistics: Parsed statistics output of a preceding StatisticsGen.
            schema: Parsed schema output of a preceding SchemaGen.
        """
        super().__init__(**kwargs)
        self.statistics = statistics
        self.schema = schema

    @abstractmethod
    def partition_fn(self):
        """
        Returns the partition function associated with the current split type,
        along with keyword arguments used in the signature of the partition
        function.

        To be eligible in use in a Split Step, the partition_fn has to adhere
        to the following design contract:

        1. The signature is of the following type:

            >>> def partition_fn(element, n, **kwargs) -> int,

            where n is the number of splits;
        2. The partition_fn only returns signed integers i less than n, i.e. ::

                0 ≤ i ≤ n - 1.

        Returns:
            A tuple (partition_fn, kwargs) of the partition function and its
             additional keyword arguments (see above).
        """
        pass

    @abstractmethod
    def get_split_names(self) -> List[Text]:
        """
        Returns the names of the splits associated with this split step.

        Returns:
            A list of strings, which are the split names.
        """
        pass

    def get_num_splits(self):
        """
        Returns the total number of splits.

        Returns:
            A positive integer, the number of splits.
        """
        return len(self.get_split_names())
