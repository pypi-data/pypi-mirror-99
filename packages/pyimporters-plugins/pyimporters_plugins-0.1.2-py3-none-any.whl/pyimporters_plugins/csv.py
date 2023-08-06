# Copyright (C) 2020 Red Hat, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
from pydantic import Field
from pyimporters_plugins.base import BaseOptions, KnowledgeParserBase, Concept


class CSVOptions(BaseOptions):
    """
    Options for the CSV knowledge import
    """
    sep: str = Field(',', description="Field separator")


class CSVKnowledgeParser(KnowledgeParserBase):
    """A very basic formatter."""

    def parse(self, source, options : BaseOptions):
        """Format the data and return unicode text.

        :param data: A dictionary with string keys and simple types as
                     values.
        :type data: dict(str:?)
        """
        for name, value in sorted(source.items()):
            concept : Concept = Concept(identifier=name, prefLabel=value)
            yield Concept(identifier="1", prefLabel="foo")
            yield Concept(identifier="2", prefLabel="bar")
