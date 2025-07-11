import subprocess
import sys
import glob

slug = sys.argv[1]


def run_command(command, verbose=0):
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except (
        subprocess.CalledProcessError
    ) as e:  # Catching the error if the command fails
        print(f"Error building book: {e.stderr}")
        sys.exit(1)
    if verbose > 0:
        print(f"Output: {result.stdout}")
    return result


book = False
notebooks = glob.glob("*.ipynb")
if len(notebooks) > 1:
    print("More than one .ipynb notebook found --> assuming this is a book")
    book = True

if book is True:
    # build book
    command = ["jb", "build", ".", "--config", "_config.yml", "--toc", "_toc.yml"]
    run_command(command)
    # build pdf
    command = [
        "jb",
        "build",
        ".",
        "--config",
        "_config.yml",
        "--toc",
        "_toc.yml",
        "--builder",
        "pdfhtml",
    ]
    run_command(command)

    # copy build outputs to 'html' dir
    command = ["cp", "-r", "_build/html", "html"]
    run_command(command)
    command = ["cp", "_build/pdf/book.pdf", "html"]
    run_command(command)

else:
    # build single notebook
    command = ["jb", "build", f"{slug}.ipynb", "--config", "_config.yml"]
    run_command(command)
    # build pdf
    command = [
        "jb",
        "build",
        f"{slug}.ipynb",
        "--config",
        "_config.yml",
        "--builder",
        "pdfhtml",
    ]
    run_command(command)

    # copy build outputs to 'html' dir
    command = ["cp", "-r", f"_build/_page/{slug}/html", "html"]
    run_command(command)
    command = ["cp", f"_build/_page/{slug}/pdf/{slug}.pdf", "html"]
    run_command(command)
