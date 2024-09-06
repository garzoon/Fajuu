from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def init_bcrypt(app):
    bcrypt.init_app(app)

def encrypt_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(hashed_password, candidate_password):
    return bcrypt.check_password_hash(hashed_password, candidate_password)
