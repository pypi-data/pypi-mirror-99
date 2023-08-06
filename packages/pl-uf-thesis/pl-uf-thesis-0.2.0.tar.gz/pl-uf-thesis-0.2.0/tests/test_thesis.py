from pathlib import Path

import pyexlatex as pl

from tests.config import INPUT_FILES_DIR
from tests.utils.doc import compare_doc
from tests.fixtures.thesis import (
    thesis,
    thesis_full_single_appendix,
    thesis_multiple_appendix,
    thesis_custom_doc_class,
    thesis_tables_and_figures,
    thesis_from_next_level_down,
    thesis_appendix_tables_and_figures,
    thesis_small_tables_and_figures
)


def test_create_thesis(thesis):
    name = "thesis"
    doc = thesis

    compare_doc(doc, name)


def test_create_thesis_full_single_appendix(thesis_full_single_appendix):
    name = "thesis_full_single_appendix"
    doc = thesis_full_single_appendix

    compare_doc(doc, name)


def test_create_thesis_multiple_appendix(thesis_multiple_appendix):
    name = "thesis_multiple_appendix"
    doc = thesis_multiple_appendix

    compare_doc(doc, name)


def test_create_thesis_custom_doc_class(thesis_custom_doc_class):
    name = "thesis_custom_doc_class"
    doc = thesis_custom_doc_class

    compare_doc(doc, name)


def test_create_thesis_tables_and_figures(thesis_tables_and_figures):
    name = "thesis_tables_and_figures"
    doc = thesis_tables_and_figures

    compare_doc(doc, name)


def test_create_thesis_from_next_level_down(thesis_from_next_level_down):
    name = "thesis"
    doc = thesis_from_next_level_down

    compare_doc(doc, name)


def test_create_thesis_appendix_tables_and_figures(thesis_appendix_tables_and_figures):
    name = "thesis_appendix_tables_and_figures"
    doc = thesis_appendix_tables_and_figures

    compare_doc(doc, name)


def test_create_thesis_small_tables_and_figures(thesis_small_tables_and_figures):
    name = "thesis_small_tables_and_figures"
    doc = thesis_small_tables_and_figures

    compare_doc(doc, name)