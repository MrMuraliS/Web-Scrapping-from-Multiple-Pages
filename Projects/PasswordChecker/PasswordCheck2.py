import requests
import hashlib
import sys

''' We are not allowed to send our password in plain text.
    We have hash our password before giving it to API. 
    and We should not even send the complete hashed password through API, if you do so you will get 400 error.

    the expectation is you should send only 5 digits of the hashed password.

    You can hash your password here: https://passwordsgenerator.net/sha1-hash-generator/
'''


def req_api_data(query):
    url = 'https://api.pwnedpasswords.com/range/' + str(query)
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching {res.status_code}, Please check the API')
    return res


def pwd_leaks_count(data, has_to_check):
    hashes = [line.split(':') for line in data.splitlines()]
    for h, count in hashes:
        if h == has_to_check:
            return count
    return 0


def pwd_api_check(password):
    hash_pwd = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    # return hash_pwd
    first_5_char, tail = hash_pwd[:5], hash_pwd[5:]
    response = req_api_data(first_5_char)
    response_data = response.text
    return pwd_leaks_count(response_data, tail)


def main(Password):
    for givenpwd in Password:
        count = pwd_api_check(givenpwd)
        if count:
            print(f'{givenpwd} was hacked {count} times, You should really change the password')
        else:
            print(f'Great, Your password ({givenpwd}) hasn\'n been hacked, You\'r good to use it')
    return 'done!'


main(sys.argv[1:])
