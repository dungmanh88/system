from app import db
from sqlalchemy import exc
from models import BlogPost

try:
    db.session.query(BlogPost).delete()
    ### Commit the change
    db.session.commit()
except exc.SQLAlchemyError:
    db.session.rollback()
