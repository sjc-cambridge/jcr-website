from bs4 import BeautifulSoup
import os
import pathlib
import shutil

class HTMLParser:
    """
    Class can be used to parse html files, snipping out important bits e.g. mains
    and stitching jinja in.
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
        self.title += "<title>St. John's JCR</title>"
        self.title += "\n{% endblock %}\n\n"

    def make_header(self):
        with open(self.path) as html_file:
            soup = BeautifulSoup(self.text_file, 'html.parser')
            heading = soup.find(id='headerbox')
            self.header += f"{heading}\n"
            self.header += "{% endblock %}\n\n"

    def get_main_start(self):
        """Find end of main."""
        return self.text_file.find('<main')

    def get_main_end(self):
        """Find end of main."""
        return self.text_file.find('/main>') + 6

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
        self.edited_html = self.edited_html.replace('\\n', ' ')
        self.edited_html = BeautifulSoup(self.edited_html, 'html.parser')
        self.edited_html = self.edited_html.prettify('utf-8')
        with open(self.path,'wb') as html_file:
            html_file.write(self.edited_html)  # Write HTML
        return 'Snipped {}'.format(self.path)


def file_recurse(func, directory_path, exceptions):
    '''Function for recursively operating on all files
        in a directory w/ exceptions.
    '''
    path = pathlib.Path(directory_path)
    for filepath_obj in path.iterdir():
        filepath = str(filepath_obj)
        print(filepath)
        if filepath_obj.is_file():
            if filepath not in exceptions:
                func(filepath)
            else:
                pass
        else:
            path2 = pathlib.Path(filepath)
            file_recurse(func, path2, exceptions)
    return

exceptions_list = []

def assets_finder(filepath):
    '''Check if file is static content or jinja stuff'''
    if '.DS_Store' in filepath or 'assets' in filepath or 'shared' in filepath or 'j2.html' in filepath:
        exceptions_list.append(filepath)
    else:
        return None

def jinjafy_html(filepath):
    html_parser = HTMLParser(filepath)
    html_parser.modify_template()

def jinja_rename(filepath):
    if '.j2.html' not in filepath:  # If not already renamed
        jinja_filepath = filepath.replace(".html", ".j2.html")
        os.rename(filepath, jinja_filepath)
    return 'Renamed {}'.format(filepath)

curr_dir = os.path.dirname(__file__)
templates_og_path = os.path.join(curr_dir,'templates_og')  # Templates before jinjafication from BSS.
templates_path = os.path.join(curr_dir,'templates')

try:
    shutil.copytree(templates_og_path, templates_path)  # Make copy of og templates and move to templates folder.
except Exception as e:
    print(e)  # Directory already exists

file_recurse(assets_finder, templates_path, [])  # Build list of assets file paths by recursion

file_recurse(jinjafy_html, templates_path, exceptions_list)  # Jinja stitching with exceptions

file_recurse(jinja_rename, templates_path, exceptions_list)  # Renaming files to j2.html to show use of Jinja 2.
