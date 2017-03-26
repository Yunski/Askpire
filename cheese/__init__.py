import logging

from flask import current_app, Flask, request, redirect, url_for, render_template, session
from flask_api import status


def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    """ sql
    with app.app_context():
        model = sql
        model.init_app(app)"""

    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/profiles')
    def profiles():
        return render_template('profiles.html')


    @app.route('/services')
    def services():
        return render_template('profiles.html')

    @app.route('/vision')
    def vision():
        return render_template('vision.html')

    # Add an error handler. This is useful for debugging the live application,
    # however, you should disable the output of the exception for production
    # applications.
    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return app
