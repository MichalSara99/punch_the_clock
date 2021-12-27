import os
from app import db,create_app
from flask_migrate import Migrate
# CUSTOM PYTHON OBJECTS:
from app.models import Time_dimension,User,Work





app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app,db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,User=User,Work = Work,Time_dimension = Time_dimension)


