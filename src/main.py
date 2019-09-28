import json

from flask import Flask, render_template, request, redirect, url_for

from src.json_search import JsonSearch

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
    search_data = []
    return render_template('index.html', search_data=search_data)


@app.route('/89')
def test():
    return '一体感！'


@app.route("/result", methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        name = request.args.get('name')
        skill = request.args.get('skill').split()
        talent = request.args.get('talent').split()
        cinderella = request.args.get('cinderella')

        search_rank = request.args.getlist('rare')
        search_element = request.args.getlist('element')

        # レア度をここで弾いている(選択されていないレア度は検索対象に追加しない)
        search_json_data = [[i, json_dict[i]] for i in search_rank]

        json_search = JsonSearch(search_json_data)

        json_search.search_element(search_element)
        json_search.search_name(name)
        json_search.search_skill(skill)
        json_search.search_talent(talent)
        json_search.search_cinderella_card(cinderella)

        if not json_search.search_json_data:
            json_search.search_json_data.append('検索結果なし')

        search_data = [name, skill, talent, cinderella, search_rank, search_element]

        return render_template('index.html', result=json_search.search_json_data, search_data=search_data)
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
