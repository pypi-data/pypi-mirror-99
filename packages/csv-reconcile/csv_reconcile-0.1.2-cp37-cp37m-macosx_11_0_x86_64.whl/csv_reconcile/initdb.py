from flask import current_app
import csv
from .db import get_db, normalizeDBcol

from importlib.resources import read_text
import csv_reconcile
from . import scorer


def initDataTable(colnames, idcol):
    db = get_db()
    cols = []
    for col in colnames:
        slug = normalizeDBcol(col)
        if col == idcol:
            cols.append('%s TEXT PRIMARY KEY' % (slug,))
        else:
            cols.append('%s TEXT NOT NULL' % (slug,))

        db.execute('INSERT INTO datacols VALUES (?,?)', (col, slug))

    # create data table with the contents of the csv file
    createSQL = 'CREATE TABLE data (\n  %s\n)'
    db.execute(createSQL % (',\n  '.join(cols),))


def initReconcileTable(colnames):
    db = get_db()
    create = [
        'CREATE TABLE reconcile (\n  id TEXT PRIMARY KEY,\n  word TEXT NOT NULL'
    ]
    for col in colnames:
        create.append('%s TEXT NOT NULL' % (col,))

    # create data table with the contents of the csv file
    db.execute(',\n  '.join(create) + '\n)')


def init_db():
    db = get_db()
    idcol, searchcol = current_app.config['CSVCOLS']
    csvfilenm = current_app.config['CSVFILE']
    kwargs = current_app.config.get('CSVKWARGS', {})
    scoreOptions = current_app.config['SCOREOPTIONS']
    csvencoding = current_app.config.get('CSVENCODING', None)
    enckwarg = dict()
    if csvencoding:
        enckwarg['encoding'] = csvencoding

    schema = read_text(csv_reconcile, 'schema.sql')
    db.executescript(schema)

    with db:
        # Create a table with ids (as PRIMARY ID), words and bigrams
        with open(csvfilenm, newline='', **enckwarg) as csvfile:
            reader = csv.reader(csvfile, **kwargs)
            header = next(reader)

            # Throws if col doesn't exist
            searchidx = header.index(searchcol)
            ididx = header.index(idcol)

            normalizedFields = scorer.getNormalizedFields()
            initDataTable(header, idcol)
            initReconcileTable(normalizedFields)

            datavals = ','.join('?' * len(header))

            for row in reader:
                mid = row[ididx]
                word = row[searchidx]
                matchFields = scorer.normalizeWord(word, **scoreOptions)
                db.execute(
                    "INSERT INTO reconcile VALUES (%s)" %
                    (','.join('?' * (2 + len(normalizedFields))),),
                    (mid, word) + tuple(matchFields))

                db.execute("INSERT INTO data VALUES (%s)" % (datavals), row)
