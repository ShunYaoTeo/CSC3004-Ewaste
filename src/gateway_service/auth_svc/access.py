import os, requests


def login(request):
    auth = request.authorization
    if not auth:
        return None, ("missing credentials", 401)

    basicAuth = (auth.username, auth.password)

    response = requests.post(
                f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login",
                auth=basicAuth
            )
    
    if response.status_code == 200:
        print("*[GATEWAY SERVICE] Login success")
        return response.text, None
    else:
        print("*[GATEWAY SERVICE] Login failed")
        return None, (response.text, response.status_code)
