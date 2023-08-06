from enum import Enum
from pathlib import Path
from typing import Type, Dict, Any

from progress.bar import Bar
from pydantic import BaseModel, Field
from rdflib import Graph, RDF, SKOS
from rdflib.resource import Resource

from pyimporters_plugins.base import KnowledgeParserBase, KnowledgeParserOptions, Concept

class RDFFormat(str, Enum):
    xml = 'xml'
    n3 = 'n3'
    turtle = 'turtle'
    nt = 'nt'
    json_ld = 'json-ld'

class SKOSOptions(KnowledgeParserOptions):
    """
    Options for the RDF knowledge import
    """
    rdf_format: RDFFormat = Field(RDFFormat.xml, description="RDF format")


class SKOSKnowledgeParser(KnowledgeParserBase):
    def parse(self, source : Path, options : Dict[str,Any], bar : Bar):
        options = SKOSOptions(**options)
        bar.max = 20
        bar.start()
        g = Graph()
        thes = g.parse(source=str(source), format=options.rdf_format)
        bar.next(20)
        bar.max = len(list(thes.subjects(predicate=RDF.type, object=SKOS.Concept)))
        for curi in thes[:RDF.type:SKOS.Concept]:
            bar.next()
            c = Resource(g, curi)
            concept: Concept = None
            for prefLabel in c.objects(SKOS.prefLabel):
                if prefLabel.language.startswith(options.lang):
                    concept: Concept = Concept(identifier=str(curi), prefLabel=prefLabel.value)
            if concept:
                for altLabel in c.objects(SKOS.altLabel):
                    if altLabel.language.startswith(options.lang):
                        if concept.altLabel is None:
                            concept.altLabel = []
                        concept.altLabel.append(altLabel.value)
                yield concept
        bar.finish()

    @classmethod
    def get_schema(cls) -> Type[BaseModel]:
        return SKOSOptions