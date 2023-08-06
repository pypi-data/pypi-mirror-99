# -*- coding: utf-8 -*-
# --------------------------
# Copyright © 2014 -            Qentinel Group.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ---------------------------

import os
import slate3k as slate_pdf_reader
from pdfminer.pdfparser import PSEOF
from QWeb.internal import download, util
from QWeb.internal.exceptions import QWebFileNotFoundError, QWebValueMismatchError


class File:

    ACTIVE_FILE = None

    def __init__(self, content, file):
        self.content = content
        self.file = file
        File.ACTIVE_FILE = self

    @staticmethod
    def create_pdf_instance(filename):
        all_text = ''
        filepath = download.get_path(filename)
        try:
            with open(filepath, 'rb') as pdf_obj:
                pdf = slate_pdf_reader.PDF(pdf_obj)
                for page in pdf:
                    all_text += page.strip()
                if all_text != '':
                    return File(all_text, filepath)
                raise QWebValueMismatchError('Text not found. Seems that the pdf is empty.')
        except TypeError as e:
            raise QWebFileNotFoundError('File not found. Got {} instead.'.format(e))
        except PSEOF as e:
            raise QWebFileNotFoundError('File found, but it\'s not valid pdf-file: {}'.format(e))

    @staticmethod
    def create_text_file_instance(filename):
        filepath = download.get_path(filename)
        try:
            with open(filepath, 'rb') as txt_file:
                data = txt_file.read()
                data = data.decode("utf-8")
                if data != '':
                    return File(data, filepath)
                raise QWebValueMismatchError('Text not found. Seems that the file is empty.')
        except TypeError as e:
            raise QWebFileNotFoundError('File not found. Got {} instead.'.format(e))

    def get(self, **kwargs):
        if kwargs:
            return util.get_substring(self.content, **kwargs)
        return self.content

    def verify(self, text):
        if text in self.content:
            return True
        raise QWebValueMismatchError('File did not contain the text "{}"'.format(text))

    def remove(self):
        os.remove(self.file)

    def get_index_of(self, text, condition):
        index = self.content.find(text)
        if index > -1:
            if util.par2bool(condition) is False:
                index += len(text)
            return index
        raise QWebValueMismatchError('File did not contain the text "{}"'.format(text))
