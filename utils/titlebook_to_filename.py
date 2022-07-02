import string

"""Fonction permettant de modifier le nom du livre afin qu'il soit
adapté au nommage sur windows en enlevant les caractères spéciaux
"""


def title_book_to_file_name(titlebook):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in titlebook if c in valid_chars)
    filename = filename.replace(' ', '_')
    return filename