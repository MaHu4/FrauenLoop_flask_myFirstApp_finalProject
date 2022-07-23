import os
import sys
from flask import Flask, request, abort, jsonify, render_template, url_for, flash, redirect
from flask_cors import CORS
import traceback
from forms import NewLocationForm,  RegistrationForm, LoginForm
from models import setup_db, SampleLocation, db_drop_and_create_all, User

from forms import RegistrationForm
from models import User
from sqlalchemy.exc import IntegrityError
import hashlib

from forms import LoginForm
from flask_login import login_user, logout_user, login_required, current_user, login_manager, LoginManager


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY

    # """ uncomment at the first time running the app. Then comment back so you do not erase db content over and over """
    # db_drop_and_create_all()

    # initialize a LoginManager at the app level
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'


    ## LOGIN

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)           

    @app.route("/", methods=['GET', 'POST']) 
    def login():
        # Sanity check: if the user is already authenticated then go back to home page
        # if current_user.is_authenticated:
        #    return redirect(url_for('map'))

        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(display_name=form.username.data).first()
            hashed_input_password = hashlib.md5(form.password.data.encode()).hexdigest()
            if user and user.password == hashed_input_password:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('map'))
            else:
                flash('Oups! Something went wrong. Please check user name and password', 'danger')
        return render_template('login.html', title='Login', form=form) 

    ## LOGOUT

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash(f'You have logged out!', 'success')
        return redirect(url_for('login'))   

    ## REGISTRATION FORM

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        # Sanity check: if the user is already authenticated then go back to home page
        # if current_user.is_authenticated:
        #     return redirect(url_for('map'))

        # Otherwise process the RegistrationForm from request (if it came)
        form = RegistrationForm()
        if form.validate_on_submit():
            # hash user password, create user and store it in database
            hashed_password = hashlib.md5(form.password.data.encode()).hexdigest()
            user = User(
                full_name=form.fullname.data,
                display_name=form.username.data, 
                email=form.email.data, 
                password=hashed_password)

            try:
                user.insert()
                flash(f'Account created for: {form.username.data}!', 'success')
                return redirect(url_for('map'))
            except IntegrityError as e:
                flash(f'Could not register! The entered username or email might be already taken', 'danger')
                print('IntegrityError when trying to store new user')
                # db.session.rollback()
            
        return render_template('registration.html', form=form)   

    
    ## INTERACTIVE MAP 

    @app.route('/map', methods=['GET'])
    def map():
        return render_template(
            'map.html', 
            map_key=os.getenv('MAPS_API_KEY', 'MAPS_API_KEY_WAS_NOT_SET?!')
        )

    @app.route('/detail', methods=['GET'])
    def detail():
        location_id = float(request.args.get('id'))
        item = SampleLocation.query.get(location_id)
        return render_template(
            'detail.html', 
            item=item,
            map_key=os.getenv('MAPS_API_KEY', 'MAPS_API_KEY_WAS_NOT_SET?!')
        )            

    @app.route("/new-location", methods=['GET', 'POST'])
    @login_required #one needs to be logged in to access feature
    def new_location():
        form = NewLocationForm()

        if form.validate_on_submit():            
            latitude = float(form.coord_latitude.data)
            longitude = float(form.coord_longitude.data)
            description = form.description.data
            location_name = form.location_name.data
            shop_category = form.shop_category.data
            location = SampleLocation(
                description=description,
                location_name=location_name,
                shop_category=shop_category,
                geom=SampleLocation.point_representation(latitude=latitude, longitude=longitude)
            )   
            location.insert()

            flash(f'New location created!', 'success')
            return redirect(url_for('map'))

        return render_template(
            'new-location.html',
            form=form,
            map_key=os.getenv('MAPS_API_KEY', 'MAPS_API_KEY_WAS_NOT_SET?!')
        ) 

    @app.route("/api/store_item")
    def store_item():
        try:
            latitude = float(request.args.get('lat'))
            longitude = float(request.args.get('lng'))
            description = request.args.get('description')
            location_name=request.args.get('location_name')
            shop_category=request.args.get('shop_category')

            location = SampleLocation(
                description=description,
                location_name=location_name, # added
                shop_category=shop_category, # added
                geom=SampleLocation.point_representation(latitude=latitude, longitude=longitude)
            )   
            location.insert()

            return jsonify(
                {
                    "success": True,
                    "location": location.to_dict()
                }
            ), 200
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            app.logger.error(traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2))
            abort(500)

    @app.route("/api/get_items_in_radius")
    def get_items_in_radius():
        try:
            latitude = float(request.args.get('lat'))
            longitude = float(request.args.get('lng'))
            radius = int(request.args.get('radius'))
            category = str(request.args.get('category')) #added
            
            locations = SampleLocation.get_items_within_radius(latitude, longitude, radius, category) # category added
            return jsonify(
                {
                    "success": True,
                    "results": locations
                }
            ), 200
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            app.logger.error(traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2))
            abort(500)

# Tried with: https://www.youtube.com/watch?v=_sgVt16Q4O4
    # @app.route('/map/filter', methods=['GET', 'POST'])
    # @login_required
    # def filter():
    #     if request.method == 'POST': 
    #         print(request.form.getlist('mycheckbox'))
    #         return 'Done'
    #     return render_template(
    #         'map.html', 
    #          map_key=os.getenv('MAPS_API_KEY', 'MAPS_API_KEY_WAS_NOT_SET?!')
    #         )

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "server error"
        }), 500

    return app

app = create_app()
if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='127.0.0.1',port=port,debug=True)