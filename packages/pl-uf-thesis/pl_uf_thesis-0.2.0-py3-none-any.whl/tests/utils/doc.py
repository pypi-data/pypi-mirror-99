from pyexlatex.models.document import DocumentBase

from tests.config import GENERATED_FILES_DIR, INPUT_FILES_DIR, GENERATE_MODE
from tests.utils.pdf import compare_pdfs


def compare_doc(doc: DocumentBase, name: str):
    if GENERATE_MODE:
        return doc.to_pdf(INPUT_FILES_DIR, outname=name)

    compare_path = INPUT_FILES_DIR / f"{name}.tex"
    assert str(doc) == compare_path.read_text()
    doc.to_pdf(GENERATED_FILES_DIR, outname=name)
    compare_pdfs(INPUT_FILES_DIR / f'{name}.pdf', GENERATED_FILES_DIR / f'{name}.pdf')