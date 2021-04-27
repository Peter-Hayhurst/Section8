from werkzeug.security import safe_str_cmp
from models.user import UserModel

# see if the user exists and the password matches
def authenticate(username, password): 
    user=UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password,password): # works on all system /versions / avoids encoding problems)
        return user

# extracts the userid from the identity token (issued on sucessful authentication)
def  identity(payload):
    user_id=payload['identity']
    return UserModel.find_by_id(user_id)
