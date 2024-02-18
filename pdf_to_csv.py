import tabula
from logger import log

import codes


def extract_table_from_pdf(pdf_file_path: str, output_folder_path: str) -> str:

    try:
        table_areas = tabula.read_pdf(pdf_file_path, pages='all', multiple_tables=True, stream=True)
        if not table_areas:
            return codes.TABLE_NOT_FOUND

        for i, area in enumerate(table_areas):
            if not area.empty:
                output_file = f"{output_folder_path}/table_{i + 1}.csv"
                area.to_csv(output_file, index=False)
            else:
                log.info(f"Table {i + 1} is empty.")

        return codes.SUCCESS

    except Exception as e:
        log.exception(e)
        return codes.ERROR
