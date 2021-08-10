import argparse

from sqlalchemy import create_engine

from application.config import CONFIG

DSN = 'postgresql://{user}:{password}@{host}:{port}/{database}'

ADMIN_DB_URL = DSN.format(user='postgres', password='postgres', database='postgres', host='localhost', port=5432)

admin_engine = create_engine(ADMIN_DB_URL, isolation_level='AUTOCOMMIT')


def parse_args() -> None:
    parser = argparse.ArgumentParser('Manage Entities App database initializer')
    parser.add_argument(
        'mode',
        type=str,
        help='Use "setup" to create db and "setup_test" to create db for tests '
        'or "teardown" and "teardown_test" to delete all database data associated with this application.',
    )
    return parser.parse_args()


def setup_db(config) -> None:

    db_name = config['database']
    db_user = config['user']
    db_pass = config['password']

    conn = admin_engine.connect()
    conn.execute('DROP DATABASE IF EXISTS %s' % db_name)
    conn.execute('DROP ROLE IF EXISTS %s' % db_user)
    conn.execute("CREATE USER %s WITH PASSWORD '%s'" % (db_user, db_pass))
    conn.execute('CREATE DATABASE %s' % db_name)
    conn.execute('GRANT ALL PRIVILEGES ON DATABASE %s TO %s' % (db_name, db_user))
    conn.close()


def teardown_db(config) -> None:

    db_name = config['database']
    db_user = config['user']

    conn = admin_engine.connect()
    conn.execute(
        """
      SELECT pg_terminate_backend(pg_stat_activity.pid)
      FROM pg_stat_activity
      WHERE pg_stat_activity.datname = '%s'
        AND pid <> pg_backend_pid();"""
        % db_name
    )
    conn.execute('DROP DATABASE IF EXISTS %s' % db_name)
    conn.execute('DROP ROLE IF EXISTS %s' % db_user)
    conn.close()


if __name__ == '__main__':
    db_url = DSN.format(**CONFIG['postgres'])
    engine = create_engine(db_url)

    args = parse_args()

    mode = args.mode

    if mode == 'setup':
        setup_db(CONFIG['postgres'])
    elif mode == 'setup_test':
        setup_db(CONFIG['postgres_test'])
    elif mode == 'teardown':
        teardown_db(CONFIG['postgres'])
    elif mode == 'teardown_test':
        teardown_db(CONFIG['postgres_test'])

    print('Done!')
