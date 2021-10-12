import unidecode

SPACE_TOKEN = 'S'
NEWLINE_BOX = 'NL'
NEWPAGE_BOX = 'NP'

PROPORTION_OFFSET_TOP = 20 / 100
PROPORTION_OFFSET_LEFT = 30 / 100
PROPORTION_OFFSET_DOT_RADIUS = 10 / 100
PROPORTION_OFFSET_NODOT_RADIUS = 1 / 100

PROPORTION_BOX_XY_OFFSETS = {
    '1': {
        'x': PROPORTION_OFFSET_LEFT,
        'y': PROPORTION_OFFSET_TOP
    },
    '2': {
        'x': PROPORTION_OFFSET_LEFT,
        'y': 0.5
    },
    '3': {
        'x': PROPORTION_OFFSET_LEFT,
        'y': 1 - PROPORTION_OFFSET_TOP
    },
    '4': {
        'x': 1 - PROPORTION_OFFSET_LEFT,
        'y': PROPORTION_OFFSET_TOP
    },
    '5': {
        'x': 1 - PROPORTION_OFFSET_LEFT,
        'y': 0.5
    },
    '6': {
        'x': 1 - PROPORTION_OFFSET_LEFT,
        'y': 1 - PROPORTION_OFFSET_TOP
    }
}

def render_box(box_dict, box_x_offset, box_y_offset, box_height, box_width, write_original_text):

    box_string = box_dict['box']
    box_desc = box_dict['desc']

    output = ''

    for char in '123456':

        output += '\n<circle cx="' + str(box_x_offset + box_width * PROPORTION_BOX_XY_OFFSETS[char]['x']) + '"'
        output += ' cy="' + str(box_y_offset + box_width * PROPORTION_BOX_XY_OFFSETS[char]['y']) + '"'

        if char in box_string:
            output += ' r="' + str(box_width * PROPORTION_OFFSET_DOT_RADIUS) + '"'
        else:
            output += ' r="' + str(box_width * PROPORTION_OFFSET_NODOT_RADIUS) + '"'

        output += ' fill="black" />'

    if write_original_text:
        decoded_box_desc = unidecode.unidecode(box_desc)
        output += '<text x="' + str(box_x_offset + round(box_width / 4) ) + '" y="' + str(box_y_offset + round(box_height * 0.8)) + '" font-size="' + str(round(box_height / 6)) + '">' + decoded_box_desc + '</text>'

    return output

def render_pages(box_list, box_height, boxes_per_row, rows_per_page, left_margin, top_margin, write_original_text=True):

    book = []

    box_width = round(box_height * (2/3))

    page_output = ''

    box_x_offset = left_margin
    box_y_offset = top_margin
    box_count = 0

    row_index = 0

    for box_dict in box_list:

        box_string = box_dict['box']
        box_count += 1

        if box_string not in (NEWLINE_BOX,NEWPAGE_BOX):
            page_output += render_box(box_dict, box_x_offset, box_y_offset, box_height, box_width, write_original_text)

        if box_count == boxes_per_row or box_string == NEWLINE_BOX:
            box_x_offset = left_margin
            box_y_offset += box_height
            box_count = 0
            row_index +=1
        else:
            box_x_offset += box_width

        if row_index > rows_per_page or box_string == NEWPAGE_BOX:
            row_index = 0
            svg_header = '<svg width="' + str(box_width * boxes_per_row + left_margin * 2) + '" height="' + str((rows_per_page + 2) * box_height) + '" xmlns="http://www.w3.org/2000/svg">'
            page_output += '\n</svg>'
            book.append(svg_header + page_output)
            box_x_offset = left_margin
            box_y_offset = top_margin
            page_output = ''

    page_output += '\n</svg>'

    svg_header = '<svg width="' + str(box_width * boxes_per_row + left_margin * 2) + '" height="' + str((rows_per_page + 2) * box_height) + '" xmlns="http://www.w3.org/2000/svg">'

    book.append(svg_header + page_output)

    return book

if __name__ == "__main__":

    #page_string = '1235 24 1234 S 356 123456 S 2456 23 145 1235 NL 24 1234 S 356 NL 123456 S 2456 23 145 1235 24 1234 S 356 123456 S 2456 23 145' 
    box_list = [{'box': '3456', 'desc': 'NUM'}, {'box': '46', 'desc': 'MAY'}, {'box': '15', 'desc': 'E'}, {'box': '234', 'desc': 's'}, {'box': '2345', 'desc': 't'}, {'box': '135', 'desc': 'o'}, {'box': 'S', 'desc': 'ESPACIO'}, {'box': '3456', 'desc': 'NUM'}, {'box': '15', 'desc': 'e'}, {'box': '234', 'desc': 's'}, {'box': 'S', 'desc': 'ESPACIO'}, {'box': '3456', 'desc': 'NUM'}, {'box': '15', 'desc': 'e'}, {'box': '123', 'desc': 'l'}, {'box': 'S', 'desc': 'ESPACIO'}, {'box': '3456', 'desc': 'NUM'}, {'box': '46', 'desc': 'MAY'}, {'box': '12456', 'desc': 'Ñ'}, {'box': '1', 'desc': 'a'}, {'box': '1345', 'desc': 'n'}, {'box': '145', 'desc': 'd'}, {'box': '23456', 'desc': 'ú'}, {'box': 'S', 'desc': 'ESPACIO'}, {'box': '3456', 'desc': 'NUM'}, {'box': '1345', 'desc': 'n'}, {'box': '23456', 'desc': 'ú'}, {'box': '134', 'desc': 'm'}, {'box': '15', 'desc': 'e'}, {'box': '1235', 'desc': 'r'}, {'box': '135', 'desc': 'o'}, {'box': 'S', 'desc': 'ESPACIO'}, {'box': '12', 'desc': '2'}, {'box': '245', 'desc': '0'}, {'box': 'S', 'desc': 'ESPACIO'}, {'box': '3456', 'desc': 'NUM'}, {'box': '15', 'desc': 'e'}, {'box': '1345', 'desc': 'n'}, {'box': 'S', 'desc': 'ESPACIO'}, {'box': '3456', 'desc': 'NUM'}, {'box': '123', 'desc': 'l'}, {'box': '1', 'desc': 'a'}, {'box': 'S', 'desc': 'ESPACIO'}, {'box': '3456', 'desc': 'NUM'}, {'box': '123', 'desc': 'l'}, {'box': '24', 'desc': 'i'}, {'box': '234', 'desc': 's'}, {'box': '2345', 'desc': 't'}, {'box': '1', 'desc': 'a'}, {'box': '3', 'desc': '.'}, {'box': 'S', 'desc': 'ESPACIO'}]
    box_height = 60
    boxes_per_row = 12
    rows_per_page = 30
    svg_text = render_pages(box_list, box_height, boxes_per_row, rows_per_page)
    with open('page.svg', 'w') as f:
        f.write(svg_text)