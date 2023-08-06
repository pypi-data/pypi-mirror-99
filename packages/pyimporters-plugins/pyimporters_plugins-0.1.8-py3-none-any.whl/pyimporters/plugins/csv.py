from typing import Type

from pydantic import Field, BaseModel
from pyimporters.plugins.base import KnowledgeParserOptions, KnowledgeParserBase, Concept


class CSVOptions(KnowledgeParserOptions):
    """
    Options for the CSV knowledge import
    """
    sep: str = Field(',', description="Field separator")


class CSVKnowledgeParser(KnowledgeParserBase):
    def parse(self, source, options : KnowledgeParserOptions):
        for name, value in sorted(source.items()):
            concept : Concept = Concept(identifier=name, prefLabel=value)
            yield Concept(identifier="1", prefLabel="foo")
            yield Concept(identifier="2", prefLabel="bar")

    @classmethod
    def get_schema(cls) -> Type[BaseModel]:
        return CSVOptions