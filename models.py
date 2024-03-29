import os
from random import choices
from secrets import choice
from unicodedata import category
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2.types import Geometry
from shapely.geometry import Point
from geoalchemy2.shape import to_shape
from geoalchemy2.elements import WKTElement
from geoalchemy2.functions import ST_DWithin
from geoalchemy2.types import Geography
from sqlalchemy.sql.expression import cast
from geoalchemy2.shape import from_shape
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

'''
setup_db(app):
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    database_path = os.getenv('DATABASE_URL', 'DATABASE_URL_WAS_NOT_SET?!')

    # https://stackoverflow.com/questions/62688256/sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy-dialectspostgre
    database_path = database_path.replace('postgres://', 'postgresql://')

    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

    # Initial sample data:
    insert_sample_locations()

# to add locations in map:
def insert_sample_locations():
    pass
    # loc1 = SampleLocation(
    #     description='Brandenburger Tor',
    #     geom=SampleLocation.point_representation(
    #         latitude=52.516247, 
    #         longitude=13.377711
    #     )
    # )
    # loc1.insert()

class SpatialConstants:
    SRID = 4326

class ShopCategory(): 
    def __init__(self, category, number):
        self.category = category
        self.number = number 

    # def get_shop_category (self): 
    #     return self.category

all_shop_categories = [
    ShopCategory('Secondhand store / boutique', 1), # number needed because it doesn't change as identifiyer, while naming of category can change (also for different languages)
    ShopCategory('Fairfashion store', 2),
    ShopCategory('Rental store for clothes', 3),
    ShopCategory('Designer fashion store', 4),
    ShopCategory('Swap box / cupboard', 5),
    ShopCategory('Flea market for clothes', 6),
    ShopCategory('Tailor or shoe maker / repairer', 7),
    ShopCategory('Upcycling', 8),
    ShopCategory('Clothes donations', 9),
    ShopCategory('Eco laundry', 10)]


class SampleLocation(db.Model):
    __tablename__ = 'sample_locations'

    def get_shop_category(self, shop_categories):   # added on 31.07
        for s in shop_categories:
            if s.number == int(self.shop_category): 
                return s

    id = Column(Integer, primary_key=True)
    location_name = Column(String(50))
    shop_category =Column(String) #can this me removed??
    description = Column(String(500))
    geom = Column(Geometry(geometry_type='POINT', srid=SpatialConstants.SRID))

    

    @staticmethod
    def point_representation(latitude, longitude):
        point = 'POINT(%s %s)' % (longitude, latitude)
        wkb_element = WKTElement(point, srid=SpatialConstants.SRID)
        return wkb_element

    @staticmethod
    def get_items_within_radius(lat, lng, radius, shop_category):
        """Return all sample locations within a given radius (in meters)"""

        #TODO: The arbitrary limit = 100 is just a quick way to make sure 
        # we won't return tons of entries at once, 
        # paging needs to be in place for real usecase
        results = SampleLocation.query.filter(
            ST_DWithin(
                cast(SampleLocation.geom, Geography),
                cast(from_shape(Point(lng, lat)), Geography),
                radius)
            ).limit(100).all() 

        return [l.to_dict() for l in results]    

    def get_location_latitude(self):
        point = to_shape(self.geom)
        return point.y

    def get_location_longitude(self):
        point = to_shape(self.geom)
        return point.x  

    def to_dict(self):
        return {
            'id': self.id,
            'location_name': self.location_name,
            'shop_category': self.shop_category,
            'description': self.description,
            'location': {
                'lng': self.get_location_longitude(),
                'lat': self.get_location_latitude(), 
            }
        }    

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()    


## USER CLASS (for registration and sign in)

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False) # i.e Hanna Barbera
    display_name = db.Column(db.String(20), unique=True, nullable=False) # i.e hanna_25
    email = db.Column(db.String(120), unique=True, nullable=False) # i.e hanna@hanna-barbera.com
    password = db.Column(db.String(32), nullable=False) 
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()
        
    def __repr__(self):
        return f"User({self.id}, '{self.display_name}', '{self.email}')"      

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()   