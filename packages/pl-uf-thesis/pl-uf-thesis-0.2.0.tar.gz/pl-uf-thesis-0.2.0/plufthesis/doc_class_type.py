from typing import Optional

import pyexlatex as pl
from pyexlatex.models.control.documentclass.classtypes.documentclasstype import (
    DocumentClassType,
)

from plufthesis.config import ASSETS_PATH

UF_THESIS_DISSERTATION_CLS_FILE = ASSETS_PATH / "ufdissertation.cls"
UF_THESIS_DISSERTATION_CLS_TEXT = UF_THESIS_DISSERTATION_CLS_FILE.read_text()


def get_class_type(natbib_options: Optional[str] = "numbers") -> DocumentClassType:
    orig_natbib = pl.RequirePackage("natbib", modifier_str="numbers")
    new_natbib = pl.RequirePackage("natbib", modifier_str=natbib_options)
    new_cls_text = UF_THESIS_DISSERTATION_CLS_TEXT.replace(
        str(orig_natbib), str(new_natbib)
    )
    class_type = DocumentClassType("uf-thesis-dissertation", new_cls_text)
    return class_type


# TODO [$602039315315e00008a1abd9]: replace this once pyexlatex has a more convenient way of adding custom class types
def register_doc_type(natbib_options: Optional[str] = "numbers"):
    from pyexlatex.models.control.documentclass.classtypes.custom import (
        CUSTOM_CLASS_TYPES,
    )

    class_type = get_class_type(natbib_options)
    CUSTOM_CLASS_TYPES[class_type.name] = class_type
