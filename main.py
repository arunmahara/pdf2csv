import argparse
from pdf_to_csv import extract_table_from_pdf


def main(pdf_file: str, output_folder: str):
    extract_table_from_pdf(pdf_file, output_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract tables from PDF file.")
    parser.add_argument('-s', '--source', help="Path to the PDF file", dest="pdf_file")
    parser.add_argument('-o', '--output', help="Path to the output folder", dest="output_folder")
    args = parser.parse_args()

    assert args.pdf_file is not None, "Must provide a PDF file!"
    assert args.output_folder is not None, "Must provide a output folder!"

    main(args.pdf_file, args.output_folder)
