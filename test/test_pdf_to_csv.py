import os
import shutil
import pytest
from unittest.mock import patch

from pdf_to_csv import is_pdf, is_pdf_password_protected, extract_table_from_pdf


@pytest.fixture()
def output_folder():
    folder = "test/output"
    os.makedirs(folder, exist_ok=True)
    yield folder
    shutil.rmtree(folder)


def test_is_pdf():
    assert is_pdf("test.pdf") is True
    assert is_pdf("test.txt") is False


def test_is_pdf_password_protected():
    assert is_pdf_password_protected("example_pdfs/pdf5.pdf") is True
    assert is_pdf_password_protected("example_pdfs/pdf4.pdf") is False


def test_extract_table_from_valid_pdf(output_folder):
    extract_table_from_pdf("example_pdfs/pdf2.pdf", output_folder)
    assert os.path.exists(f"{output_folder}/table_1.csv")
    with open(f"{output_folder}/table_1.csv", "r") as file:
        assert file.read() != ""


def test_pdf_with_no_table_data(output_folder):
    extract_table_from_pdf("example_pdfs/pdf1.pdf", output_folder)
    assert not os.path.exists(f"{output_folder}/table_1.csv")


@patch("pdf_to_csv.check_for_password")
def test_extract_table_from_password_protected_pdf_invalid_password(mock_check_for_password, output_folder):
    # Mocking invalid password
    mock_check_for_password.return_value = "pass"

    extract_table_from_pdf("example_pdfs/pdf5.pdf", output_folder)

    # Asserting that table file is not created
    assert not os.path.exists(f"{output_folder}/table_1.csv")

    # Asserting that check_for_password method was called once with the correct arguments
    mock_check_for_password.assert_called_once_with("example_pdfs/pdf5.pdf")


@patch("pdf_to_csv.check_for_password")
def test_extract_table_from_password_protected_pdf_valid_password(mock_check_for_password, output_folder):
    # Mocking valid password
    mock_check_for_password.return_value = "123456"

    extract_table_from_pdf("example_pdfs/pdf5.pdf", output_folder)

    # Asserting that table file is created and not empty
    assert os.path.exists(f"{output_folder}/table_1.csv")
    with open(f"{output_folder}/table_1.csv", "r") as file:
        assert file.read() != ""

    # Asserting that check_for_password method was called once with the correct arguments
    mock_check_for_password.assert_called_once_with("example_pdfs/pdf5.pdf")
