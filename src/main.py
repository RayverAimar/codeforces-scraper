# Codeforces Scraper

import pandas as pd
import requests

# Getting solved problems by specific user

def get_solved_user_problems(user_name):
    url = f'https://codeforces.com/api/user.status?handle={user_name}'
    r = requests.get(url)
    if r.status_code != 200:
        print('There was an error in the request.')
        print(r.json()['comment'])
        return None
    if r.json()['status'] != 'OK':
        print('Call limit exceeded. Try again in 2 seconds')
        return None
    
    for submission in r.json()['result']:
        if submission['verdict'] == "OK":
            print(submission['problem']['name'])


# Plot activity