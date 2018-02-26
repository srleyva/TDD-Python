from flask import current_app, g
from tinydb import TinyDB, where


def write_to_table(table, value):
    name = value.get('name')
    if _get_item(table, name):
        return False
    table = get_table(table)
    value.update({'id': _get_max_id('person') + 1})
    table.insert(value)
    return name


def delete_from_table(table, ID):
    table = get_table(table)
    response = table.remove(where('id') == int(ID))
    return response


def get_item_from_table(table, ID):
    table = get_table(table)
    record = table.search(where('id') == int(ID))
    return record


def get_table(table):
    """Opens a new database connection"""
    g.tinydb = TinyDB(current_app.config['DATABASE'])
    person_table = g.tinydb.table(table)
    return person_table


def _get_item(table, name):
    """Fetch a single item from the db"""
    table = get_table(table)
    try:
        return table.search(where('name') == name)[0]
    except IndexError:
        return None


def _get_max_id(table):
    table = get_table(table).all()
    table.sort(key=lambda k: k['id'], reverse=True)
    try:
        max_id = table[0]['id']
    except IndexError:
        return 0
    return max_id
