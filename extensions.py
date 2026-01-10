from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager
from utils.token_blocklist import BLOCKLIST

mysql = MySQL()
jwt = JWTManager()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in BLOCKLIST