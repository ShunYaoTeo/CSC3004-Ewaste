import json
import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))

@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "*[AUTH SERVICE] No authorization header", 401
    
    if not mysql.connection:
        return "*[AUTH SERVICE] No mysql connection", 500
    cursor = mysql.connection.cursor()
    result = cursor.execute("SELECT email, password, admin FROM user WHERE email=%s", (auth.username,))

    if result > 0:
        user_row = cursor.fetchone()
        email = user_row[0]
        password = user_row[1]
        admin = user_row[2]

        if auth.username != email or auth.password != password:
            return "*[AUTH SERVICE] wrong credentials", 401
        else: 
            return createJWT(auth.username, os.environ.get("JWT_KEY"), admin)
    else:
        return "*[AUTH SERVICE] No user found", 401
    
@server.route("/validate", methods=["POST"])
def validate():
    encoded_JWT = request.headers["Authorization"]

    if not encoded_JWT:
        return "*[AUTH SERVICE] missing token", 401
    
    encoded_JWT = encoded_JWT.split(" ")[1]
    try:
        decoded_JWT = jwt.decode(encoded_JWT, os.environ.get("JWT_KEY"), algorithms=["HS256"])
    except Exception as err:
        print(err)
        return "*[AUTH SERVICE] not authorized", 403
    
    return decoded_JWT, 200

def createJWT(username, secret, admin):
    return jwt.encode(
            {
                "username": username,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                + datetime.timedelta(days=1),
                # issued_at
                "iat": datetime.datetime.utcnow(),
                "admin": admin,
            },
            secret,
            algorithm="HS256",
        )


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)