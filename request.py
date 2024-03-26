import requests

# For the signup endpoint
new_user_data = {
    "email":"admin@example.com",
    "password":"somepassword"
}

# using http because it is a development server.
response = requests.post("http://localhost:8000/signup", json=new_user_data)
print(response.json())

# For the login endpoint.
user_credentials = {
    "email":"admin@example.com",
    "password":"somepassword"
}
access_token = "admin@example.com"  

# using http because it is a development server.
response = requests.post("http://localhost:8000/login", json=user_credentials)
print(response.json())

# For addPost endpoint.
post_data = {
    "text": "Anything can be posted.",
}

# Send a POST request to the /addPost endpoint with the post data
response = requests.post("http://localhost:8000/addPost", json=post_data, headers={"Authorization": f"Bearer {access_token}"})
print(response)


# For getPosts endpoint.
response = requests.get("http://localhost:8000/getPosts", headers={"Authorization": f"Bearer {access_token}"})
print(response.json())


# For the deletePost endpoint.
post_id = "post_id" 
response = requests.delete(f"http://localhost:8000/deletePost/{post_id}", headers={"Authorization": f"Bearer {access_token}"})
print(response.json())
