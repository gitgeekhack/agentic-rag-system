import fitz
import logging
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app import textract_client, anthropic_llm

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    document = fitz.open(pdf_path)
    raw_text = ""
    for page_number in range(len(document)):
        logging.info(f"Processing page {page_number + 1}...")
        page = document[page_number]
        image_bytes = get_image_bytes(page)
        response = extract_text_from_image(image_bytes)

        # Iterate over the blocks in the response
        for item in response['Blocks']:
            # Only extract 'LINE' blocks which represent individual lines of text
            if item['BlockType'] == 'LINE':
                raw_text += item['Text'] + ' '

    return raw_text

def get_image_bytes(page):
    """Get image bytes from the page object."""
    zoom = 2  # to increase the resolution of image
    matrix = fitz.Matrix(zoom, zoom)
    image = page.get_pixmap(matrix=matrix)
    image_bytes = image.tobytes(output="png")
    return image_bytes

def extract_text_from_image(image_bytes):
    """
    :param image_bytes: bytes array of image
    :return: response object of extracted text from textract using image bytes
    """
    try:
        response = textract_client.detect_document_text(
            Document={
                'Bytes': image_bytes,
            },
        )
        return response
    except Exception as e:
        logging.error(f"Error in Textract call: {e}")
        return None

def data_formatter(raw_text):
    """ This method is used to format the data and prepare chunks """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=15000, chunk_overlap=200
    )

    texts = text_splitter.split_text(raw_text)

    for text in texts:
        threshold = anthropic_llm.get_num_tokens(text)
        if threshold > 5000:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=10000, chunk_overlap=200
            )
            texts = text_splitter.split_text(raw_text)
            break

    docs = [Document(page_content=t) for t in texts]
    return docs
