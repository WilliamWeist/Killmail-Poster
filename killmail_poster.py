import time, threading
import requests, pyperclip

killmails = []

def read_clipboard():
    print('Reading the clipboard...')
    while True:
        killmails.append(pyperclip.waitForPaste())
        pyperclip.copy('')

def post_killmails(killmails: list):
    while True:
        if len(killmails) > 0:
            killmail = killmails.pop(0)
            if killmail.startswith('https://esi.evetech.net/v1/killmails/'):
                print(f'Posting: {killmail}')
                killmail = killmail.replace('https://esi.evetech.net/v1/killmails/', '').replace('/?datasource=tranquility', '')
                id_hash = killmail.split('/')
                response = requests.post(f'https://zkillboard.com/api/killmail/add/{id_hash[0]}/{id_hash[1]}/')
                status = response.json()['status']
                print(f'{status}: ' , end='')
                if status == 'success':
                    print(response.json()['url'].replace('\\', ''))
                else:
                    print(response.json()['error'])
        else:
            time.sleep(1)

if __name__ == '__main__':
    killmail_poster = threading.Thread(target = post_killmails, args=(killmails,), daemon=True)
    killmail_poster.start()
    read_clipboard()