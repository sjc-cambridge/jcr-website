from bs4 import BeautifulSoup
import os
from pathlib import Path
import shutil

class HTMLParser:
    """
    Class can be used to bulk edit the html files created by exporting with
    Bootstrap studio, converting them to use jinja syntax. Make sure your main
    page content is within a main element and that you give your page header
    container the id 'headerbox'.
    """

    def __init__(self, path):
        self.path = path
        self.extension = "{% extends 'shared/_layout.j2.html' %}\n\n"
        self.title = "{% block title %}\n"
        self.header = "{% block header %}\n"
        self.edited_html = ""
        self.snipped_main = "{% block main %}\n"
        with open(self.path, encoding="utf-8") as html_file:
            self.text_file = html_file.read()

    def make_title(self):
        self.title += "<title>St. John's JCR </title>"
        self.title += "\n{% endblock %}\n\n"

    def make_header(self):
        with open(self.path):
            soup = BeautifulSoup(self.text_file, "html.parser")
            heading = soup.find(id="headerbox")
            self.header += "{}\n".format(heading)
            self.header += "{% endblock %}\n\n"

    def get_main_start(self):
        """Find end of main."""
        return self.text_file.find("<main")

    def get_main_end(self):
        """Find end of main."""
        return self.text_file.find("/main>") + 6

    def strip_main(self):
        """Stip HTML to leave contents main behind, add jinja main syntax."""
        start_ind = self.get_main_start()
        end_ind = self.get_main_end()
        self.snipped_main += self.text_file[start_ind:end_ind]
        self.snipped_main += """\n{% endblock %}"""

    def modify_template(self):
        self.make_title()
        self.make_header()
        self.strip_main()
        self.edited_html += self.extension
        self.edited_html += self.title
        self.edited_html += self.header
        self.edited_html += self.snipped_main
        self.edited_html = self.edited_html.replace("\\n", " ")
        self.edited_html = BeautifulSoup(self.edited_html, "html.parser")
        self.edited_html = self.edited_html.prettify("utf-8")
        with open(self.path, "wb") as html_file:
            html_file.write(self.edited_html)  # Write HTML
        return "Snipped {}".format(self.path)


def file_recurse(func, directory_path):
    """Function for recursively operating on all files
        in a directory w/ exceptions.
    """
    path = Path(directory_path)
    for filepath_obj in path.iterdir():
        filepath = str(filepath_obj)
        if filepath_obj.is_file():
            if file_is_exempt(filepath):
                pass
            else:
                func(filepath)
        else:
            path2 = Path(filepath)
            file_recurse(func, path2)
    return


def file_is_exempt(filepath):
    """Check if file is static content or jinja stuff
    """
    if ".DS_Store" in filepath or "assets" in filepath or "shared" in filepath or "j2.html" in filepath:
        return True
    else:
        return False


def jinjafy_html(filepath):
    """Jinjafies html file to extend from shared/_layout.j2.html
    """
    if ".html" in filepath and ".j2.html" not in filepath:  # If
        html_parser = HTMLParser(filepath)
        html_parser.modify_template()
        jinja_filepath = filepath.replace(".html", ".j2.html")
        os.rename(filepath, jinja_filepath)
        return "Jinjafied {}".format(filepath)


def get_file_array(dir, regex_pattern):
    """Return an array of filepaths within a directory that match given pattern
    """
    files = []
    files_generator = Path(dir).glob(regex_pattern)
    for file in files_generator:
        files.append(str(file))
    return files


def copy_over_only_new_files(src_dir, dst_dir, regex_pattern="**/*.*"):
    """Recursively copies files from one directory into another
    It only copies files that do not exist in the destionation
    """
    src_files = get_file_array(src_dir, regex_pattern)
    dst_files = get_file_array(dst_dir, regex_pattern)

    for src_file in src_files:
        potential_dst_file = src_file.replace(src_dir, dst_dir, 1)

        if potential_dst_file not in dst_files:
            print("Copying new file:\n {} >> {}\n".format(
                src_file, potential_dst_file))
            shutil.copy(src_file, potential_dst_file)
        else:
            # file exists already >> skip
            pass


# define directory paths
script_dir = os.path.dirname(__file__)
parent_dir = Path(script_dir).parent

templates_dir = os.path.join(parent_dir, "website/templates")
assets_dir = os.path.join(parent_dir, "website/assets")

templates_og_dir = os.path.join(parent_dir, "website/templates_og")

templates_temp_dir = os.path.join(parent_dir, "website/templates_temp")
assets_temp_dir = os.path.join(templates_temp_dir, "assets")

# file manipulation
try:
    shutil.rmtree(templates_temp_dir)
    print("Removed old temp directory\n")
except:
    print("No temp directory exists yet\n")

print("Creating templates_temp directory\n")
shutil.copytree(templates_og_dir, templates_temp_dir)

print("Copying over any new assets\n")
copy_over_only_new_files(assets_temp_dir, assets_dir)

print("Jinjafying html files\n")
file_recurse(jinjafy_html, templates_temp_dir)

print("Copying over any new pages\n")
copy_over_only_new_files(templates_temp_dir, templates_dir, "**/*.j2.html")

print("Removing temp directory\n")
shutil.rmtree(templates_temp_dir)
