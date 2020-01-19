import re

from flask import Flask, render_template, request, redirect, url_for

from hachinai_search.models import search_db

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/result')
def search():
    if request.method == 'GET':

        card_name = request.args.get('card_name')
        cinderella_card_name = request.args.get('cinderella_card')
        skill_name = request.args.get('skill_name')
        ability_name = request.args.get('ability_name')

        rare_list = request.args.getlist('rare')
        attribute_list = request.args.getlist('attribute')

        result = search_db(card_name, cinderella_card_name, skill_name, ability_name, rare_list, attribute_list)

        if result:
            # TODO: 検索にヒットした部分のハイライトが実装できていない
            #  フロントに持たせるか、バックエンドに持たせるかも未定
            return render_template('search_result.html', result=result, card_name=card_name,
                                   cinderella_card_name=cinderella_card_name, skill_name=skill_name,
                                   ability_name=ability_name)
        else:
            return render_template('no_data.html', result=result, card_name=card_name,
                                   cinderella_card_name=cinderella_card_name, skill_name=skill_name,
                                   ability_name=ability_name)
    else:
        return redirect(url_for('/'))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
