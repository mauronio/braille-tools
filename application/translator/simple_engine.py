from . import basic_alphabet as alphabet
import re

word_pattern = re.compile(alphabet.word_regexp)
number_pattern = re.compile(alphabet.number_regexp)

def process_char(char):

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

def process_token(token):

    output = []

    print(token)

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

    token_list = text.split(' ')
    for token in token_list:
        numeric_box = process_token(token)
        output += numeric_box
        output += [alphabet.space_dict]

    return output


if __name__ == "__main__":

    text = 'Esto es el Ñandú número 20 en la lista.'

    output_list = process_text(text)

    print(output_list)
