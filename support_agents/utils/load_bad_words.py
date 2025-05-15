import os

#returning bad words from bad_words.txt file
def load_bad_words(file_path=None):
    default_path = os.path.join(os.path.dirname(__file__), '../config/bad_words.txt')
    path = file_path or default_path

    try:
        with open(path, 'r', encoding='utf-8') as file:
            return set(line.strip().lower() for line in file if line.strip())
    except FileNotFoundError:
        return set()
