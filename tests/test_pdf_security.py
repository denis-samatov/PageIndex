"""PDF parser regressions use authored bytes, never external documents."""
import subprocess
import sys


def test_unterminated_content_comment_does_not_hang():
    # PyPDF2 3.0.1 loops forever on this content stream (GHSA-4vvm-4w3v-6mr8).
    # A child timeout turns a parser regression into a bounded test failure.
    program = '''
import io
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

writer = PdfWriter()
writer.add_blank_page(width=72, height=72)
page = writer.pages[0]
stream = DecodedStreamObject()
stream.set_data(b"% comment without terminating newline")
page[NameObject("/Contents")] = writer._add_object(stream)
page[NameObject("/Resources")] = DictionaryObject()
payload = io.BytesIO()
writer.write(payload)
reader = PdfReader(io.BytesIO(payload.getvalue()))
assert reader.pages[0].extract_text() == ""
'''
    subprocess.run([sys.executable, '-c', program], check=True,
                   capture_output=True, text=True, timeout=10)
