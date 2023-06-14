import grpc
from concurrent import futures
import ewaste_service_pb2
import ewaste_service_pb2_grpc
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

class EwasteServiceServicer(ewaste_service_pb2_grpc.EwasteServiceServicer):
    
    def AddEwaste(self, request, context):
        try:
            with connection.cursor() as cursor:
                cursor.execute('''INSERT INTO eWasteItems (UserName, ItemType, ItemWeight) VALUES (%s, %s, %s)''',
                            (request.user_name, request.item_type, request.weight))
                connection.commit()
                return ewaste_service_pb2.AddEwasteResponse(success=True, message="E-Waste item added.")
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
