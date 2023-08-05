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
"""Tests for the ZenML image data step."""

import json

import pytest

from zenml.components.data_gen.constants import FILE_EXT, FILE_NAME, \
    BINARY_DATA, IMAGE, LABEL
from zenml.steps.data.image_data_step import get_matching_label, \
    add_label_and_metadata, SplitByFileName

json_data = {"1f22663e72.jpg": {"label": 0,
                                "metadata": {"height": 256,
                                             "width": 256,
                                             "num_channels": 3}}}


def test_get_matching_label():
    filename = "1f22663e72.jpg"
    label_data = json.dumps(json_data)

    label, metadata = get_matching_label(label_data=label_data,
                                         img_filename=filename)

    expected_label = json_data[filename]["label"]
    expected_metadata = json_data[filename]["metadata"]

    assert label == expected_label
    assert metadata == expected_metadata

    # simulate an image filename not found inside the dict
    json_data2 = {}
    label_data = json.dumps(json_data2)

    with pytest.raises(KeyError):
        _, _ = get_matching_label(label_data=label_data, img_filename=filename)


def test_file_split():
    # example image
    example1 = {FILE_NAME: "abc", FILE_EXT: ".jpg"}

    # example label file, found by the file extension .txt
    example2 = {FILE_NAME: "def", FILE_EXT: ".txt"}

    # pathological image file, taken as label file by the function because
    # the word "label" is present in the file name
    example3 = {FILE_NAME: "xyz_label", FILE_EXT: ".jpg"}

    # png image, to be detected as image
    example4 = {FILE_NAME: "data", FILE_EXT: ".png"}

    splits = [SplitByFileName(ex, 2) for ex in [example1, example2,
                                                example3, example4]]

    assert splits == [0, 1, 1, 0]


def test_add_label_and_metadata():
    filename = "1f22663e72.jpg"
    label_data = {BINARY_DATA: json.dumps(json_data)}

    example_img = {FILE_NAME: filename, BINARY_DATA: b"12345"}

    updated_img = add_label_and_metadata(image_dict=example_img,
                                         label_dict=label_data)

    assert BINARY_DATA not in updated_img
    assert IMAGE in updated_img
    assert LABEL in updated_img
    assert all(md_key in updated_img for md_key in
               json_data[filename]["metadata"])
