import grpc
from concurrent import futures
import ewaste_service_pb2
import ewaste_service_pb2_grpc
import rewards_service_pb2
import rewards_service_pb2_grpc
import os
import math
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

# Item Type to Points Gain rule
EWASTE_POINTS = {
    "batteries": 5,
    "resistors": 10,
    "wires": 3,
    }

class EwasteServiceServicer(ewaste_service_pb2_grpc.EwasteServiceServicer):
    

    def calculate_points(self, item_type, weight_kg):
        """Calculate points based on item type and weight."""
        # Make sure item type is recognized
        if item_type not in EWASTE_POINTS:
            raise ValueError(f"Unknown item type {item_type}")

        # Get points per kg for the item type
        points_per_kg = EWASTE_POINTS[item_type]

        # Calculate total points
        total_points = weight_kg * points_per_kg
        total_points = math.ceil(total_points)

        return int(total_points)
    
    def AddEwaste(self, request, context):
        try:
            with connection.cursor() as cursor:
                cursor.execute('''INSERT INTO eWasteItems (UserName, ItemType, ItemWeight) VALUES (%s, %s, %s)''',
                            (request.user_name, request.item_type, request.weight))
                
                cursor.execute('''INSERT INTO ItemTypeStats (UserName, ItemType, TotalWeight, TotalItems)
                                  VALUES (%s, %s, %s, 1)
                                  ON DUPLICATE KEY UPDATE TotalWeight = TotalWeight + %s, TotalItems = TotalItems + 1''',
                            (request.user_name, request.item_type, request.weight, request.weight))
                
                connection.commit()

                points_to_add = self.calculate_points(request.item_type, request.weight)
                

                # Call Rewards Service Grpc Server to update User Points
                rewards_channel = grpc.insecure_channel('rewards-ewaste:50052')
                stub = rewards_service_pb2_grpc.RewardServiceStub(rewards_channel)
                add_points_request = rewards_service_pb2.AddPointsRequest(username=request.user_name, pointsToAdd=points_to_add)
                add_points_response = stub.AddPoints(add_points_request)

                if add_points_response.success:
                    return ewaste_service_pb2.AddEwasteResponse(success=True, message="E-Waste item added.")
                else:
                    return ewaste_service_pb2.AddEwasteResponse(success=False, message="Add Points Error.")
                
        except Exception as e:
            print(f"An exception occurred: {e}")
            traceback.print_exc() 
            return ewaste_service_pb2.AddEwasteResponse(success=False, message="Error Occurred")

    def GetUserEwaste(self, request, context):
        try:
            with connection.cursor() as cursor:
                cursor.execute('''SELECT * from eWasteItems WHERE UserName = %s''', (request.user_name,))
                results = cursor.fetchall()
                if results:
                    ewaste_items = [ewaste_service_pb2.EwasteItem(
                            item_id=int(result["ItemId"]),
                            user_name=result["UserName"],
                            item_type=result["ItemType"],
                            weight=float(result["ItemWeight"]),
                            date_added=str(result["DateSubmitted"])
                        ) for result in results]
                    return ewaste_service_pb2.GetUserEwasteResponse(items=ewaste_items)
                else:
                    return ewaste_service_pb2.GetUserEwasteResponse(items=[])
        except Exception as e:
            print(f"An exception occurred: {e}")
            traceback.print_exc() 
            return ewaste_service_pb2.GetUserEwasteResponse(items=[])

    def GetUserEwasteStats(self, request, context):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT ItemType, TotalWeight, TotalItems FROM ItemTypeStats WHERE UserName=%s", (request.user_name,))
                results = cursor.fetchall()
                if results:
                    stats = {item["ItemType"]: ewaste_service_pb2.EwasteStats(total_weight=item["TotalWeight"], total_items=item["TotalItems"]) for item in results}
                    return ewaste_service_pb2.GetUserEwasteStatsResponse(item_stats=stats)
                else:
                    return ewaste_service_pb2.GetUserEwasteStatsResponse(item_stats={})
        except Exception as e:
            print(f"An exception occurred: {e}")
            traceback.print_exc() 
            return ewaste_service_pb2.GetUserEwasteStatsResponse(item_stats={})

    def GetEwasteItem(self, request, context):
        pass  # Implement this function as per your business logic.

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ewaste_service_pb2_grpc.add_EwasteServiceServicer_to_server(EwasteServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("*[EWASTE SERVICE] Server has started")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
