from flask import Flask
from flask import render_template, request, redirect, url_for

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def main():
    text = request.form.get('text')
    numeric_string = request.form.get('numeric_string')
    result_text = request.form.get('result_text')
    translate_action = request.form.get('translate_action')
    clear_action = request.form.get('clear_action')

    print('text', text)
    print('numeric_string', numeric_string)
    print('translate_action', translate_action)
    print('clear_action', clear_action)

    result_text = ''
    if not translate_action is None:
        result_text = text + ' MODIFIED'

    if not clear_action is None:
        text = ''
        numeric_string = ''

    return render_template("main.html", text=text, numeric_string=numeric_string, result_text=result_text)

@app.route('/about')
def about():
    return 'Braille Tools Web App'
