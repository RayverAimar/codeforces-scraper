# Codeforces Scraper

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests

# Getting solved problems by specific user

def drop_duplicates(l):
    return list(dict.fromkeys(l))

def get_user_solved_problems(user_name):
    url = f'https://codeforces.com/api/user.status?handle={user_name}'
    r = requests.get(url)
    if r.status_code != 200:
        print('There was an error in the request.')
        print(r.json()['comment'])
        return None
    if r.json()['status'] != 'OK':
        print('Call limit exceeded. Try again in 2 seconds')
        return None
    
    historical_problems_done = []
    problems_done_by_contest = {}

    for submission in r.json()['result']:
        if submission['verdict'] == "OK":
            historical_problems_done.append(submission['problem']['name'])
            if submission['author']['participantType'] == 'CONTESTANT':
                problems_done_by_contest.setdefault(submission['contestId'], []).append(submission['problem']['index'])
    
    n_problems_done = 0

    for key in problems_done_by_contest.keys():
        n_problems_done+=len(problems_done_by_contest[key])
    
    print(f'Rate of problems done by contest: {n_problems_done/len(problems_done_by_contest)}')

    drop_duplicates(historical_problems_done)

    return historical_problems_done

def scrape_top_ten_rated():
    pass

def get_user_solved_problems_by_tag(user_name, tag):
    pass

def get_user_activity(user_name):
    url = f'https://codeforces.com/api/user.rating?handle={user_name}'
    r = requests.get(url)
    if r.status_code != 200:
        print('There was an error in the request.')
        print(r.json()['comment'])
    if r.json()['status'] != 'OK':
        print('Call limit exceeded. Try again in 2 seconds')
        return None
    
    rating_changes = []

    for result in r.json()['result']:
        rating_changes.append(result['newRating'])
    
    print(f'Total of participated public contests: {len(rating_changes)}')
    print(f'Highest rating got: {max(rating_changes)}')

    plt.plot(rating_changes, c='aqua', marker='o', lw=2, ms=3.5, mec='blue', mfc='blue')
    plt.ylabel('Rating')
    plt.xlabel('Number of contest')
    plt.title(f'Historical rating change of {user_name}')
    plt.show()


problems_done = get_user_solved_problems('tourist')
get_user_activity('tourist')

# Look for rate in every contest. How many problems does this user do in a contest CONTESTANT/PRACTICE