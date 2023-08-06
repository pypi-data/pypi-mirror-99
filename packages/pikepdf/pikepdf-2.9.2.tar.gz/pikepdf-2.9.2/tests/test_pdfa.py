import os
import xml.etree.ElementTree as ET
from pathlib import Path
from subprocess import PIPE, STDOUT, run

import pytest

from pikepdf import Pdf

try:
    VERAPDF = Path(os.environ['HOME']) / 'verapdf' / 'verapdf'
    if not VERAPDF.is_file():
        VERAPDF = None
except Exception:  # pylint: disable=w0703
    VERAPDF = None

pytestmark = pytest.mark.skipif(not VERAPDF, reason="verapdf not found")


def verapdf_validate(filename):
    proc = run([VERAPDF, filename], stdout=PIPE, stderr=STDOUT, check=True)
    result = proc.stdout.decode('utf-8')
    xml_start = result.find('<?xml version')
    xml = result[xml_start:]
    root = ET.fromstring(xml)
    node = root.find(".//validationReports")
    result = node.attrib['compliant'] == '1' and node.attrib['failedJobs'] == '0'
    if not result:
        print(proc.stdout.decode())
    return result


def test_pdfa_sanity(resources, outdir):
    filename = resources / 'veraPDF test suite 6-2-10-t02-pass-a.pdf'

    assert verapdf_validate(filename)

    with Pdf.open(filename) as pdf:
        pdf.save(outdir / 'pdfa.pdf')

        assert verapdf_validate(outdir / 'pdfa.pdf')
        m = pdf.open_metadata()
        assert m.pdfa_status == '1B'
        assert m.pdfx_status == ''

    with Pdf.open(resources / 'graph.pdf') as pdf:
        m = pdf.open_metadata()
        assert m.pdfa_status == ''


def test_pdfa_modify(resources, outdir):
    sandwich = resources / 'sandwich.pdf'
    assert verapdf_validate(sandwich)

    with Pdf.open(sandwich) as pdf:
        with pdf.open_metadata(
            update_docinfo=False, set_pikepdf_as_editor=False
        ) as meta:
            pass
        with pytest.raises(RuntimeError, match="not opened"):
            del meta['pdfaid:part']
        pdf.save(outdir / '1.pdf')
    assert verapdf_validate(outdir / '1.pdf')

    with Pdf.open(sandwich) as pdf:
        with pdf.open_metadata(
            update_docinfo=False, set_pikepdf_as_editor=True
        ) as meta:
            pass
        pdf.save(outdir / '2.pdf')
    assert verapdf_validate(outdir / '2.pdf')

    with Pdf.open(sandwich) as pdf:
        with pdf.open_metadata(update_docinfo=True, set_pikepdf_as_editor=True) as meta:
            meta['dc:source'] = 'Test'
            meta['dc:title'] = 'Title Test'
        pdf.save(outdir / '3.pdf')
    assert verapdf_validate(outdir / '3.pdf')


def test_pdfa_creator(resources, outdir, caplog):
    sandwich = resources / 'sandwich.pdf'

    with Pdf.open(sandwich) as pdf:
        with pdf.open_metadata(
            update_docinfo=False, set_pikepdf_as_editor=False
        ) as meta:
            meta['dc:creator'] = 'The Creator'
        messages = [
            rec.message
            for rec in caplog.records
            if rec.message.startswith('dc:creator')
        ]
        if not messages:
            pytest.fail("Failed to warn about setting dc:creator to a string")
