# -*- coding: utf-8 -*-
# Copyright (C) 2020 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import abc
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field


class Concept(BaseModel):
    identifier: str = Field(str, description="Unique identifier of the concept", example="http://www.example.com/rocks")
    prefLabel: str = Field(str, description="Unique identifier of the concept")
    prefLabel: str = Field(..., description="The preferred label of the concept", example="rocks")
    altLabel: Optional[List[str]] = Field(..., description="The alternative labels of the concept", example=["basalt", "granite", "slate"])
    properties: Optional[Dict[str,Any]] = Field(None, description="Additional properties of the concept", example={"wikidataId" : "Q8063"})

class BaseOptions(BaseModel):
    """
    Options for the knowledge import
    """
    lang: str = Field('en', description="Language of the project", extra="internal")
    limit: int = Field(0, description="Number of concepts to import. O means all", extra="advanced", ge=0)
    mongo_tocol: str = Field("concepts",
                                description="Collection where concepts are stored in the mongo database",
                                extra="advanced,internal")
    class Config:
        orm_mode = True

class KnowledgeParserBase(metaclass=abc.ABCMeta):
    """Base class for example plugin used in the tutorial.
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def parse(self, source, options : BaseOptions):
        """Format the data and return unicode text.

        :param data: A dictionary with string keys and simple types as
                     values.
        :type data: dict(str:?)
        :returns: Iterable producing the concepts.
        """
