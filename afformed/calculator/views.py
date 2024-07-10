from django.http import JsonResponse
import requests
from collections import deque
import time

# Configuration
WINDOW_SIZE = 10
TEST_SERVER_URL = 'http://20.244.56.144/test'

# Storage for numbers
numbers = { 
    'primes': deque(maxlen=WINDOW_SIZE),
    'fibo': deque(maxlen=WINDOW_SIZE),
    'even': deque(maxlen=WINDOW_SIZE),
    'rand': deque(maxlen=WINDOW_SIZE),
}




def fetch_numbers_from_test_server(qualified_id):
    try:
        req ={
            "companyName": "Untitled",
            "clientID": "fe60af74-f36d-4ed9-bf52-077997bcb569",
            "clientSecret": "pgVrWgRVLZiPifNc",
            "ownerName": "Marzook",
            "ownerEmail": "mmohamedmarzook0701@gmail.com",
            "rollNo": "410621104059"
            }
        auth_token = requests.post(url="http://20.244.56.144/test/auth", json=req)
        auth_token = auth_token.json()
        token = auth_token["access_token"]
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(f"{TEST_SERVER_URL}/{qualified_id}", timeout=0.5,headers=headers)
        response.raise_for_status()
        return response.json().get('numbers', [])
    except requests.RequestException:
        return []

def get_numbers(request, qualified_id):
    if qualified_id not in numbers:
        return JsonResponse({'error': 'Invalid number ID'}, status=400)

    fetched_numbers = fetch_numbers_from_test_server(qualified_id)


    current_numbers = numbers[qualified_id]
    previous_state = list(current_numbers)

    # Add unique numbers
    for num in fetched_numbers:
        if num not in current_numbers:
            current_numbers.append(num)
    
    # Calculate average
    if current_numbers:
        average = sum(current_numbers) / len(current_numbers)
    else:
        average = 0

    response = {
        'fetched_numbers': fetched_numbers,
        'previous_state': previous_state,
        'current_state': list(current_numbers),
        'average': average
    }
    return JsonResponse(response)
