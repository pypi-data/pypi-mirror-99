from pathlib import Path
from typing import Type, Dict, Any
from progress.bar import Bar
from pydantic import Field, BaseModel
from pyimporters_plugins.base import KnowledgeParserOptions, KnowledgeParserBase, Concept

class DummyOptions(KnowledgeParserOptions):
    """
    Options for the Dummy knowledge import
    """
    foo : str = Field("bar", description="Dummy parameter")

class DummyKnowledgeParser(KnowledgeParserBase):
    def parse(self, source : Path, options : Dict[str,Any], bar : Bar):
        options = DummyOptions(**options)
        bar.max = 1
        bar.start()
        bar.next()
        yield Concept(identifier=options.foo, prefLabel=options.foo)
        bar.finish()

    @classmethod
    def get_schema(cls) -> Type[BaseModel]:
        return DummyOptions

