import json

from flask import Flask, render_template, request, redirect, url_for

from json_search import JsonSearch

app = Flask(__name__)

with open('json/SSR.json', 'r', encoding='utf-8') as f:
    ssr_data = json.load(f)
with open('json/SR.json', 'r', encoding='utf-8') as f:
    sr_data = json.load(f)
with open('json/R.json', 'r', encoding='utf-8') as f:
    r_data = json.load(f)
with open('json/N.json', 'r', encoding='utf-8') as f:
    n_data = json.load(f)

json_dict = {'SSR': ssr_data, 'SR': sr_data, 'R': r_data, 'N': n_data}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/89')
def test():
    return '一体感！'


@app.route("/result", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':

        name = request.form['name']
        skill = request.form['skill']
        talent = request.form['talent']
        cinderella = request.form['cinderella']

        search_rank = request.form.getlist('rare')
        search_element = request.form.getlist('element')

        # レア度をここで弾いている
        search_json_data = [[i, json_dict[i]] for i in search_rank]

        json_search = JsonSearch(search_json_data)
        json_search.search_element(search_element)
        json_search.search_name(name)
        json_search.search_skill(skill)
        json_search.search_talent(talent)
        json_search.search_cinderella_card(cinderella)

        if not json_search.search_json_data:
            json_search.search_json_data.append('検索結果なし')

        return render_template('index.html', result=json_search.search_json_data, skill=skill, talent=talent,
                               cinderella=cinderella)
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
