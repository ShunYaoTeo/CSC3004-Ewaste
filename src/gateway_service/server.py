import os, json, sys, requests
import grpc
import ewaste_service_pb2
import ewaste_service_pb2_grpc
import rewards_service_pb2
import rewards_service_pb2_grpc
from flask import Flask, request, jsonify
from flask_cors import CORS
from auth_svc import access
from auth_validate import validate
import logging
server = Flask(__name__)
CORS(server)

# gRPC channels
eWasteServiceChannel = grpc.insecure_channel('service-ewaste:50051')
rewardsServiceChannel = grpc.insecure_channel('rewards-ewaste:50052')

# Stubs
eWasteServiceStub = ewaste_service_pb2_grpc.EwasteServiceStub(eWasteServiceChannel)
rewardsServiceStub = rewards_service_pb2_grpc.RewardServiceStub(rewardsServiceChannel)

######### Auth Service Endpoints ###########
@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err
    

######### eWaste Service Endpoints ###########    
@server.route("/addEwaste", methods=["POST"])
def addEwaste():
    # Check Validation of User's JWT Token
    access, err = validate.token(request)
    print("access: ", access, ", error: ", err)
    if err:
        print("*[Gateway Service] validation failed: ", err)
        return err
    
    # Get the username from the jwt token
    access = json.loads(access)
    user_name = access['username']
    item_type = request.args.get('item_type')
    weight = request.args.get('weight')
    # Create the AddEwaste request
    req = ewaste_service_pb2.AddEwasteRequest(
        user_name=str(user_name),
        item_type=str(item_type),
        weight=float(weight)
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

@server.route("/getUserEwasteStats", methods=["GET"])
def getUserEwasteStats():
    # Check Validation of User's JWT Token
    access, err = validate.token(request)
    print("access: ", access, ", error: ", err)
    if err:
        print("*[Gateway Service] validation failed: ", err)
        return err
    
    # Get the username from the jwt token
    access = json.loads(access)
    user_name = access['username']

    print("*[GATEWAY SERVICE] getUserEwasteStats username: ", user_name)

    req = ewaste_service_pb2.GetUserEwasteStatsRequest(user_name=str(user_name))
    items = eWasteServiceStub.GetUserEwasteStats(req)

    items_dict = [
    {'item_type': item_type, 'total_weight': item.total_weight, 'total_items': item.total_items}
    for item_type, item in items.item_stats.items()
    ]

    return jsonify(items_dict), 200

######### Rewards Service Endpoints ###########
@server.route("/getReward", methods=["GET"])
def getReward():
     # Check Validation of User's JWT Token
    access, err = validate.token(request)
    print("access: ", access, ", error: ", err)
    if err:
        print("*[Gateway Service] validation failed: ", err)
        return err

    req = rewards_service_pb2.GetRewardsRequest()
    resp = rewardsServiceStub.GetRewards(req)
    rewards_dict = [{'reward_id': reward.rewardId, 'reward_name': reward.rewardName, 'cost': reward.rewardPoints} for reward in resp.rewards]

    return jsonify(rewards_dict), 200

@server.route("/getUserRewards", methods=["GET"])
def getUserRewards():
    # Check Validation of User's JWT Token
    access, err = validate.token(request)
    if err:
        return err

    # Get the username from the jwt token
    access = json.loads(access)
    user_name = access['username']

    req = rewards_service_pb2.GetUserRewardsRequest(username=str(user_name))
    resp = rewardsServiceStub.GetUserRewards(req)
    rewards_dict = [{'reward_id': reward.rewardId, 'reward_name': reward.rewardName, 'cost': reward.rewardPoints} for reward in resp.rewards]

    return jsonify(rewards_dict), 200

@server.route("/redeemReward", methods=["POST"])
def redeemReward():
    # Check Validation of User's JWT Token
    access, err = validate.token(request)
    if err:
        return err

    # Get the username and reward_id from the request
    access = json.loads(access)
    user_name = access['username']
    reward_id = request.args.get('reward_id')

    req = rewards_service_pb2.RedeemRewardRequest(username=str(user_name), rewardId=int(reward_id))
    resp = rewardsServiceStub.RedeemReward(req)

    return {"success": resp.success, "message": resp.message}

@server.route("/getUserPoints", methods=["GET"])
def getUserPoints():
    # Check Validation of User's JWT Token
    access, err = validate.token(request)
    if err:
        return err

    # Get the username from the jwt token
    access = json.loads(access)
    user_name = access['username']

    req = rewards_service_pb2.GetUserPointsRequest(username=str(user_name))
    resp = rewardsServiceStub.GetUserPoints(req)

    return {"points": resp.points}


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