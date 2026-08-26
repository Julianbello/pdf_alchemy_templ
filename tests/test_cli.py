import sys
import fitz
from pathlib import Path
from unittest.mock import patch


# Ensure the project root is in sys.path for imports
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from cmdline import Cmdline
from parseargs import PDFArgumentParser


# Test assets
ASSET_PDF = PROJECT_ROOT / "tests" / "assets" / "test_alchemy.pdf"
ASSET_IMAGE = PROJECT_ROOT / "tests" / "assets" / "test.png"


def run_cmdline(args_list, capsys):
    """Helper to parse arguments, run Cmdline, and capture output."""
    parser = PDFArgumentParser()
    args = parser.parser.parse_args(args_list)
    app = Cmdline(args)

    if args.total_pages:
        app.get_num_pages()

    elif args.split:
        app.split_pdf()

    elif args.delete:
        app.del_range()

    elif args.crop_half:
        app.crop_half()

    elif args.command == "add":
        app.add_pdf()

    elif args.command == "translate":
        app.translate_pdf()

    elif args.command == "image":
        app.add_image()

    else:
        print("No arguments used")

    return capsys.readouterr().out


# ============================================================
# TEST 1 - GET NUMBER OF PAGES
# ============================================================

def test_get_num_pages(capsys):
    out = run_cmdline(
        [
            "-f",
            str(ASSET_PDF),
            "-o",
            "out",
            "-tp"
        ],
        capsys
    )

    assert "Total pages" in out


# ============================================================
# TEST 2 - SPLIT PDF
# ============================================================

def test_split_pdf(tmp_path, capsys):
    out_dir = tmp_path / "split"
    out_dir.mkdir()

    run_cmdline(
        [
            "-f",
            str(ASSET_PDF),
            "-o",
            str(out_dir),
            "-s",
            "1-2",
            "3-4"
        ],
        capsys
    )

    part1 = out_dir / "part_1.pdf"
    part2 = out_dir / "part_2.pdf"

    assert part1.is_file()
    assert part2.is_file()

    doc1 = fitz.open(part1)
    doc2 = fitz.open(part2)

    assert doc1.page_count == 2
    assert doc2.page_count >= 1

    doc1.close()
    doc2.close()


# ============================================================
# TEST 3 - DELETE RANGE
# ============================================================

def test_del_range(tmp_path, capsys):
    out_pdf = tmp_path / "deleted.pdf"

    run_cmdline(
        [
            "-f",
            str(ASSET_PDF),
            "-o",
            str(out_pdf),
            "-d",
            "1-2"
        ],
        capsys
    )

    assert out_pdf.is_file()

    src_doc = fitz.open(ASSET_PDF)
    out_doc = fitz.open(out_pdf)

    assert out_doc.page_count == src_doc.page_count - 2

    src_doc.close()
    out_doc.close()


# ============================================================
# TEST 4 - ADD PDF
# ============================================================

def test_add_pdf(tmp_path, capsys):
    insert_pdf = tmp_path / "insert.pdf"

    doc = fitz.open()
    doc.new_page()
    doc.save(insert_pdf)
    doc.close()

    out_pdf = tmp_path / "added.pdf"

    run_cmdline(
        [
            "-f",
            str(ASSET_PDF),
            "-o",
            str(out_pdf),
            "add",
            str(insert_pdf),
            "--after",
            "1"
        ],
        capsys
    )

    assert out_pdf.is_file()

    src_doc = fitz.open(ASSET_PDF)
    out_doc = fitz.open(out_pdf)

    assert out_doc.page_count == src_doc.page_count + 1

    src_doc.close()
    out_doc.close()


# ============================================================
# TEST 5 - CROP HALF
# ============================================================

def test_crop_half(tmp_path, capsys):
    out_pdf = tmp_path / "cropped.pdf"

    run_cmdline(
        [
            "-f",
            str(ASSET_PDF),
            "-o",
            str(out_pdf),
            "-ch",
            "1"
        ],
        capsys
    )

    assert out_pdf.is_file()

    src_doc = fitz.open(ASSET_PDF)
    out_doc = fitz.open(out_pdf)

    assert out_doc.page_count == src_doc.page_count + 1

    src_doc.close()
    out_doc.close()


# ============================================================
# TEST 6 - TRANSLATE PDF
# ============================================================

def test_translate_pdf(tmp_path, capsys):
    out_pdf = tmp_path / "translated" / "translated.pdf"

    class FakeTranslator:

        def __init__(self, source, target):
            self.source = source
            self.target = target

        def translate(self, text):
            return "Translated text"

    with patch(
        "deep_translator.GoogleTranslator",
        FakeTranslator
    ):
        run_cmdline(
            [
                "-f",
                str(ASSET_PDF),
                "-o",
                str(out_pdf),
                "translate",
                "--to",
                "es"
            ],
            capsys
        )

    assert out_pdf.is_file()

    src_doc = fitz.open(ASSET_PDF)
    out_doc = fitz.open(out_pdf)

    # The translated PDF must have the same number of pages
    assert out_doc.page_count == src_doc.page_count

    # Verify translated text
    translated_text = out_doc[0].get_text()

    assert "Translated text" in translated_text

    src_doc.close()
    out_doc.close()


# ============================================================
# TEST 7 - ADD IMAGE
# ============================================================

def test_add_image(tmp_path, capsys):
    out_pdf = tmp_path / "image_test" / "image_added.pdf"

    run_cmdline(
        [
            "-f",
            str(ASSET_PDF),
            "-o",
            str(out_pdf),
            "image",
            str(ASSET_IMAGE),
            "--page",
            "1",
            "--x",
            "100",
            "--y",
            "100",
            "--width",
            "200",
            "--height",
            "200"
        ],
        capsys
    )

    assert out_pdf.is_file()

    src_doc = fitz.open(ASSET_PDF)
    out_doc = fitz.open(out_pdf)

    # Adding an image must not change the page count
    assert out_doc.page_count == src_doc.page_count

    # Verify image exists on first page
    page = out_doc.load_page(0)
    images = page.get_images(full=True)

    assert len(images) >= 1

    src_doc.close()
    out_doc.close()