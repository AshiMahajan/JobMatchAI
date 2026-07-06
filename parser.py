import pdfplumber

from docx import Document

from core.logger import logger


def extract_text_from_pdf(
        pdf_path: str
) -> str:

    text = ""

    try:

        with pdfplumber.open(
                pdf_path
        ) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:

                    text += page_text + "\n"

        return text

    except FileNotFoundError as error:

        logger.error(
            "PDF file not found: %s",
            pdf_path
        )

        raise RuntimeError(
            "Uploaded PDF could not be found."
        ) from error

    except Exception as error:

        logger.error(
            "Failed to parse PDF: %s",
            pdf_path
        )

        raise RuntimeError(
            "Unable to read the uploaded PDF."
        ) from error


def extract_text_from_docx(
        docx_path: str
) -> str:

    try:

        document = Document(
            docx_path
        )

        return "\n".join(

            paragraph.text

            for paragraph in document.paragraphs

        )

    except FileNotFoundError as error:

        logger.error(
            "DOCX file not found: %s",
            docx_path
        )

        raise RuntimeError(
            "Uploaded DOCX could not be found."
        ) from error

    except Exception as error:

        logger.error(
            "Failed to parse DOCX: %s",
            docx_path
        )

        raise RuntimeError(
            "Unable to read the uploaded DOCX."
        ) from error