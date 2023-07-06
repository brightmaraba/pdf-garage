"""
A module that uses pikepfdf and pdf2image to split a pdf into multiple
pdfs and convert each pdf to a png image.
To use - Install pikepdf and pdf2image using pip or other package manager.
    - Create a source directory and add the pdf to be split to it.-
    - Create a dest directory to save the split pdfs to.
    - Create an images_dir directory to save the converted images to.
    - Update the source_pdf, dest_dir and images_dir variables to
    point to the correct directories.
    - Put source pdfs to split in the source directory.
    - Update the file2pages dictionary to map the pdfs to
    split and the page ranges to split them into.
"""

import os
from pikepdf import Pdf
from pdf2image import convert_from_path

# Path to the pdf to split and the directory to save the split pdfs to.

this_dir = os.path.dirname(os.path.abspath(__file__))
source_pdf = os.path.join(this_dir, "source", "nominees.pdf")
dest_dir = os.path.join(this_dir, "dest")
images_dir = os.path.join(this_dir, "images_dir")

"""
Mappping of pdfs to split and the page ranges to split them into.
- The key is the index of the pdf to split.
- The value is a list of the first and last page to split the pdf into.
- Important: The last page is not included in the split.
"""

file2pages = {
    0: [0, 1],
    1: [1, 2],
    2: [2, 3],
    3: [3, 4],
    4: [4, 5],
}

# Load PDF File to be split.
pdf_file = Pdf.open(source_pdf)


# Set up Split PDF File into multiple PDFs.
new_pdf_files = [Pdf.new() for _ in file2pages]
new_pdf_index = 0


def split_pdf(pdf_file, file2pages, new_pdf_files, new_pdf_index):
    """Function to split a PDF into multiple PDFs."""
    for n, page in enumerate(pdf_file.pages):
        if n in list(range(*file2pages[new_pdf_index])):
            new_pdf_files[new_pdf_index].pages.append(page)
            print(f"Page {n} added to PDF {new_pdf_index}")
        else:
            # Create new name of file
            name, ext = "page", (os.path.splitext(source_pdf)[1])
            output_pdf_filename = f"{name}_{new_pdf_index}{ext}"
            # Save PDF File.
            new_pdf_files[new_pdf_index].save(
                os.path.join(dest_dir, output_pdf_filename)
            )
            print(f"[+] PDF {new_pdf_index} saved to {output_pdf_filename}")
            # Increment to next PDF file.
            new_pdf_index += 1
            # Add the 'nth' page to the new PDF file.
            new_pdf_files[new_pdf_index].pages.append(page)
            print(f"[*] Assinging page {n} to PDF File {new_pdf_index}")

    # Save the last PDF file.
    name, ext = "page", (os.path.splitext(source_pdf)[1])
    output_pdf_filename = f"{name}_{new_pdf_index}{ext}"
    new_pdf_files[new_pdf_index].save(
        os.path.join(dest_dir, output_pdf_filename)
    )  # noqa
    print(f"[+] File: {output_pdf_filename} saved.")


def conver_pdf_to_image(source_pdf_file):
    """Function to convert pdfs to PNF images."""
    images = convert_from_path(source_pdf_file, dpi=500)
    for i in range(len(images)):
        images[i].save(os.path.join(images_dir, f"page_{i}.png"), "PNG")
        print(f"[+] Image {i} saved.")
    print("[+] All images saved.")


if __name__ == "__main__":
    """Run the script."""
    try:
        split_pdf(pdf_file, file2pages, new_pdf_files, new_pdf_index)
        pdf_files = os.listdir(dest_dir)
        conver_pdf_to_image(source_pdf)
    except Exception as e:
        print(f"[-] Error: {e}")
