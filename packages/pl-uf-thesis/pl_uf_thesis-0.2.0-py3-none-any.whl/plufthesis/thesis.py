import datetime
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Union, List, Optional, Sequence, Callable, Dict

import pyexlatex as pl
from pyexlatex import Package
from pyexlatex.logic.builder import build, _build
from pyexlatex.models.control.documentclass.documentclass import DocumentClass
from pyexlatex.models.section.sections import Chapter
from pyexlatex.models.credits.author import Author
from pyexlatex.models.document import DocumentBase
from pyexlatex.models.format.paragraph.sloppy import Sloppy
from pyexlatex.models.title.title import Title
from pyexlatex.typing import PyexlatexItems
from pyexlatex.models.document import get_table_figure_size_packages
import plufthesis.info_models as im
from plufthesis import register_doc_type

from plufthesis.info_models import ThesisTypes


class UFThesis(DocumentBase):
    """
    The main high-level class for creating UF theses/dissertations
    """
    name = 'document'

    def __init__(self, content: PyexlatexItems, title: str, author: str,
                 major: str, chair: str, abstract: PyexlatexItems,
                 bibliography: pl.Bibliography,
                 dedication_contents: PyexlatexItems = 'I dedicate this to...',
                 acknowledgements_contents: PyexlatexItems = 'I would like to thank...',
                 biographical_contents: PyexlatexItems = 'Nick made this Pyexlatex template from the LaTeX template, then got a Ph.D.',
                 abbreviation_contents: Optional[PyexlatexItems] = None,
                 appendix_contents: Optional[Sequence[Chapter]] = None,
                 multiple_appendices: bool = False,
                 edit_mode: bool = False,
                 bibliography_style: str = 'amsplain',
                 co_chair: Optional[str] = None,
                 thesis_type: ThesisTypes = ThesisTypes.DISSERTATION,
                 degree_type: str = 'Doctor of Philosophy',
                 degree_year: int = datetime.datetime.today().year,
                 degree_month: str = 'May',
                 has_tables: bool = False, has_figures: bool = False,
                 has_objects: bool = False,
                 tables_relative_font_size: int = 0,
                 figures_relative_font_size: int = 0,
                 natbib_options: Optional[str] = 'numbers',
                 packages: Optional[List[Union[Package, str]]]=None,
                 pre_env_contents: Optional[PyexlatexItems] = None,
                 pre_output_func: Optional[Callable] = None):
        self.natbib_options = natbib_options
        self.init_data()
        # These package imports are already handled in the cls file. To avoid conflicts
        # when using items which also include these packages, add these to packages first
        self.data.packages.append(pl.Package('hyperref', modifier_str='linktoc=all'))
        self.data.packages.append(pl.Package('natbib', modifier_str=natbib_options))

        # Necessary to get self.data.references which sets self.has_references in DocumentBase
        # which enables bibtex
        self.data.references.extend(bibliography.references)

        register_doc_type(self.natbib_options)
        if edit_mode:
            self.document_class_obj = DocumentClass(
                document_type='uf-thesis-dissertation',
                options=['editMode'],
            )
        else:
            self.document_class_obj = DocumentClass(
                document_type='uf-thesis-dissertation',
            )
        register_doc_type()

        from pyexlatex.models.item import ItemBase
        if pre_env_contents is None:
            pre_env_contents_list = []
        elif isinstance(pre_env_contents, (ItemBase, str)):
            pre_env_contents_list = [pre_env_contents]
        else:
            pre_env_contents_list = pre_env_contents  # type: ignore

        if has_tables:
            pre_env_contents_list.append(pl.Raw(r'\haveTablestrue'))
        if has_figures:
            pre_env_contents_list.append(pl.Raw(r'\haveFigurestrue'))
        if has_objects:
            pre_env_contents_list.append(pl.Raw(r'\haveObjectstrue'))

        self.temp_tex_contents: Dict[str, PyexlatexItems] = dict(
            dedicationFile=dedication_contents,
            acknowledgementsFile=acknowledgements_contents,
            abstractFile=abstract,
            referenceFile=_build(bibliography.references),
            biographyFile=biographical_contents,
        )
        set_ref_file = r'\setReferenceFile{referenceFile}{' + bibliography_style + '}%'

        pre_env_contents_list.extend([
            Sloppy(),
            Title(title),
            im.DegreeType(degree_type),
            im.Major(major),
            Author(author, short_author=None),
            im.ThesisType(thesis_type),
            im.DegreeYear(degree_year),
            im.DegreeMonth(degree_month),
            im.Chair(chair, co_chair),
            pl.Raw(r"""
\setDedicationFile{dedicationFile}%                 Dedication Page
\setAcknowledgementsFile{acknowledgementsFile}%     Acknowledgements Page
\setAbstractFile{abstractFile}%                     Abstract Page (This should only include the abstract itself)
\setBiographicalFile{biographyFile}%                Biography file of the Author (you).
            """),
            pl.Raw(set_ref_file),
        ])

        if multiple_appendices:
            pre_env_contents_list.append(pl.Raw(r"""
\multipleAppendixtrue%                          Uncomment this if you have more than one appendix, 
%                                                   comment it if you have only one appendix.
            """))

        if abbreviation_contents is not None:
            pre_env_contents_list.append(pl.Raw(r"""
\setAbbreviationsFile{abbreviations}%           Abbreviations Page
            """))
            self.temp_tex_contents.update(abbreviations=abbreviation_contents)

        if appendix_contents is not None:
            pre_env_contents_list.append(pl.Raw(r"""
\setAppendixFile{appendix}%                     Appendix Content; hyperlinking might be weird.
                        """))
            self.temp_tex_contents.update(appendix=appendix_contents)

        for temp_content in self.temp_tex_contents.values():
            self.add_data_from_content(temp_content)

        floatrow_options = 'capposition=top,captionskip=0pt'
        pre_env_contents_list.extend(
            get_table_figure_size_packages(
                tables_relative_font_size,
                figures_relative_font_size,
                floatrow_table_options=floatrow_options,
                floatrow_figure_options=floatrow_options,
            )
        )

        super().__init__(
            content,
            packages=packages,
            pre_env_contents=pre_env_contents_list,
            pre_output_func=pre_output_func,
        )

    def _write_temp_tex_file(self, name: str, content: PyexlatexItems, directory: Path, ext: str = 'tex'):
        out_path = directory / f'{name}.{ext}'
        text_content = build(content)
        out_path.write_text(text_content)
        self.data.filepaths.append(str(out_path))
        self.data.binaries.append(bytes(text_content, 'utf8'))

    def _write_temp_tex_files(self, directory: Path):
        for name, content in self.temp_tex_contents.items():
            if name == 'referenceFile':
                ext = 'bib'
            else:
                ext = 'tex'
            self._write_temp_tex_file(name, content, directory, ext=ext)

    def to_pdf(self, *args, **kwargs):
        with TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            orig_data = deepcopy(self.data)
            self._write_temp_tex_files(tmp_dir)
            result = super().to_pdf(*args, **kwargs)
            self.data = orig_data
        return result

    def to_html(self, *args, **kwargs):
        with TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            orig_data = deepcopy(self.data)
            self._write_temp_tex_files(tmp_dir)
            result = super().to_html(*args, **kwargs)
            self.data = orig_data
        return result
