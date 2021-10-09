from flask import Flask
from flask import render_template, request, redirect, url_for, send_from_directory, current_app

import render.svg_builder as svg_builder
import translator.simple_engine as engine
import os

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

from PyPDF2 import PdfFileMerger

DEFAULT_BOX_HEIGHT = 60
DEFAULT_BOXES_PER_ROW = 40
DEFAULT_ROWS_PER_PAGE = 30

app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['POST', 'GET'])
def main():
    input_text = request.form.get('input_text')
    if input_text is None:
        input_text = ''

    box_height = request.form.get('box_height', DEFAULT_BOX_HEIGHT)
    boxes_per_row = request.form.get('boxes_per_row', DEFAULT_BOXES_PER_ROW)
    rows_per_page = request.form.get('rows_per_page', DEFAULT_ROWS_PER_PAGE)

    numeric_string = request.form.get('numeric_string')
    translate_action = request.form.get('translate_action')
    clear_action = request.form.get('clear_action')
    form_dict = request.form.to_dict(flat=False)
    print ("form_dict", form_dict)
    show_text = form_dict.get('show_text')
    if show_text is None:
        checked_value = ''
        write_original_text = False
    else:
        checked_value = 'checked'
        write_original_text = True
        
    print('input text', input_text)
    print('numeric_string', numeric_string)
    print('translate_action', translate_action)
    print('clear_action', clear_action)

    rendered_book = []

    if not clear_action is None:
        input_text = ''
        rendered_book = []
        translate_action = 'OK'

    if not translate_action is None:
        raw_translation = engine.process_text(input_text)
        rendered_book = svg_builder.render_pages(raw_translation, int(box_height), int(boxes_per_row), int(rows_per_page), write_original_text)
        pdf_page_list = []
        for i in range(1, len(rendered_book) + 1):
            rendered_page = rendered_book[i-1] 
            with open('static/translation_' + str(i) + '.svg', 'w') as f:
                f.write(rendered_page)

            drawing = svg2rlg(os.path.join(current_app.root_path, 'static', 'translation_' + str(i) + '.svg'))
            pdf_filepath = os.path.join(current_app.root_path, 'static', 'translation_' + str(i) + '.pdf')
            renderPDF.drawToFile(drawing, pdf_filepath)
            pdf_page_list.append(pdf_filepath)

        merger = PdfFileMerger()

        for pdf in pdf_page_list:
            merger.append(pdf)
        merger.write(os.path.join(current_app.root_path, 'static', 'translation.pdf'))
        merger.close()

    print ('rendered_book len', len(rendered_book))
    return render_template("main.html", text=input_text, book=rendered_book, book_length=len(rendered_book), box_height=box_height, boxes_per_row = boxes_per_row, rows_per_page = rows_per_page, checked_value=checked_value)

@app.route('/about')
def about():
    return 'Braille Tools Web App'

@app.route('/static/translation_svg', methods=['GET', 'POST'])
def download_SVG():
    public_folder = os.path.join(current_app.root_path, 'static')
    # Returning file from appended path
    return send_from_directory(public_folder, 'translation.svg')

@app.route('/static/translation_pdf', methods=['GET', 'POST'])
def download_PDF():
    public_folder = os.path.join(current_app.root_path, 'static')
    # Returning file from appended path
    return send_from_directory(public_folder, 'translation.pdf')