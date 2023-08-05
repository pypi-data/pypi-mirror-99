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
"""CSv Datasource definition"""

from typing import Text, Dict

from zenml.datasources import BaseDatasource
from zenml.steps.data import CSVDataStep


class CSVDatasource(BaseDatasource):
    """ZenML CSV datasource definition.

    Use this for CSV training pipelines.
    """

    def __init__(
            self,
            name: Text,
            path: Text,
            schema: Dict = None,
            **kwargs):
        """
        Create a CSV datasource. Creating this datasource creates a Beam
        pipeline that converts the CSV file into TFRecords for pipelines to
        use.

        The path can be a local path or a Google Cloud Storage bucket
        path for now (S3, Azure coming soon). The path defines the datasource,
        meaning a change in it (including file name) should be dealt with by
        creating another datasource.

        Args:
            name (str): name of datasource.
            path (str): path to csv file.
            schema (str): optional schema for data to conform to.
        """
        super().__init__(name, **kwargs)
        self.path = path
        self.schema = schema

    def get_data_step(self):
        return CSVDataStep(self.path, self.schema)
