from bs4 import BeautifulSoup
import os
import pathlib


class HTMLParser:
    """
    Class can be used to parse html files, snipping out important bits e.g. mains
    and stitching jinja in.
    """
    def __init__(self, path):
        self.path = path
        with open(path, encoding="utf-8") as html_file:
            self.text_file = html_file.read()

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
        snipped_html = """{% block main %}\n"""
        snipped_html += self.text_file[start_ind:end_ind]
        snipped_html += """\n{% endblock %}"""
        snipped_html = snipped_html.replace('\\n', ' ')  # Remove newline chars
        snipped_html = BeautifulSoup(snipped_html, 'html.parser')  # Prettify HTML
        snipped_html= snipped_html.prettify('utf-8') # Re-encode HTML
        with open(self.path,'wb') as html_file:
            html_file.write(snipped_html)  # Write HTML
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
    '''Check if file is static content'''
    if 'assets' in filepath:
        exceptions_list.append(filepath)
    else:
        return None

def chop_main(filepath):
    html_scanner = HTMLParser(filepath)
    html_scanner.strip_main()

curr_dir = os.path.dirname(__file__)

templates_path = os.path.join(curr_dir,'templates2')


file_recurse(assets_finder, templates_path, [])  # Build list of assets file paths by recursion

file_recurse(chop_main, templates_path, exceptions_list)  # Jinja stitching with exceptions
