import os
import sys
import glob

slug = sys.argv[1]

book = False
notebooks = glob.glob("*.ipynb")
if len(notebooks) > 1:
    print(
        "More than one .ipynb notebook found --> assuming this is a book rather than a single notebook"
    )
    book = True

if book is True:
    # build book
    command = "jb build . --config _config.yml --toc _toc.yml"
    os.system(command)
    # build pdf
    command = "jb build . --config _config.yml --toc _toc.yml --builder pdfhtml"
    os.system(command)

    # copy build outputs to 'html' dir
    command = "cp -r '_build/html' html"
    os.system(command)
    command = "cp '_build/pdf/book.pdf' html"
    os.system(command)

else:
    # build single notebook
    command = f"jb build {slug}.ipynb --config _config.yml"
    os.system(command)
    # build pdf
    command = f"jb build {slug}.ipynb --config _config.yml --builder pdfhtml"
    os.system(command)

    # copy build outputs to 'html' dir
    command = f"cp -r '_build/_page/{slug}/html' html"
    os.system(command)
    command = f"cp '_build/_page/{slug}/pdf/{slug}.pdf' html"
    os.system(command)
