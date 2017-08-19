from app import db
from sqlalchemy import exc
from models import BlogPost

try:
    ### create the database and db tables
    db.create_all()

    ### Insert data
    db.session.add(BlogPost("Good", "I\'m Good"))
    db.session.add(BlogPost("Bad", "I\'m Bad"))
    db.session.add(BlogPost("Flask", "Flask"))
    db.session.add(BlogPost("Postgresql", "Postgresql"))

    ### Commit the change
    db.session.commit()
except exc.SQLAlchemyError:
    db.session.rollback()
