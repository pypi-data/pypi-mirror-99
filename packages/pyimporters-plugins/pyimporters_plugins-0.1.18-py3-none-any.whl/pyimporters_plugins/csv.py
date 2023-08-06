from typing import Type, Dict, Any

from pydantic import Field, BaseModel
from pyimporters_plugins.base import KnowledgeParserOptions, KnowledgeParserBase, Concept

class TXTOptions(KnowledgeParserOptions):
    """
    Options for the TXT knowledge import
    """
    encoding : str = Field('utf-8', description="Encoding of the file")

class TXTKnowledgeParser(KnowledgeParserBase):
    def parse(self, source, options : Dict[str,Any]):
        options = TXTOptions(**options)
        # for name, value in sorted(source.items()):
        #     concept : Concept = Concept(identifier=name, prefLabel=value)
        yield Concept(identifier="foo", prefLabel="foo")
        yield Concept(identifier="bar", prefLabel="bar")

    @classmethod
    def get_schema(cls) -> Type[BaseModel]:
        return TXTOptions

class CSVOptions(TXTOptions):
    """
    Options for the CSV knowledge import
    """
    separator : str = Field(',', description="Field separator")
    quotechar : str = Field('"', description="")
    header : str = Field('infer', description="Row number(s) to use as the column names, and the start of the data")
    skip_blank_lines : bool = Field(True, description="If True, skip over blank lines rather than interpreting as NaN values")

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