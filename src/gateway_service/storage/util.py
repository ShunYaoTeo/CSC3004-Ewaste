import pika, json


def upload(channel, request, userEmail, routingKey, correlation_id):
        
    message = {
        "username": userEmail,
        "food_type": request.form["food_type"],
        "reason" : request.form["reason"],
        "donated" : request.form["donated"],
        }

    try:
        channel.basic_publish(
                exchange="",
                routing_key= routingKey,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                    correlation_id=correlation_id
                ),#Persistent mode as such so that when pods fail, messages are still persisted
            )
        
        # Store the correlation ID in the dictionary
        
        print("[*Gateway_Service] Request Sent to foodwaste Queue!")
    except Exception as err:
        print(err)
        return "[*Gateway_Service] Failed to send request message to Food_Waste_Service", 500
