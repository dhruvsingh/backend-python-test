"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
  main.py dropdb
"""
from docopt import docopt
import subprocess
import os
import json

from alayatodo import app, models
from flask_fixtures import load_fixtures


def _run_sql(filename):
    try:
        subprocess.check_output(
            "sqlite3 %s < %s" % (app.config['DATABASE'], filename),
            stderr=subprocess.STDOUT,
            shell=True
        )
    except subprocess.CalledProcessError, ex:
        print ex.output
        os.exit(1)


if __name__ == '__main__':
    args = docopt(__doc__)

    if args['dropdb']:
        models.db.drop_all()
        print "AlayaTodo: Database dropped."
    elif args['initdb']:
        # create db and all tables
        models.db.create_all()
        # initialize data for the created db
        fixture_dir_path = os.path.join(os.getcwd(), 'fixtures')
        # we know that no dirs are there in the fixtures path, so safe to
        # iterate
        for fixture in os.listdir(fixture_dir_path):
            fixture_path = os.path.join(fixture_dir_path, fixture)
            with open(fixture_path, 'r') as infile:
                load_fixtures(models.db, json.loads(infile.read()))

        print "AlayaTodo: Database initialized."
    else:
        app.run(use_reloader=True)
