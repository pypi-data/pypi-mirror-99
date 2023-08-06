from enum import Enum
from typing import Type, Dict, Any

from pydantic import BaseModel, Field
from rdflib import Graph, RDF, SKOS
from rdflib.resource import Resource

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
    def parse(self, source, options : Dict[str,Any]):
        options = RDFOptions(**options)
        g = Graph()
        thes = g.parse(file=source, format=options.rdf_format)
        for curi in thes[:RDF.type:SKOS.Concept]:
            c = Resource(g, curi)
            concept: Concept = Concept(identifier=curi)
            for prefLabel in c.objects(SKOS.prefLabel):
                if prefLabel.language.startswith(options.lang):
                    concept.prefLabel = prefLabel.value
            for altLabel in c.objects(SKOS.altLabel):
                if altLabel.language.startswith(options.lang):
                    concept.altLabel.add(altLabel.value)
            yield concept

    @classmethod
    def get_schema(cls) -> Type[BaseModel]:
        return RDFOptions