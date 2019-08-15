from bs4 import BeautifulSoup
import os
import pathlib


class HTMLParser:
    """
    Class can be used to parse html files, snipping out important bits e.g. mains
    and stitching jinja in.
    """
    def __init__(self, path):
        """Open specified file and initialise reserved words and IDs.
        Initialise grammar, comment start/end strings.
        """
        self.path = path
        self.next_character = ""
        self.current_character = ""
        self.previous_character = ""
        self.prev2_character = ""
        self.prev3_character = ""
        self.current_5chars = ""
        self.char_no = 1
        with open(path, encoding="utf-8") as html_file:
            self.text_file = html_file.read()


    def reset_file(self):
        """Return text file pointer to start."""
        self.text_file.seek(0)
        self.char_no = 1

    def read_character(self):
        """Read next character.
        """
        character = self.text_file[self.char_no]
        self.char_no +=1
        return character

    def update_characters(self):
        """Cyclic update of characters that are being kept track of."""
        self.prev3_character = self.prev2_character
        self.prev2_character = self.previous_character
        self.previous_character = self.current_character
        self.current_character = self.next_character
        self.next_character = self.read_character()
        self.current_5chars = str(self.prev3_character)+str(self.prev2_character)+str(self.previous_character)+str(self.current_character)+str(self.next_character)

    def get_main_start(self):
        """Find start of main."""
        while self.current_5chars != '<main':
            self.update_characters()
        return self.char_no

    def get_main_end(self):
        """Find end of main."""
        while self.current_5chars != '/main':
            self.update_characters()
        return self.char_no

    def strip_main(self):
        """Stip HTML to leave contents of main behind"""
        start_ind = self.get_main_start()
        end_ind = self.get_main_end()
        snipped_html = """{% block main %}\n"""
        snipped_html += self.text_file[start_ind-5:end_ind+1]
        snipped_html += """\n{% endblock %}"""
        snipped_html = snipped_html.replace('\\n', ' ')
        snipped_html = BeautifulSoup(snipped_html, 'html.parser')

        snipped_html= snipped_html.prettify('utf-8')
        with open(self.path,'wb') as html_file:
            html_file.write(snipped_html)

        return 'Snipped {}'.format(self.path)


def file_recurse(func, directory_path, exceptions):
    '''Function for recursively operating on all files in a directory w/ exceptions.
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
