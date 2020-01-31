import math
import re

import psycopg2
from flask import g

from hachinai_search import settings


def get_db():
    if "db" not in g:
        database_url = settings.DATABASE_URL
        g.db = psycopg2.connect(database_url)
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def split_word_space(word):
    if word:
        return re.split(r'\s+', word)
    else:
        return None


def make_card_name_sql(word):
    conn = get_db()
    cur = conn.cursor()
    card_name_sql = b''
    if word:
        word_after = list(map(lambda x: '%' + x + '%', word))
        card_name_sql += cur.mogrify('card_name ~~* ANY(%s) AND ', (word_after,))
    return card_name_sql.decode()


def make_where_sql(name, word):
    conn = get_db()
    cur = conn.cursor()
    where_sql = b''
    where_sql += cur.mogrify('{} ~~* ANY (%s) AND '.format(name), (word,))
    return where_sql.decode()


def make_cinderella_intersect_sql(search_word):
    conn = get_db()
    cur = conn.cursor()
    sql = b''
    if search_word:
        for i in search_word:
            sql += b'INTERSECT '
            sql += cur.mogrify('SELECT card_id FROM card_cinderellas '
                               'INNER JOIN cinderella_card_informations cci '
                               'ON card_cinderellas.cinderella_card_id = cci.cinderella_card_information_id '
                               'AND cinderella_card_name LIKE %s ', ('%' + i + '%',))
    return sql.decode()


def make_skill_intersect_sql(search_word):
    conn = get_db()
    cur = conn.cursor()
    sql = b''
    if search_word:
        for i in search_word:
            sql += b'INTERSECT '
            sql += cur.mogrify('SELECT card_id FROM card_skills '
                               'INNER JOIN skill_informations si on card_skills.skill_id = si.skill_information_id '
                               'AND skill_name LIKE %s ', ('%' + i + '%',))
    return sql.decode()


def make_ability_intersect_sql(search_word):
    conn = get_db()
    cur = conn.cursor()
    sql = b''
    if search_word:
        for i in search_word:
            sql += b'INTERSECT '
            sql += cur.mogrify('SELECT card_id FROM card_abilities '
                               'INNER JOIN ability_informations ai on card_abilities.ability_id'
                               ' = ai.ability_information_id '
                               'AND ability_name LIKE %s ', ('%' + i + '%',))
    return sql.decode()


def get_page(cinderella_card_sql, skill_name_sql, ability_name_sql, where_sql):
    conn = get_db()
    cur = conn.cursor()

    # SQL変えたらCOUNTできなくなったてへぺろ☆
    cur.execute('SELECT COUNT (DISTINCT ("card_informations".card_id)) FROM card_informations '
                'INNER JOIN card_cinderellas ON card_informations.card_id = card_cinderellas.card_id '
                'INNER JOIN cinderella_card_informations ON card_cinderellas.cinderella_card_id = '
                'cinderella_card_informations.cinderella_card_information_id{cinderella} '
                'INNER JOIN card_skills ON card_informations.card_id = card_skills.card_id '
                'INNER JOIN skill_informations ON card_skills.skill_id = skill_informations.skill_information_id{skill} '
                'INNER JOIN card_abilities ON card_informations.card_id = card_abilities.card_id '
                'INNER JOIN ability_informations on card_abilities.ability_id = ability_informations.ability_information_id{ability} '
                '{where};'.format(cinderella=cinderella_card_sql, skill=skill_name_sql,
                                  ability=ability_name_sql, where=where_sql))
    all_count = cur.fetchone()[0]
    paging = math.ceil(all_count / 10)

    return paging


def get_result(card_name, rarity, attribute, cinderella_card_sql, skill_name_sql, ability_sql):
    conn = get_db()
    cur = conn.cursor()

    where = card_name + rarity + attribute

    if where:
        where = 'WHERE ' + where[:-4]

    print(cur.mogrify('SELECT DISTINCT (card_id) '
                      'FROM card_informations '
                      '{where}'
                      '{cinderella_card}'
                      '{skill}'
                      '{ability}'
                      .format(where=where, cinderella_card=cinderella_card_sql,
                              skill=skill_name_sql, ability=ability_sql)))

    cur.execute('SELECT DISTINCT (card_id) '
                'FROM card_informations '
                '{where}'
                '{cinderella_card}'
                '{skill}'
                '{ability}'
                .format(where=where, cinderella_card=cinderella_card_sql,
                        skill=skill_name_sql, ability=ability_sql))
    return cur.fetchall()


def get_card_name(i):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT card_name FROM card_informations WHERE card_id = %s', (i,))

    return cur.fetchone()[0]


def get_attribute(i):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT attribute FROM card_informations WHERE card_id = %s', (i,))

    return cur.fetchone()[0]


def get_rarity(i):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT rarity FROM card_informations WHERE card_id = %s', (i,))

    return cur.fetchone()[0]


def get_cinderella_card(i):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT cinderella_card_name FROM card_cinderellas '
                'INNER JOIN cinderella_card_informations ON card_cinderellas.cinderella_card_id = '
                'cinderella_card_informations.cinderella_card_information_id '
                'WHERE card_id = %s', (i,))
    card_list = []
    for i in cur.fetchall():
        card_list.append({'card_name': i[0]})
    return card_list


def get_skill(i):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT skill_name FROM card_skills '
                'INNER JOIN skill_informations ON card_skills.skill_id = skill_informations.skill_information_id '
                'WHERE card_id = %s', (i,))
    skill_list = []
    for i in cur.fetchall():
        skill_list.append({'skill_name': i[0]})
    return skill_list


def get_ability(i):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT ability_name FROM card_abilities '
                'INNER JOIN ability_informations ON card_abilities.ability_id = '
                'ability_informations.ability_information_id '
                'WHERE card_id = %s', (i,))
    ability_list = []
    for i in cur.fetchall():
        ability_list.append({'ability_name': i[0]})
    return ability_list


def search_db(card_name, cinderella_card, skill_name, ability_name, rare, attribute):
    card_name = split_word_space(card_name)

    cinderella_card = split_word_space(cinderella_card)
    skill_name = split_word_space(skill_name)
    ability_name = split_word_space(ability_name)

    card_name_sql = make_card_name_sql(card_name)
    rarity_sql = make_where_sql('rarity', rare)
    attribute_sql = make_where_sql('attribute', attribute)

    cinderella_card_sql = make_cinderella_intersect_sql(cinderella_card)
    skill_name_sql = make_skill_intersect_sql(skill_name)
    ability_name_sql = make_ability_intersect_sql(ability_name)

    # page = get_page(cinderella_card_sql, skill_name_sql, ability_name_sql, where_sql)
    result = get_result(card_name_sql, rarity_sql, attribute_sql, cinderella_card_sql, skill_name_sql, ability_name_sql)

    result_list = []
    for i in result:
        chara_data = {}
        chara_data.update({'card_name': get_card_name(i)})
        chara_data.update({'attribute': get_attribute(i)})
        chara_data.update({'rarity': get_rarity(i)})
        chara_data.update({'cinderella_cards': get_cinderella_card(i)})
        chara_data.update({'skills': get_skill(i)})
        chara_data.update({'ability': get_ability(i)})

        result_list.append(chara_data)

    return result_list
