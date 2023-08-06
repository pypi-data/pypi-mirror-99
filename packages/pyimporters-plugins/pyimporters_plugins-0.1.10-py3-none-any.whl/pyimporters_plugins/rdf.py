from enum import Enum
from typing import Type

from pydantic import BaseModel, Field
from pyimporters_plugins.base import KnowledgeParserBase, KnowledgeParserOptions, Concept

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