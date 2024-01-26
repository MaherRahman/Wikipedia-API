from flask import Flask, request, jsonify
import sys
import json
import requests

payload = json.dumps({
"username": "Maher"
})
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}


# Define the API endpoints
endpoints = ["most-viewed",
             "view-count",
             "most-viewed-day"]

def validate_input(endpoint, arg1, arg2, arg3, arg4):
    if endpoint not in endpoints:
        return False, "Invalid endpoint"
    try:
        if arg1 is not None:
            if not isinstance(arg1, str):
                return False, "Invalid article"
        # Check if the year and month are valid, Wikipedia was founded in 2001
        year = int(arg2)
        if year < 2001 or year > 2024:
            return False, "Invalid year"
        month = int(arg3)
        if month < 1 or month > 12:
            return False, "Invalid month"
        # If the endpoint has a week argument, convert it to integer and check if it is valid
        week = int(arg4)
        if week != -1:
            if week < 1 or week > 4:
                return False, "Invalid week"
    except ValueError:
        # If any argument cannot be converted to the expected type, return False
        return False, "Invalid argument type"
    # If all checks pass, return True
    return True, "Valid input"

def get_local(endpoint, arg1, arg2, arg3, arg4):
    url = f"http://127.0.0.1:5000/{endpoint}/"
    if arg1 is not None: 
        url = url + "/" + str(arg1)
    url = url + "/" + str(arg2) + "/" + str(arg3)
    if arg4 != -1:
        url = url + "/" + str(arg4)
    print(url)
    response = requests.request("GET", url, headers=headers, data=payload)
    return response

def run_app():
    print("This API lets you view the most viewed articles for a week or month, see the view counts of an article, \n or retrieve the day of the month where an article got the most views")
    print("These are the available endpoints that you can use")
    for endpoint in endpoints:
        print(endpoint)
    print("To exit the program, type 'quit'")
    # Loop until the user types 'quit'
    while True:
        # Prompt the user for the endpoint
        endpoint = input("Enter the endpoint: ")
        # Check if the user wants to quit
        if endpoint == "quit":
            break
        arg1 = None
        if endpoint == "view-count" or endpoint == "most-viewed-day":
            arg1 = input("Enter the title of the article you wish to query: ")
        # Prompt the user for the arguments
        arg2 = input("Enter the Year: ")
        arg3 = input("Enter the Month: ")
        arg4 = input("Enter the Week, if you don't want a week, enter -1: ")
        # Validate the user input
        valid, message = validate_input(endpoint, arg1, arg2, arg3, arg4)
        # If the input is valid, send the request and print the response
        if valid:
            response = get_local(endpoint, arg1, arg2, arg3, arg4)
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.json()}")
        # If the input is invalid, print the error message
        else:
            print(f"Error: {message}")
    sys.exit()

run_app()
