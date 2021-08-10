def test_development_config(app, config_yaml):
    app.config.from_object('application.config.DevelopmentConfig')
    assert app.config['DEBUG']
    assert not app.config['TESTING']
    assert app.config[
        'SQLALCHEMY_DATABASE_URI'
    ] == 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
        **config_yaml['postgres']
    )


def test_testing_config(app, config_yaml):
    app.config.from_object('application.config.TestingConfig')
    assert app.config['DEBUG']
    assert app.config['TESTING']
    assert not app.config['PRESERVE_CONTEXT_ON_EXCEPTION']
    assert app.config[
        'SQLALCHEMY_DATABASE_URI'
    ] == 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
        **config_yaml['postgres_test']
    )


def test_production_config(app, config_yaml):
    app.config.from_object('application.config.ProductionConfig')
    assert not app.config['DEBUG']
    assert not app.config['TESTING']
    assert app.config[
        'SQLALCHEMY_DATABASE_URI'
    ] == 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
        **config_yaml['postgres']
    )
