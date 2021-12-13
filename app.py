import os

from flask import Flask
from flask_apscheduler import APScheduler
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from db import db
from main import job
from resources.user import UserRegister, UserLogin, TokenRefresh, UserProfile

__author__ = "@toannguyen3105"

app = Flask(__name__)
CORS(app)


# set configuration values
class Config(object):
    SCHEDULER_API_ENABLED = True


app.config.from_object(Config())

# initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = '_____***!pdfPriceFit!***_____'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserProfile, '/profile')
api.add_resource(TokenRefresh, '/refresh')


# DEBUG: import datetime
# DEBUG: next_run_time=datetime.datetime.now()

# import datetime
# @scheduler.task('interval', id='pdt_price_fit', minutes=20, misfire_grace_time=900, next_run_time=datetime.datetime.now())
@scheduler.task('interval', id='hc_pbn', seconds=3, misfire_grace_time=900, max_instances=2)
def ScheduledTask():
    with app.app_context():
        job()


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, use_reloader=False, debug=True)
