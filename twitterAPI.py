import urllib.request, urllib.parse, urllib.error
from twurl import augment
import ssl
import json
import sys
import sqlite3


def main():
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    if len(sys.argv) <= 1:
        print('Not a valid command. Help:')
        print('-stat: gives the user status.')
        print('-friends: gives the user friends.')
        print('-svfr: save users friend in a data base.')
    else:
        if len(sys.argv) == 2 and sys.argv[1] == "-stat":
            account = input('Enter account name:')
            num_stat = input('Enter numbers of status:')
            user_status(account,num_stat,ctx)
        if len(sys.argv) == 2 and sys.argv[1] == "-friends":
            account = input('Enter account name:')
            num_friends = input('Enter numbers of friends:')
            user_friends(account,num_friends,ctx)
        if len(sys.argv) == 2 and sys.argv[1] == "-svfr":
            account = input('Enter account name:')
            num_friends = input('Enter numbers of friends:')
            save_user_friends(account,num_friends,ctx)

def save_user_friends(account,num_friends,ctx):
    conn = sqlite3.connect('twitter.db')
    cur = conn.cursor()
    create_sql = "CREATE TABLE IF NOT EXISTS " + account + " (id INTEGER PRIMARY KEY, friend_name TEXT UNIQUE)"
    cur.execute(create_sql)
    print("Calling Twitter...")
    if not num_friends.isnumeric():
        num_friends = 50
    url = 'https://api.twitter.com/1.1/friends/list.json'
    formed_url = augment(url,{'screen_name': account,'count': num_friends})
    try:
        connection = urllib.request.urlopen(formed_url, context=ctx)
    except:
        print('Not a valid account')
        quit()
    data = connection.read().decode()
    headers = dict(connection.getheaders())
    print('Remaining:',headers['x-rate-limit-remaining'])
    print('------------------------------------------------')
    js = json.loads(data)
    for user in js['users']:
        select_sql = "SELECT * FROM " + account + " WHERE friend_name = ?"
        cur.execute(select_sql,(user['screen_name'],))
        row = cur.fetchone()
        if row is None:
            insert_sql = "INSERT INTO " + account + " (friend_name) VALUES (?)" 
            cur.execute(insert_sql,(user['screen_name'],))
        print(user['screen_name'])
    conn.commit()
    
def user_friends(account,num_friends,ctx):
    print("Calling Twitter...")
    if not num_friends.isnumeric():
        num_friends = 20
    url = 'https://api.twitter.com/1.1/friends/list.json'
    formed_url = augment(url,{'screen_name': account,'count': num_friends})
    try:
        connection = urllib.request.urlopen(formed_url, context=ctx)
    except:
        print('Not a valid account')
        quit() 
    data = connection.read().decode()
    headers = dict(connection.getheaders())
    print('Remaining:',headers['x-rate-limit-remaining'])
    print('------------------------------------------------')
    js = json.loads(data)
    for user in js['users']:
        print(user['screen_name'])
    
def user_status(account,num_stat,ctx):
    print("Calling Twitter...")
    if not num_stat.isnumeric():
        num_stat = 50
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    formed_url = augment(url,{'screen_name': account,'count': num_stat})
    try:
        connection = urllib.request.urlopen(formed_url, context=ctx)
    except:
        print('Not a valid account')
        quit()        
    data = connection.read().decode()
    headers = dict(connection.getheaders())
    print('Remaining:',headers['x-rate-limit-remaining'])
    print('------------------------------------------------')
    js = json.loads(data)
    for stat in js:
        print("Date:",stat['created_at'])
        print("Status:",stat['text'])

main()


