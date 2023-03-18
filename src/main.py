# Codeforces Scraper

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
from bs4 import BeautifulSoup

# Utility functions

def drop_duplicates(l):
    return list(dict.fromkeys(l))

def display_info(top_ten):

    print('\nCurrent codeforces top ten table\n')

    for i, element in enumerate(top_ten):
        print(f"{i+1}) {element['name']}[{element['rating']}] -> {element['profile_route']}")

def coincidence(l1, l2):
    for i in l1:
        for e in l2:
            if i == e:
                return True
    return False

def print_problems(problems):
    for i, problem in enumerate(problems):
        print(f'{i+1}) {problem}')

# Scrape functions

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

    historical_problems_done = drop_duplicates(historical_problems_done)

    return historical_problems_done

def get_problems_done_by_user_in_specific_contest(user_name, contestId, participant=True):
    url = f'https://codeforces.com/api/user.status?handle={user_name}'
    r = requests.get(url)
    if r.status_code != 200:
        print('There was an error in the request.')
        print(r.json()['comment'])
        return None
    if r.json()['status'] != 'OK':
        print('Call limit exceeded. Try again in 2 seconds')
        return None
    if int(contestId) > 2000:
        print('Not a valid contest')
        return None

    problems_done = []

    for submission in r.json()['result']:
        if int(submission['contestId']) != int(contestId):
            continue
        if submission['verdict'] != 'OK':
            continue
        if participant:
            if submission['author']['participantType'] != 'CONTESTANT':
                continue
        problems_done.append(submission['problem']['name'])
    
    problems_done = drop_duplicates(problems_done)

    print(len(problems_done), 'solved problems.')
    return problems_done
        
def scrape_top_ten_rated():
    url = 'https://codeforces.com'
    r = requests.get(url)
    s = BeautifulSoup(r.text, 'lxml')
    
    profile_routes = [item.get('href') for item in s.find('table', attrs={'class':'rtable'}).find_all('a')]
    users_names = [profile.split('/')[2] for profile in profile_routes]

    users_info = []

    for i in range(10):
        user_info = {}
        user_info['profile_route'] = url+profile_routes[i]
        user_info['name'] = users_names[i]
        user_info['rating'] = None
        users_info.append(user_info)

    return users_info

def get_user_solved_problems_by_tag(user_name, tag):
    url = f'https://codeforces.com/api/user.status?handle={user_name}'
    r = requests.get(url)
    if r.status_code != 200:
        print('There was an error in the request.')
        print(r.json()['comment'])
        return None
    if r.json()['status'] != 'OK':
        print('Call limit exceeded. Try again in 2 seconds')
        return None
    
    problems_done = []

    for submission in r.json()['result']:
        if submission['verdict'] != "OK":
            continue
        problem_tags = submission['problem']['tags']
        if tag in problem_tags:
            problems_done.append(submission['problem']['name'])

    problems_done = drop_duplicates(problems_done)

    return problems_done

def get_user_activity(user_name, graphics=True):
    url = f'https://codeforces.com/api/user.rating?handle={user_name}'
    r = requests.get(url)
    if r.status_code != 200:
        print('There was an error in the request.')
        print(r.json()['comment'])
        return None
    if r.json()['status'] != 'OK':
        print('Call limit exceeded. Try again in 2 seconds')
        return None
    
    rating_changes = []

    for result in r.json()['result']:
        rating_changes.append(result['newRating'])
    
    print(f'Displaying info of {user_name}...')
    print(f'\tTotal of participated public contests: {len(rating_changes)}')
    print(f'\tHighest rating got: {max(rating_changes)}')

    if graphics:
        plt.plot(rating_changes, c='aqua', marker='o', lw=2, ms=3.5, mec='blue', mfc='blue')
        plt.ylabel('Rating')
        plt.xlabel('Number of contest')
        plt.title(f'Historical rating change of {user_name}')
        plt.show()

    return rating_changes[-1]

def menu():
    
    print('1. Display codeforces top-ten-rated info')
    print('2. Get historical solved problems by an user')
    print('3. Get solved problems with specific tag by an user')
    print('4. Get rating change of an user')
    print('5. Get solved problems in a contest by an specific user')
    try:
        option = int(input('Type your option: '))
    except Exception as e:
        print(e)
        return
    if option == 1:
        top_ten_info = scrape_top_ten_rated()
        if not top_ten_info:
            return
        for each_top in top_ten_info:
            each_top['rating'] = get_user_activity(each_top['name'], graphics=True) # may be false if graphics are not wanted
        display_info(top_ten_info)
    elif option == 2:
        try:
            user_name = input('User name: ')
        except Exception as e:
            print(e)
            return
        solved_problems = get_user_solved_problems(user_name)
        if not solved_problems:
            return
        print_problems(solved_problems)
    elif option == 3:
        try:
            user_name = input('User name: ')
            tag = input('tag: ')
        except Exception as e:
            print(e)
            return
        solved_problems = get_user_solved_problems_by_tag(user_name, tag)
        if not solved_problems:
            return
        print_problems(solved_problems)
    elif option == 4:
        try:
            user_name = input('User name: ')
        except Exception as e:
            print(e)
            return 
        current_rating = get_user_activity(user_name, graphics=True) # may be false if graphics are not wanted
        if not current_rating:
            return
        print(f'Current user rating: {current_rating}')
    elif option == 5:
        try:
            user_name = input('User name: ')
            contestId = input('contestId: ')
        except Exception as e:
            print(e)
            return 
        solved_problems = get_problems_done_by_user_in_specific_contest(user_name, contestId, participant=True) # May be True or False if want to get only solved problems as contestant
        if not solved_problems:
            return
        print_problems(solved_problems)
    else:
        print('Invalid option\nExiting...')       

if __name__ == '__main__':
    menu()