import os

base_dir=os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY=os.urandom(24).hex()
    #SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(base_dir,'app.db')
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://flaskuser:flaskuser@localhost/userdb"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    MONGO_URI="mongodb://localhost:27017/empdb"
