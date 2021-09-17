SPACE_BOX_STRING = 'S'
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

def render_box(box_string, box_x_offset, box_y_offset, box_height, box_width):

    output = ''

    for char in '123456':

        output += '\n<circle cx="' + str(box_x_offset + box_width * PROPORTION_BOX_XY_OFFSETS[char]['x']) + '"'
        output += ' cy="' + str(box_y_offset + box_width * PROPORTION_BOX_XY_OFFSETS[char]['y']) + '"'

        if char in box_string:
            output += ' r="' + str(box_width * PROPORTION_OFFSET_DOT_RADIUS) + '"'
        else:
            output += ' r="' + str(box_width * PROPORTION_OFFSET_NODOT_RADIUS) + '"'

        output += ' fill="black" />'

    return output

def render_page(page_string, box_height, box_width, boxes_per_row):

    output = '<svg width="' + str(box_width * boxes_per_row) + '" height="' + str(box_height * len(page_string)) + '" xmlns="http://www.w3.org/2000/svg">'

    box_string_list = []
    box_string_build = ''

    for char in page_string + ' ':
        if char == ' ':
            box_string_list.append(str(box_string_build))
            box_string_build = ''
        else:
            box_string_build += char

    box_x_offset = 0
    box_y_offset = 0
    box_count = 0

    for box_string in box_string_list:

        box_count += 1

        output += render_box(box_string, box_x_offset, box_y_offset, box_height, box_width)

        if box_count == boxes_per_row:
            box_x_offset = 0
            box_y_offset += box_height
            box_count = 0
        else:
            box_x_offset += box_width

    output += '\n</svg>'

    return output

if __name__ == "__main__":

    page_string = '1235 24 1234 S 356 123456 S 2456 23 145 1235 24 1234 S 356 123456 S 2456 23 145 1235 24 1234 S 356 123456 S 2456 23 145' 
    box_height = 60
    box_width = 40
    boxes_per_row = 12
    svg_text = render_page(page_string, box_height, box_width, boxes_per_row)
    with open('page.svg', 'w') as f:
        f.write(svg_text)