from typing import Type, Dict, Any
from zipfile import Path

from pydantic import Field, BaseModel
from pyimporters_plugins.base import KnowledgeParserOptions, KnowledgeParserBase, Concept

class DummyOptions(KnowledgeParserOptions):
    """
    Options for the Dummy knowledge import
    """
    foo : str = Field("bar", description="Dummy parameter")

class DummyKnowledgeParser(KnowledgeParserBase):
    def parse(self, source : Path, options : Dict[str,Any]):
        options = DummyOptions(**options)
        yield Concept(identifier=options.foo, prefLabel=options.foo)

    @classmethod
    def get_schema(cls) -> Type[BaseModel]:
        return DummyOptions

