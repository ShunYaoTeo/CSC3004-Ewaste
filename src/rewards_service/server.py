import grpc
from concurrent import futures
import rewards_service_pb2
import rewards_service_pb2_grpc
import os
import logging, traceback
import pymysql.cursors

connection = pymysql.connect(
    host=os.environ.get("MYSQL_HOST"),
    user=os.environ.get("MYSQL_USER"),
    password=os.environ.get("MYSQL_PASSWORD"),
    database=os.environ.get("MYSQL_DB"),
    port=int(os.environ.get("MYSQL_PORT")),
    cursorclass=pymysql.cursors.DictCursor
)

class RewardServiceServicer(rewards_service_pb2_grpc.RewardServiceServicer):
    def AddPoints(self, request, context):
        username = request.username
        points_to_add = request.pointsToAdd

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''INSERT INTO UserPoints (UserName, Points) VALUES (%s, %s)
                       ON DUPLICATE KEY UPDATE Points = Points + %s''', (username, points_to_add, points_to_add)
                )
                connection.commit()

            return rewards_service_pb2.AddPointsResponse(success=True, message="Points added successfully.")

        except Exception as e:
            print(f"An exception occurred: {e}")
            traceback.print_exc() 
            return rewards_service_pb2.AddPointsResponse(success=False, message="Error occurred while adding points.")

    def GetRewards(self, request, context):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Rewards")
                rewards = cursor.fetchall()

            return rewards_service_pb2.GetRewardsResponse(rewards=[rewards_service_pb2.Reward(rewardId=reward['RewardId'], rewardName=reward['RewardName'], rewardPoints=reward['Cost']) for reward in rewards])

        except Exception as e:
            print(f"An exception occurred: {e}")
            traceback.print_exc() 
            return rewards_service_pb2.GetRewardsResponse(rewards=[])


    def GetUserRewards(self, request, context):
        username = request.username

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT R.RewardId, R.RewardName, R.Cost 
                    FROM UserRewards UR 
                    INNER JOIN Rewards R ON UR.RewardId = R.RewardId 
                    WHERE UR.Username = %s AND UR.Redeemed = True""", (username,)
                )
                user_rewards = cursor.fetchall()

            return rewards_service_pb2.GetUserRewardsResponse(
                rewards=[rewards_service_pb2.Reward(
                    rewardId=reward['RewardId'], 
                    rewardName=reward['RewardName'], 
                    rewardPoints=reward['Cost']) for reward in user_rewards]
            )

        except Exception as e:
            print(f"An exception occurred: {e}")
            traceback.print_exc() 
            return rewards_service_pb2.GetUserRewardsResponse(rewards=[])


    def GetUserPoints(self, request, context):
        username = request.username

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT Points FROM UserPoints WHERE UserName = %s", (username,)
                )
                user_points = cursor.fetchone()

            return rewards_service_pb2.GetUserPointsResponse(points=user_points['Points'] if user_points else 0)

        except Exception as e:
            print(f"An exception occurred: {e}")
            traceback.print_exc() 
            return rewards_service_pb2.GetUserPointsResponse(points=0)


    def RedeemReward(self, request, context):
        username = request.username
        reward_id = request.rewardId

        try:
            with connection.cursor() as cursor:
                # Check user's current points
                cursor.execute("SELECT Points FROM UserPoints WHERE UserName = %s", (username,))
                user_points = cursor.fetchone()

                # Check required points for the reward
                cursor.execute("SELECT Cost FROM Rewards WHERE RewardId = %s", (reward_id,))
                reward_cost = cursor.fetchone()

                if user_points and reward_cost and user_points['Points'] >= reward_cost['Cost']:
                    # Deduct points
                    cursor.execute(
                        "UPDATE UserPoints SET Points = Points - %s WHERE UserName = %s", (reward_cost['Cost'], username)
                    )

                    # Add redeemed reward to UserRewards table
                    cursor.execute(
                        "INSERT INTO UserRewards (UserName, RewardId, Redeemed) VALUES (%s, %s, %s)", 
                        (username, reward_id, True)
                    )

                    connection.commit()
                    return rewards_service_pb2.RedeemRewardResponse(success=True, message="Reward redeemed successfully.")

                else:
                    return rewards_service_pb2.RedeemRewardResponse(success=False, message="Not enough points or Reward doesn't exist.")

        except Exception as e:
            print(f"An exception occurred: {e}")
            traceback.print_exc() 
            return rewards_service_pb2.RedeemRewardResponse(success=False, message="Error occurred while redeeming reward.")



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rewards_service_pb2_grpc.add_RewardServiceServicer_to_server(RewardServiceServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("[REWARDS SERVICE] Server has started")
    server.wait_for_termination()
    
if __name__ == '__main__':
    logging.basicConfig()
    serve()
