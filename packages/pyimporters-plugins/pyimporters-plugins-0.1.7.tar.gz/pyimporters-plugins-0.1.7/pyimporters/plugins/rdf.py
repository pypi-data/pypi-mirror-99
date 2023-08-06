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
from enum import Enum
from typing import Type

from pydantic import BaseModel, Field
from pyimporters.plugins.base import KnowledgeParserBase, KnowledgeParserOptions, Concept

class RDFFormat(str, Enum):
    xml = 'xml'
    n3 = 'n3'
    turtle = 'turtle'
    nt = 'nt'

class RDFOptions(KnowledgeParserOptions):
    """
    Options for the RDF knowledge import
    """
    rdf_format: RDFFormat = Field(RDFFormat.xml, description="RDF format")


class RDFKnowledgeParser(KnowledgeParserBase):
    def parse(self, source, options : KnowledgeParserOptions):
        # for name, value in sorted(source.items()):
        #     concept : Concept = Concept(identifier=name, prefLabel=value)
        yield Concept(identifier="http://kt.com#1", prefLabel="foo", altLabels=["Foo", "fooo"])
        yield Concept(identifier="http://kt.com#2", prefLabel="bar", altLabels=["BAR", "baar"])

    @classmethod
    def get_schema(cls) -> Type[BaseModel]:
        return RDFOptions