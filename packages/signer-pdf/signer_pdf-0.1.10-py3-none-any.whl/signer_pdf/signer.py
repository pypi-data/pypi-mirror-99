import io

import PyPDF2
from pdf2image import convert_from_bytes

import signer_pdf.sign_generator as sign_generator


def sign(name, date, a_hash, position, in_file):



    original = PyPDF2.PdfFileReader(in_file)
    first_page = original.getPage(0)
    page_media = first_page.mediaBox



    pdf_with_signed_page = PyPDF2.PdfFileWriter()
    pdf_with_signed_page.addPage(first_page)
    pdf_with_signed_page_bytes = io.BytesIO()
    pdf_with_signed_page.write(pdf_with_signed_page_bytes)
    pdf_with_signed_page_bytes.seek(0)

    images = convert_from_bytes(pdf_with_signed_page_bytes.read())


    # pdf_with_signed_page_image = Image(file=pdf_with_signed_page_bytes)
    # pdf_with_signed_page_image.convert("png")
    # pdf_with_signed_page_image_bytes = io.BytesIO()
    # pdf_with_signed_page_image.save(file=pdf_with_signed_page_image_bytes)

    signed_page_bytes = sign_generator.convert(name, date, a_hash, position, images[0])


    signed_page = PyPDF2.PdfFileReader(signed_page_bytes).getPage(0)
    (page_width, page_height) = page_media.upperRight
    signed_page.scaleTo(float(page_width), float(page_height))

    output_signed_pdf = PyPDF2.PdfFileWriter()

    for i in range(original.getNumPages()):
        if i == 0:
            output_signed_pdf.addPage(signed_page)
        else:
            page = original.getPage(i)
            output_signed_pdf.addPage(page)

    fp = io.BytesIO()
    output_signed_pdf.write(fp)
    return fp
