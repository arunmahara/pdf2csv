import tabula
import PyPDF2
import logging
from getpass import getpass


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s: %(levelname)s: %(filename)s-%(lineno)s: %(message)s'
)
log = logging.getLogger(__name__)


def is_pdf_password_protected(pdf_file_path: str) -> bool:
    with open(pdf_file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        if reader.is_encrypted:
            return True
        else:
            return False


def extract_table_from_pdf(pdf_file_path: str, output_folder_path: str) -> str:

    try:

        password = None
        if is_pdf_password_protected(pdf_file_path):
            log.info(f"PDF {pdf_file_path} is password protected.")
            password = getpass("Enter the password: ")

        table_areas = tabula.read_pdf(pdf_file_path, pages='all', multiple_tables=True, stream=True, password=password)
        if not table_areas:
            log.info(f"No tables found in {pdf_file_path}")
            return

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
