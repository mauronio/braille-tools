from os import replace
from . import basic_alphabet as alphabet
import re

TOKEN_NEWLINE = '\n'
TOKEN_NEWPAGE = '--'

word_pattern = re.compile(alphabet.word_regexp)
number_pattern = re.compile(alphabet.number_regexp)

def process_char(char):

    if char == '\r':
        return []

    if char == TOKEN_NEWLINE:
        return [{'box': 'NL', 'desc': 'NL'}]

    if char.isupper():
        prefix = {'box': alphabet.uppercase_prefix, 'desc': alphabet.uppercase_description}
    else:
        prefix = None

    box_text = alphabet.alphabet_castillian.get(char.lower())

    if box_text is None:
        box = {'box': alphabet.error_box, 'desc': alphabet.error_description}
    else:
        box = {'box': box_text, 'desc': char}
    
    if not prefix is None:
        return [prefix, box]
    else:
        return [box]

def process_token(token, previous_token):
    print(token)

    if token == TOKEN_NEWPAGE and previous_token == TOKEN_NEWLINE:

        return [{'box': 'NP', 'desc': 'New Page'}]

    elif token == TOKEN_NEWLINE and previous_token == TOKEN_NEWPAGE:

        return []

    else:

        output = []

        number_match = number_pattern.match(token)

        if number_match is None:
            prefix = None
        else:
            prefix = {'box': alphabet.number_prefix, 'desc': alphabet.number_description}

        output_char = []
        for char in token:
            output_char += process_char(char)

        if not prefix is None:
            output += [prefix]

        output += output_char

        return output
    

def process_text(text):

    output = []

    token_list = []
    current_token = ''
    for char in text:
        if char == ' ' or char == TOKEN_NEWLINE:

            if len(current_token) > 0:
                token_list.append(current_token)
                current_token = ''

            token_list.append(char)

        elif char != '\r':

            current_token += char

    if len(current_token) > 0:
        token_list.append(current_token)

    previous_token = None    
    for token in token_list:
        numeric_box = process_token(token, previous_token)
        output += numeric_box
        previous_token = token

    print('token_list', token_list)
    print('output', output)

    return output


if __name__ == "__main__":

    text = 'Esto es el Ñandú número 20 en la lista.'

    output_list = process_text(text)

    print(output_list)
