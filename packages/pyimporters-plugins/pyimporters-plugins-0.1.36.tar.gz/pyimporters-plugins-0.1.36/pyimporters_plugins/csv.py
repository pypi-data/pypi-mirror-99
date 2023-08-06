import codecs
from pathlib import Path
from typing import Type, Dict, Any
import pandas as pd
from progress.bar import Bar
from pydantic import Field, BaseModel
from pyimporters_plugins.base import KnowledgeParserOptions, KnowledgeParserBase, Concept

class TXTOptions(KnowledgeParserOptions):
    """
    Options for the TXT knowledge import
    """
    encoding : str = Field('utf-8', description="Encoding of the file")

class TXTKnowledgeParser(KnowledgeParserBase):
    def parse(self, source : Path, options : Dict[str,Any], bar : Bar):
        options = TXTOptions(**options)
        bar.max = file_len(source)
        bar.start()
        with source.open("r", encoding=options.encoding) as fin:
            for line in fin:
                bar.next()
                term = line.strip()
                if term:
                    yield Concept(identifier=term, prefLabel=term)
        bar.finish()

    @classmethod
    def get_schema(cls) -> Type[BaseModel]:
        return TXTOptions

class CSVOptions(TXTOptions):
    """
    Options for the CSV knowledge import
    """
    separator : str = Field(',', description="Field separator")
    quotechar : str = Field('"', description="")
    multivalue_separator : str = Field(None, description="Additional separator to split multivalued columns if any")
    header : str = Field('infer', description="Row number(s) to use as the column names, and the start of the data")
    skip_blank_lines : bool = Field(True, description="If True, skip over blank lines rather than interpreting as NaN values")
    identifier_col : str = Field(None, description="Column to use as the identifier of the concept, either given as string name or column index")
    prefLabel_col : str = Field(None, description="Column to use as the prefLabel of the concept, either given as string name or column index")
    altLabel_cols : str = Field(None, description="Column(s) to use as the altLabel of the concept, either given as a (list of) string name(s) or column index(es)")

class CSVKnowledgeParser(KnowledgeParserBase):
    def parse(self, source : Path, options : Dict[str,Any], bar : Bar):
        options = CSVOptions(**options)
        bar.max = file_len(source)
        bar.start()
        lines = pd.read_csv(source,
                            sep=options.separator,
                            quotechar=options.quotechar,
                            header=options.header if options.header else None,
                            skip_blank_lines=options.skip_blank_lines,
                            encoding=options.encoding).fillna(value='')
        prefLabel_col = 0 if (options.prefLabel_col is None or not options.prefLabel_col.strip()) else col_index(options.prefLabel_col)
        identifier_col = prefLabel_col if (options.identifier_col is None or not options.identifier_col.strip()) else col_index(options.identifier_col)
        altLabel_cols =  None if (options.altLabel_cols is None or not options.altLabel_cols.strip()) else options.altLabel_cols
        all_cols = [col for col in lines.columns if col not in [prefLabel_col, identifier_col]] if altLabel_cols else None
        for index, row in lines.iterrows():
            bar.next()
            prefLabel = row[prefLabel_col].strip()
            identifier = row[identifier_col].strip()
            concept : Concept = Concept(identifier=identifier, prefLabel=prefLabel)
            if altLabel_cols:
                concept.altLabel = []
                alts_cols = [col_index(x.strip()) for x in altLabel_cols.split(',')]
                restrict =  any(col.startswith("-") for col in alts_cols)
                if restrict:
                    list_cols = [col for col in all_cols if f"-{col}" not in alts_cols]
                    alts_cols = list_cols
                for alt_col in alts_cols:
                    altLabel = row[alt_col].strip()
                    if altLabel:
                        if options.multivalue_separator:
                            altLabels = [x.strip() for x in altLabel.split(options.multivalue_separator)]
                            concept.altLabel.extend(altLabels)
                        else:
                            concept.altLabel.add(altLabel)
            yield concept
        bar.finish()

    @classmethod
    def get_schema(cls) -> Type[BaseModel]:
        return CSVOptions

def col_index(col):
    return int(col) if col.lstrip('+-').isdigit() else col

def file_len(input_file:Path):
  """ Count number of lines in a file."""
  with open(input_file) as f:
      nr_of_lines = sum(1 for line in f)
  return nr_of_lines
