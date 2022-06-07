from sre_constants import SUCCESS
import requests, random, threading, time, names, os
from art import *
from colorama import Fore, Back, Style, init
init(autoreset=True)
from datetime import date
today = date.today()

errors = 0
success = 0

Art=text2art("SSENSE Account Generator")
print(Fore.MAGENTA + Art + "\n")

catchall = input("Enter your catchall: ")
password = input("Enter your password: ")
proxies = input("Use proxies? (y/n): ")
if proxies == "y":
    proxies = True
    with open("proxies.txt") as f:
    #Count the number of lines
        proxyCount = sum(1 for _ in f)
        print(f"{proxyCount} proxies loaded")
                #For every thread use a random proxy
else:
    proxies = False
               
amount = input("Enter the amount of accounts you want to generate: ")
print(f"Generating {amount} account(s)...")
time.sleep(1)

os.system(f'title SSENSE Account Generator - Total: {amount} - Success: {success} - Errors: {errors}')


def generate(success, errors, catchall, password, proxies):

    if proxies == True:
        with open("proxies.txt") as f:
            proxy = f.readlines()
            #Randomly selects a proxy
            proxy = proxy[random.randint(0,proxyCount-1)].strip()
            proxies = {
                'http': proxy,
                'https': proxy,
                }
    else:
        proxies = False

    try:

        firstName = names.get_first_name()
        lastName = names.get_last_name()

        randomEmail = firstName + lastName + "@" + catchall

        headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
        }

        payload = {
            'confirmpassword': password,
            'email': randomEmail,
            'gender': "men",
            'password': password,
            'source': "SSENSE_EN_SIGNUP"
        }

        req = requests.post(f'https://www.ssense.com/en-us/account/register', headers=headers, json=payload ,proxies=proxies, timeout=5)

        if req.status_code == 200:
            print(Fore.GREEN + f"Generated Account | {randomEmail} | {password}")
            success += 1
            os.system(f'title SSENSE Account Generator - Total: {amount} - Success: {success} - Errors: {errors}')     
        else:
            print(Fore.RED + "Error generating account")
            errors += 1
            os.system(f'title SSENSE Account Generator - Total: {amount} - Success: {success} - Errors: {errors}')
            time.sleep(1)
            generate(success, errors, catchall, password, proxies)
    
    except requests.exceptions.ConnectionError:
        print(Fore.RED + "Connection Error")
        time.sleep(1)
        generate(success, errors, catchall, password, proxies)
    except requests.exceptions.Timeout:
        print(Fore.RED + "Timeout Error")
        time.sleep(1)
        generate(success, errors, catchall, password, proxies)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + "Unkown Error")
        time.sleep(1)
        generate(success, errors, catchall, password, proxies)

    if success == int(amount):
        fileName = "SSENSE" + "-" + today.strftime("%H-%M-%S")
        with open(f"Accounts/{fileName}.txt", "a") as f:
            f.write(f"{randomEmail} | {password}\n")
            f.close()
            print(f"Accounts saved to {fileName}.txt")
    else:
       pass   

for _ in range(int(amount)):
    t = threading.Thread(target=generate(success, errors, catchall, password, proxies))
    t.start()
