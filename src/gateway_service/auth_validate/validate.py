import os, requests

# Function that validates whether user has the correct authorizaiton to access whatever service. 
def token(request):
    if not "Authorization" in request.headers:
        return None, ("missing credentials", 401)

    token = request.headers["Authorization"]

    if not token:
        return None, ("missing credentials", 401)

    response = requests.post(
            f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate",
            headers={"Authorization": token},
        )
    
    if response.status_code == 200:
        print("[*AUTH SERVICE] token(request) passed")
        return response.text, None
    else:
        print("[*AUTH SERVICE] token(request) failed")
        return None, (response.text, response.status_code)

