from pdf_to_csv import extract_table_from_pdf
from logger import log


def main():
    response = extract_table_from_pdf("example_pdfs/pdf2.pdf", ".")
    log.info(response)


if __name__ == "__main__":
    main()
