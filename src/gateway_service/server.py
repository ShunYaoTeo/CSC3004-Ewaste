import os, json, sys, requests
from flask import Flask, request
from flask_cors import CORS
from auth_svc import access
from auth_validate import validate
# from storage import util

server = Flask(__name__)
CORS(server)

@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err
        
    
if __name__ == "__main__":
    try:
        server.run(host='0.0.0.0', port=8080)
    except KeyboardInterrupt:
        print("Interupted")
        try: 
            sys.exit(0)
        except SystemExit:
            os._exit(0)