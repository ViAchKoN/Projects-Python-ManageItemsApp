import pytest as pytest

from application import db as _db


@pytest.fixture(scope='session')
def db(app_test, request):
    def teardown():
        _db.drop_all()

    app_ctx = app_test.app_context()
    app_ctx.push()

    app_test.db = app_test
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
