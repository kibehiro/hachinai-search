import re

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/result')
def search():
    if request.method == 'GET':

        card_name = re.split(r'\s+', request.args.get('card_name'))
        cinderella_card_name = re.split(r'\s+', request.args.get('cinderella_card'))
        skill_name = re.split(r'\s+', request.args.get('skill_name'))
        ability_name = re.split(r'\s+', request.args.get('ability_name'))

        rare_list = request.args.getlist('rare')
        attribute_list = request.args.getlist('attribute')

        return 'hoge'
    else:
        return redirect(url_for('/'))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
