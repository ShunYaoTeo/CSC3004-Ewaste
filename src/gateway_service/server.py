import os, json, sys, requests
import grpc
import ewaste_service_pb2
import ewaste_service_pb2_grpc
from flask import Flask, request, jsonify
from flask_cors import CORS
from auth_svc import access
from auth_validate import validate
import logging
server = Flask(__name__)
CORS(server)

# gRPC channels
eWasteServiceChannel = grpc.insecure_channel('service-ewaste:50051')

# Stubs
eWasteServiceStub = ewaste_service_pb2_grpc.EwasteServiceStub(eWasteServiceChannel)

@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err
    
@server.route("/addEwaste", methods=["POST"])
def addEwaste():
    # Get the data from the HTTP request
    data = request.get_json()
    
    # Create the AddEwaste request
    req = ewaste_service_pb2.AddEwasteRequest(
        user_name=data["user_name"],
        item_type=data["item_type"],
        weight=data["weight"]
    )

    # Send the request to the eWaste service
    resp = eWasteServiceStub.AddEwaste(req)

    # Return the response to the client
    return {"success": resp.success, "message": resp.message}

@server.route("/getUserEwaste", methods=["GET"])
def getUserEwaste():
    # Check Validation of User's JWT Token
    access, err = validate.token(request)
    print("access: ", access, ", error: ", err)
    if err:
        print("*[Gateway Service] validation failed: ", err)
        return err

    # Get the username from the jwt token
    access = json.loads(access)
    user_name = access['username']

    print("*[GATEWAY SERVICE] getUserEwaste username: ", user_name)
    # Create the GetUserEwaste request
    req = ewaste_service_pb2.GetUserEwasteRequest(user_name=str(user_name))

    # Send the request to the eWaste service
    items = eWasteServiceStub.GetUserEwaste(req)

    # convert the grpc response into a Python list of dicts
    items_dict = [{'item_id': item.item_id, 'user_name': item.user_name, 'item_type': item.item_type, 'weight': item.weight, 'date_added': item.date_added} for item in items.items]

    return jsonify(items_dict), 200
        
    
if __name__ == "__main__":
    try:
        logging.basicConfig()
        server.run(host='0.0.0.0', port=8080)
    except KeyboardInterrupt:
        print("Interupted")
        try: 
            sys.exit(0)
        except SystemExit:
            os._exit(0)