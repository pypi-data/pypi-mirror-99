"""
University of Florida Thesis/Dissertation Template for Pyexlatex
"""
from plufthesis.doc_class_type import register_doc_type
# Causes doc class type to get registered in pyexlatex
register_doc_type()
from plufthesis.transformers import elevate_sections_by_one_level
