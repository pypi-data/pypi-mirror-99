from pathlib import Path
from typing import Type, Dict, Any, Generator
from progress.bar import Bar
from pydantic import Field, BaseModel
from pyimporters_plugins.base import KnowledgeParserOptions, KnowledgeParserBase, Term

class DummyOptions(KnowledgeParserOptions):
    """
    Options for the Dummy knowledge import
    """
    foo : str = Field("bar", description="Dummy parameter")

class DummyKnowledgeParser(KnowledgeParserBase):
    def parse(self, source : Path, options : Dict[str,Any], bar : Bar) -> Generator[Term, None, None]:
        options = DummyOptions(**options)
        bar.max = 1
        bar.start()
        bar.next()
        yield Term(identifier=options.foo, prefLabel=options.foo)
        bar.finish()

    @classmethod
    def get_schema(cls) -> Type[BaseModel]:
        return DummyOptions

