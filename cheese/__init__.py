import logging
import json

from flask import current_app, Flask, request, redirect, url_for, render_template, session
from flask_api import status
from werkzeug.security import generate_password_hash, check_password_hash

from . import models

def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    with app.app_context():
        models.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/contact')
    def contact():
        return render_template('contact.html')


    @app.route('/profiles')
    def profiles():
        return render_template('profiles.html')


    @app.route('/interview-prep')
    def services():
        return render_template('interview-prep.html')


    @app.route('/vision')
    def vision():
        return render_template('vision.html')

    @app.route('/dashboard')
    def dashboard():
        user = session.get('user')
        if user is None:
            return redirect(url_for('login'))
        return render_template('dashboard.html', user=user)

    @app.route('/schedule')
    def schedule():
        return render_template('schedule.html')

    @app.route('/create', methods=['POST', 'GET'])
    def create():
        if request.method == 'POST':
            name = request.form["name"]
            email = request.form["email"]
            password = request.form["password"]
            if name is None or email is None or password is None:
                return json.dumps({ 'success': 'false' }), 400
            name = name.split(' ')
            first_name = name[0]
            if len(name) > 1:
                last_name = name[1]
            else:
                last_name = ""
            pw_hash = generate_password_hash(password)
            user = models.User(first_name=first_name,
                               last_name=last_name,
                               email=email,
                               password=password,
                               pw_hash=pw_hash)
            models.db.session.add(user)
            models.db.session.commit()
            session['user'] = user.first_name
            return json.dumps({ 'success': 'true' }), 201
        return render_template('create.html')

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        if request.method == 'POST':
            email = request.form["email"]
            password = request.form["password"]
            if email is None or password is None:
                return json.dumps({ 'success': 'false' }), 400
            user = models.User.query.filter_by(email=email).first()
            if user is None:
                return json.dumps({ 'success': 'false' }), 201
            if not check_password_hash(user.pw_hash, password):
                return json.dumps({ 'success': 'false' }), 201
            session['user'] = user.first_name
            return json.dumps({ 'success': 'true' }), 201
        return render_template('login.html')

    @app.route('/logout', methods=['POST'])
    def logout():
        session.pop('user', None)
        return json.dumps({ 'success': 'true' }), 201

    @app.route('/api/user', methods=['GET'])
    def get_user():
        email = request.args.get('email')
        if email is None:
            return json.dumps({ 'user_exists': 'false'}), 400
        user = models.User.query.filter_by(email=email).first()
        if user is None:
            return json.dumps({ 'user_exists': 'false'}), 201
        return json.dumps({ 'user_exists': 'true' }), 201

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
