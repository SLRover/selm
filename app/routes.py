from flask import Blueprint, render_template, redirect, url_for, request, abort, flash
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse, urljoin
from app.forms import LoginForm, RegisterForm, AddLicenseForm, EditLicenseForm, RemoveLicenseForm, SetupForm
from app.models import User, License
from app import db
import datetime
import configparser
from config import Config
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps
import os

routes_bp = Blueprint('routes_bp', __name__)


def is_new_app(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        rule = request.url_rule

        if os.path.exists(Config.CONFIG_FILE) and 'setup' in rule.rule:
            return redirect(url_for('routes_bp.index'))
        elif not os.path.exists(Config.CONFIG_FILE) and 'setup' not in rule.rule:
            return redirect(url_for('routes_bp.setup'))

        return func(*args, **kwargs)

    return decorated_view


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))

    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def validate(date_string):
    try:
        datetime.datetime.strptime(date_string, '%d.%m.%Y')
        return 'correct'
    except ValueError:
        return 'error'


@routes_bp.route('/setup', methods=['GET', 'POST'])
@is_new_app
def setup():
    form = SetupForm()

    if form.validate_on_submit():
        config = configparser.ConfigParser()
        config.add_section('DB settings')

        if form.database.data == 'postgresql':
            config.set('DB settings', 'type', form.database.data)
            config.set('DB settings', 'url', form.url.data)
            config.set('DB settings', 'user', form.user.data)
            config.set('DB settings', 'password', form.password.data)
            config.set('DB settings', 'name', form.name.data)
            config.set('DB settings', 'port', form.port.data)
            config.set('DB settings', 'tz', form.tz.data)

            with open(Config.CONFIG_FILE, 'w') as config_file:
                config.write(config_file)
        else:
            config.set('DB settings', 'type', form.database.data)
            config.set('DB settings', 'tz', form.tz.data)

            with open(Config.CONFIG_FILE, 'w') as config_file:
                config.write(config_file)

        try:
            db.create_all()

            return redirect(url_for('routes_bp.index'))
        except SQLAlchemyError as e:
            flash('Database error: {}'.format(e))

            return redirect(url_for('routes_bp.setup'))

    return render_template('setup.html', form=form)


@routes_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    all_entries = License.query.all()
    licenses = []

    for entry in all_entries:
        lic = {}
        lic['id'] = entry.id
        lic['product'] = entry.product
        lic['key'] = entry.key
        if entry.expire:
            lic['expire'] = entry.expire.strftime('%d.%m.%Y')
        lic['email'] = entry.email
        lic['active'] = entry.active
        licenses.append(lic)

    remove_form = RemoveLicenseForm()

    if remove_form.validate_on_submit():
        license_item = License.query.get(int(remove_form.remove_id.data))
        license_product = license_item.product
        db.session.delete(license_item)
        db.session.commit()
        flash('License {} was deleted'.format(license_product), category='primary')

        return redirect(url_for('routes_bp.index'))

    return render_template(
        'index.html',
        licenses=licenses,
        remove_form=remove_form
    )


@routes_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_license():
    add_form = AddLicenseForm()

    if add_form.validate_on_submit():
        if validate(add_form.expire.data) == 'correct':
            expire_date = datetime.datetime.strptime(add_form.expire.data, '%d.%m.%Y')
        else:
            flash('Expire date format is not correct', category='warning')
            expire_date = None

        new_license = License(
            product=add_form.product.data,
            key=add_form.key.data,
            expire=expire_date,
            email=add_form.email.data,
            user=current_user.id,
            active=add_form.active.data
        )
        db.session.add(new_license)
        db.session.commit()
        flash('New license added', category='success')

        return redirect(url_for('routes_bp.index'))

    return render_template('add_license.html', add_form=add_form)


@routes_bp.route('/edit/<int:license_id>', methods=['GET', 'POST'])
@login_required
def edit_license(license_id):
    license_item = License.query.get(license_id)
    edit_form = EditLicenseForm()
    license_formatted = {}
    license_formatted['id'] = license_item.id
    license_formatted['product'] = license_item.product
    license_formatted['key'] = license_item.key
    if license_item.expire:
        license_formatted['expire'] = license_item.expire.strftime('%d.%m.%Y')
    license_formatted['email'] = license_item.email
    license_formatted['active'] = license_item.active

    if edit_form.validate_on_submit():
        if validate(edit_form.expire.data) == 'correct':
            expire_date = datetime.datetime.strptime(edit_form.expire.data, '%d.%m.%Y')
        else:
            flash('Expire date format is incorrect', category='warning')

            return redirect(url_for('routes_bp.edit_license', license_id=license_id))

        license_item.product = edit_form.product.data
        license_item.key = edit_form.key.data
        license_item.expire = expire_date
        license_item.email = edit_form.email.data
        license_item.active = edit_form.active.data
        license_product = license_item.product
        db.session.commit()
        flash('License {} updated'.format(license_product), category='success')

        return redirect(url_for('routes_bp.edit_license', license_id=license_id))

    return render_template('edit_license.html', license=license_formatted, edit_form=edit_form)


@routes_bp.route('/login', methods=['GET', 'POST'])
@is_new_app
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes_bp.index'))

    if not User.query.all():
        flash('Please, register a new user', category='primary')

        return redirect(url_for('routes_bp.register'))

    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()

        if user and user.check_password(login_form.password.data):
            login_user(user)
            flash('You are logged in', category='success')
            next_page = request.args.get('next')

            if not is_safe_url(next_page):
                return abort(400)

            return redirect(next_page or url_for('routes_bp.index'))
        else:
            flash('Login or password is not correct', category='warning')

    return render_template('login.html', form=login_form)


@routes_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You are logged out', category='success')

    return redirect(url_for('routes_bp.login'))


@routes_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        new_user = User(
            username=register_form.username.data,
            email=register_form.email.data,
            fullname=register_form.full_name.data,
            password=register_form.password.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('You are registered successfully!\nPlease log in now.', category='success')

        return redirect(url_for('routes_bp.login'))

    return render_template('register.html', form=register_form)
