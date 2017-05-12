import base64
import logging
import json

from flask import abort, current_app, Flask, request, redirect, url_for, render_template, session
from flask_api import status
from werkzeug.security import generate_password_hash, check_password_hash

from . import models
from . import timekit_api

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
        email = session.get('email')
        if email is not None:
            return redirect(url_for('dashboard'))
        return render_template('index.html')

    @app.route('/contact')
    def contact():
        email = session.get('email')
        if email is not None:
            return redirect(url_for('dashboard'))
        return render_template('contact.html')

    @app.route('/yowan')
    def yowan():
        email = session.get('email')
        if email is not None:
            return redirect(url_for('dashboard'))
        return render_template('profile.html')

    @app.route('/profiles')
    def profiles():
        email = session.get('email')
        if email is not None:
            return redirect(url_for('dashboard'))
        return render_template('profiles.html')

    @app.route('/interview-prep')
    def services():
        email = session.get('email')
        if email is not None:
            return redirect(url_for('dashboard'))
        return render_template('interview-prep.html')

    @app.route('/vision')
    def vision():
        email = session.get('email')
        if email is not None:
            return redirect(url_for('dashboard'))
        return render_template('vision.html')

    @app.route('/dashboard')
    def dashboard():
        email = session.get('email')
        if email is None:
            return redirect(url_for('login'))
        user = models.User.query.filter_by(email=email).first()
        events, success = timekit_api.get_events(user)
        if not success:
            events = []
        return render_template('dashboard.html', user=user, events=events)

    @app.route('/profile')
    def my_profile():
        email = session.get('email')
        if email is None:
            return redirect(url_for('login'))
        user = models.User.query.filter_by(email=email).first()
        return render_template('my_profile.html', user=user)

    @app.route('/schedule')
    def schedule():
        email = session.get('email')
        if email is None:
            return redirect(url_for('login'))
        user = models.User.query.filter_by(email=email).first()
        consultants = { consultant.user for consultant in models.Consultant.query.all() }
        return render_template('schedule.html', user=user, consultants=consultants)

    @app.route('/calendar/<int:user_id>')
    def calendar(user_id):
        email = session.get('email')
        if email is None:
            return redirect(url_for('login'))
        user = models.User.query.get(user_id)
        if user is None:
            abort(404)
        calendar = user.calendar
        if calendar is None:
            calendar, success = timekit_api.create_calendar(user)
            if not success:
                abort(500)
        return render_template('calendar.html', user=user, app_slug=calendar.app_slug, calendar_id=calendar.timekit_id)

    @app.route('/create', methods=['POST', 'GET'])
    def create():
        if request.method == 'POST':
            name = request.form["name"]
            skype = request.form["skype"]
            email = request.form["email"]
            password = request.form["password"]
            user_type = request.form["type"]
            try:
                user_type = int(user_type)
            except ValueError:
                return json.dumps({ 'success': 'false' }), 400
            if name is None or skype is None or email is None or password is None:
                return json.dumps({ 'success': 'false' }), 400
            user = models.User.query.filter_by(email=email).first()
            if user is not None:
                return json.dumps({ 'success': 'false'}), 200
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
                               skype_username=skype,
                               password=password,
                               pw_hash=pw_hash)
            timekit_token = timekit_api.get_api_token(user)
            if timekit_token is None:
                timekit_token, success = timekit_api.create_user(user)
                if not success:
                    return json.dumps({ 'success': 'false' }), 201
            user.timekit_token = timekit_token
            models.db.session.add(user)
            models.db.session.commit()
            if user_type == 0:
                consultant = models.Consultant(user=user)
                models.db.session.add(consultant)
                models.db.session.commit()
            else:
                client = models.Client(user=user)
                models.db.session.add(client)
                models.db.session.commit()
            session['email'] = user.email
            return json.dumps({ 'success': 'true' }), 201

        email = session.get('email')
        if email is not None:
            return redirect(url_for("dashboard"))
        return render_template('create.html')

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        email = session.get("email")
        if email is not None:
            return redirect(url_for("dashboard"))
        if request.method == 'POST':
            email = request.form["email"]
            password = request.form["password"]
            if email is None or password is None:
                return json.dumps({ 'success': 'false' }), 400
            user = models.User.query.filter_by(email=email).first()
            if user is None:
                return json.dumps({ 'success': 'false' }), 200
            if not check_password_hash(user.pw_hash, password):
                return json.dumps({ 'success': 'false' }), 200
            success = timekit_api.authenticate(user)
            if not success:
                return json.dumps({ 'success': 'false' }), 200
            session['email'] = user.email
            return json.dumps({ 'success': 'true' }), 200
        return render_template('login.html')

    @app.route('/logout', methods=['POST'])
    def logout():
        session.pop('email', None)
        return json.dumps({ 'success': 'true' }), 200

    @app.route('/profile', methods=['PUT'])
    def update_user():
        email = session.get("email")
        if email is None:
            return redirect(url_for("login"))
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        skype = request.form["skype"]
        description = request.form["description"]
        school = request.form["school"]
        major = request.form["major"]
        year = request.form["year"]
        sat_math = request.form["sat_math"]
        sat_reading = request.form["sat_reading"]
        sat_writing = request.form["sat_writing"]
        act = request.form["act"]

        user = models.User.query.filter_by(email=email).first()
        if user is None:
            abort(404)
        user.first_name = first_name
        user.last_name = last_name
        user.skype = skype
        user.description = description
        user.school = school
        user.major = major
        try:
            user.year = int(year)
        except ValueError:
            pass
        try:
            user.sat_math = int(sat_math)
        except ValueError:
            pass
        try:
            user.sat_reading = int(sat_reading)
        except ValueError:
            pass
        try:
            user.sat_writing = int(sat_writing)
        except ValueError:
            pass
        try:
            user.act = int(act)
        except ValueError:
            pass

        models.db.session.commit()
        return json.dumps({ 'success': 'true' }), 200
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
