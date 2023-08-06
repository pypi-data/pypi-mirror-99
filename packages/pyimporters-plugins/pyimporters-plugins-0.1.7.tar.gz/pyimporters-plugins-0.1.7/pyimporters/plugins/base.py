import abc
from typing import Optional, List, Dict, Any, Type

from pydantic import BaseModel, Field
from typing.io import IO


class Concept(BaseModel):
    identifier: str = Field(str, description="Unique identifier of the concept", example="http://www.example.com/rocks")
    prefLabel: str = Field(str, description="Unique identifier of the concept")
    prefLabel: str = Field(..., description="The preferred label of the concept", example="rocks")
    altLabel: Optional[List[str]] = Field(..., description="The alternative labels of the concept", example=["basalt", "granite", "slate"])
    properties: Optional[Dict[str,Any]] = Field(None, description="Additional properties of the concept", example={"wikidataId" : "Q8063"})

class KnowledgeParserOptions(BaseModel):
    """
    Options for the knowledge import
    """
    format: str = Field(None, description="Format of the import")
    lang: str = Field('en', description="Language of the project", extra="internal")
    limit: int = Field(0, description="Number of concepts to import. O means all", extra="advanced", ge=0)
    class Config:
        orm_mode = True

class KnowledgeParserBase(metaclass=abc.ABCMeta):
    """Base class for example plugin used in the tutorial.
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def parse(self, source : IO, options : KnowledgeParserOptions):
        """Parse the input source file and return a stream of concepts.

        :param source: A file object containing the knowledge.
        :param options: options of the parser.
        :returns: Iterable producing the concepts.
        """

    @classmethod
    def get_schema(cls) -> Type[BaseModel]:
        return KnowledgeParserOptions