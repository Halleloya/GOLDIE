from flask_login import LoginManager
from .models import User, unicode_to_int

# login_manager: Used by flask_login to maintain the current user state
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=unicode_to_int(user_id)).first()
