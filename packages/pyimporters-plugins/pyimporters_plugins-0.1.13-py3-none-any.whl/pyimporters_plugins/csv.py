from typing import Type, Dict, Any

from pydantic import Field, BaseModel
from pyimporters_plugins.base import KnowledgeParserOptions, KnowledgeParserBase, Concept


class CSVOptions(KnowledgeParserOptions):
    """
    Options for the CSV knowledge import
    """
    separator = Field(',', description="Field separator")


class CSVKnowledgeParser(KnowledgeParserBase):
    def parse(self, source, options : Dict[str,Any]):
        options = CSVOptions(**options)
        # for name, value in sorted(source.items()):
        #     concept : Concept = Concept(identifier=name, prefLabel=value)
        yield Concept(identifier="1", prefLabel="foo")
        yield Concept(identifier="2", prefLabel="bar")

    @classmethod
    def get_schema(cls) -> Type[BaseModel]:
        return CSVOptions