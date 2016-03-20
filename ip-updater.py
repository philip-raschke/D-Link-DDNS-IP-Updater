import sys
import requests
import os
import datetime
from BeautifulSoup import BeautifulSoup
import socket


def log(msg):
    return '[' + str(datetime.datetime.now()) + '] ' + msg

path = os.path.abspath(os.path.dirname(__file__))
if (not os.path.exists(os.path.join(path, 'ip-sources')) or
    not os.path.exists(os.path.join(path, 'last-ip')) or
    not os.path.exists(os.path.join(path, 'credentials'))):
    sys.exit(log('At least one required file could not be loaded'))

ip = ''
for line in open(os.path.join(path, 'ip-sources'), 'rU', 1):
    try:
        ip = requests.get(line.rstrip('\n'), timeout=3).text.rstrip('\n')
        try:
            socket.inet_aton(ip)
        except socket.error:
            print log('Retrieved an illegal IP address from ' + line.rstrip('\n'))
            continue
        print log('Retrieved ' + ip + ' from ' + line.rstrip('\n'))
        break
    except requests.exceptions.Timeout:
        print log('Connecting to ' + line.rstrip('\n') + ' timed out')
        continue

if ip == '':
    sys.exit(log('Could not obtain IP address'))

old_ip = open(os.path.join(path, 'last-ip'), 'rU', 1).readline()
print log('Old IP address is ' + old_ip)

if ip == old_ip:
    print log('IP address did not change')
    sys.exit(0)
else:
    f = open(os.path.join(path, 'last-ip'), 'w+', 1)
    f.write(ip)
    f.close()

url_login = 'https://www.dlinkddns.com/login/?next=/'
url_page = 'https://www.dlinkddns.com/host/'
url_logout = 'https://www.dlinkddns.com/logout'
token_slug = 'csrfmiddlewaretoken'

f = open(os.path.join(path, 'credentials'), 'rU', 1)
username = f.readline().rstrip('\n')
password = f.readline().rstrip('\n')

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'Keep-Alive'
}

error = False

try:
    c = requests.session()

    # get the login page of the D-Link DDNS service
    login_get = c.get(url_login, headers=headers, timeout=5)
    if not login_get.status_code == 200:
        sys.exit(log('An error occurred while trying to get the login page'))

    # extract the CSRF-token of the response
    # send POST request to service to authenticate
    csrf = BeautifulSoup(login_get.text).find('input', {'name': token_slug})['value']
    auth = {
        'username': username,
        'password': password,
        token_slug: csrf
    }
    login_post = c.post(url_login, headers=headers, timeout=5, cookies=login_get.cookies, data=auth)
    if not login_post.status_code == 200:
        sys.exit(log('An error occurred while trying to submit the login data'))
    if BeautifulSoup(login_post.text).find('p', {'class': 'warn'}) is not None:
        sys.exit('The D-Link DDNS service does not accept the credentials.')

    # get the respective host page
    page_get = c.get(url_page, headers=headers, timeout=5, cookies=login_post.cookies)
    if not page_get.status_code == 200:
        sys.exit(log('An error occurred while trying to get the host page'))

    # extract the CSRF-token
    # send the IP address to the service
    csrf = BeautifulSoup(page_get.text).find('input', {'name': token_slug})['value']
    payload = {
        token_slug: csrf,
        'ip': ip
    }

    # after calling /host/ a redirect to the host page occurred
    # page_get.url holds the correct URL of the host
    page_post = c.post(page_get.url, headers=headers, timeout=5, cookies=login_post.cookies, data=payload)
    if not page_post.status_code == 200:
        sys.exit(log('An error occurred while trying to update the IP address'))

    # logout from the service
    logout = c.get(url_logout, headers=headers, timeout=5, cookies=login_post.cookies)
    if not logout.status_code == 200:
        sys.exit(log('An error occurred while trying to logout'))

    print log('IP address was successfully updated')

except requests.exceptions.ConnectionError:
    print log('ConnectionError occurred while communicating with the D-Link DDNS service')
    error = True
except requests.exceptions.HTTPError:
    print log('HTTPError occurred while communicating with the D-Link DDNS service')
    error = True
except requests.exceptions.Timeout:
    print log('Timeout occurred while communicating with the D-Link DDNS service')
    error = True
except requests.exceptions.TooManyRedirects:
    print log('TooManyRedirects occurred while communicating with the D-Link DDNS service')
    error = True
finally:
    if error:
        f = open(os.path.join(path, 'last-ip'), 'w', 1)
        f.write(old_ip)
        sys.exit('')
