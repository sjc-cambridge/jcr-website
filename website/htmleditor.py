from bs4 import BeautifulSoup
import os
import pathlib

class HTMLParser:
    """
    Class can be used to parse html files, snipping out important bits e.g. mains.
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
        """Translate the next sequence of characters into a symbol."""
        while self.current_5chars != '<main':
            self.update_characters()
        return self.char_no

    def get_main_end(self):
        """Translate the next sequence of characters into a symbol."""
        while self.current_5chars != '/main':
            self.update_characters()
        return self.char_no

    def strip_main(self):
        """Stip HTML to leave contents of main behind"""
        start_ind = self.get_main_start()
        end_ind = self.get_main_end()
        #snipped_html = """"""
        snipped_html = html_scanner.text_file[start_ind-5:end_ind+1]
        snipped_html = snipped_html.replace('\\n', ' ')
        snipped_html = BeautifulSoup(snipped_html, 'html.parser')

        snipped_html= snipped_html.prettify('utf-8')
        print(snipped_html)
        with open(self.path,'wb') as html_file:
            html_file.write(snipped_html)

        return 'Snipped {}'.format(self.path)

curr_dir = os.path.dirname(__file__)

path = pathlib.Path(os.path.join(curr_dir,'templates2'))

'''Act on all files within top directory and next level
    (avoiding static content at level 3!)'''

for entry in path.iterdir():
    if entry.is_file():
        print(entry)
        html_scanner = HTMLParser(str(entry))
        html_scanner.strip_main()
    else:
        path2 = pathlib.Path(entry)
        for entry2 in path2.iterdir():
            if entry2.is_file():
                print(entry2)
                html_scanner = HTMLParser(str(entry2))
                html_scanner.strip_main()
