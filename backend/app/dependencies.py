from fastapi import Depends
from app.database import get_db
from app.security.jwt import get_current_user
from app.models.user import User

get_db_dependency = get_db
get_current_user_dependency = get_current_user
