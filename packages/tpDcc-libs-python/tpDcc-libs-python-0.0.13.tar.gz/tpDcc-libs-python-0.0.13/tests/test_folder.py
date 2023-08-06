#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains folder related tests for tpDcc-libs-python
"""

from __future__ import print_function, division, absolute_import

import os
import uuid
import shutil
from tpDcc.libs.unittests.core import unittestcase

from tpDcc.libs.python import folder


class TestFolder(unittestcase.UnitTestCase()):
    def __init__(self, *args, **kwargs):
        super(TestFolder, self).__init__(*args, **kwargs)

        self._data_folder = None

    def setUp(self):
        super(TestFolder, self).setUp()

        self._data_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tests_data')
        if not os.path.isdir(self._data_folder):
            os.makedirs(self._data_folder)

    def tearDown(self):
        super(TestFolder, self).tearDown()

        if os.path.isdir(self._data_folder):
            shutil.rmtree(self._data_folder)

    def _get_folder_path(self, split=False):
        folder_path = os.path.join(self._data_folder, str(uuid.uuid4().hex))
        if split:
            folder_dir = os.path.dirname(folder_path)
            folder_name = os.path.basename(folder_path)
            return folder_dir, folder_name
        else:
            return folder_path


class TestFolderCreation(TestFolder):

    def test_folder_creation_path(self):
        self.assertTrue(os.path.isdir(folder.create_folder(self._get_folder_path())))

    def test_folder_creation_name_directory(self):
        split_folder_path = self._get_folder_path(split=True)
        self.assertTrue(os.path.isdir(folder.create_folder(split_folder_path[1], split_folder_path[0])))

    def test_folder_creation_unique(self):
        folder_path = self._get_folder_path()
        folder.create_folder(folder_path)
        self.assertTrue(os.path.isdir(folder.create_folder(folder_path, make_unique=True)))


class TestFolderRename(TestFolder):
    pass
