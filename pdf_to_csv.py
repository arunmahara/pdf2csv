import os
import tabula
import PyPDF2
import logging
from getpass import getpass

# Set up logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s: %(levelname)s: %(filename)s-%(lineno)s: %(message)s'
)
log = logging.getLogger(__name__)


def is_pdf(file_path: str) -> bool:
    """
    Check if the file is a PDF file.
    """
    _, file_ext = os.path.splitext(file_path)
    return file_ext.lower() == ".pdf"


def is_pdf_password_protected(pdf_file_path: str) -> bool:
    """
    Check if the PDF file is password protected.
    """
    with open(pdf_file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        if reader.is_encrypted:
            return True
        else:
            return False


def check_for_password(pdf_file_path: str) -> str:
    """
    Check if the PDF is password protected and ask for the password if it is.
    """
    password = None

    # Check if the PDF is password protected
    if is_pdf_password_protected(pdf_file_path):
        log.info(f"PDF {pdf_file_path} is password protected.")
        # Ask for the password
        password = getpass("Enter the password: ")

    return password


def extract_table_from_pdf(pdf_file_path: str, output_folder_path: str) -> str:
    """
    Extract tables from a PDF file and save them as CSV files.
    """
    try:
        # Check if the input file is a PDF
        if not is_pdf(pdf_file_path):
            log.error(f"Incorrect file type. {pdf_file_path} is not a PDF file.")
            return

        # Check if the PDF is password protected
        password = check_for_password(pdf_file_path)

        # Read tables from the PDF
        table_areas = tabula.read_pdf(pdf_file_path, pages='all', multiple_tables=True, stream=True, password=password)

        # Check if tables were found
        if not table_areas:
            log.info(f"No tables found in {pdf_file_path}")
            return

        # Iterate through each table area and save as CSV
        for i, area in enumerate(table_areas):
            if not area.empty:
                output_file = f"{output_folder_path}/table_{i + 1}.csv"
                area.to_csv(output_file, index=False)
            else:
                log.info(f"Table {i + 1} is empty.")

        log.info(f"Tables extracted successfully.")

    except Exception as e:
        if "Cannot decrypt PDF" in str(e):
            log.error("Incorrect Password! Please try again.")
        else:
            log.exception(f"An error occurred while extracting tables. {e}")
