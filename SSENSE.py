import requests, random, threading, time, names, os
from art import *
from colorama import Fore, Back, Style, init
init(autoreset=True)
from datetime import date
today = date.today()


class Main:

    def __init__(self):

        self.success = 0
        self.errors = 0

        Art=text2art("SSENSE Account Generator")
        print(Fore.MAGENTA + Art + "\n")

        self.catchall = input("Enter your catchall: ")
        self.password = input("Enter your password: ")
        self.proxies = input("Use proxies? (y/n): ")
        if self.proxies == "y":
            self.proxies = True
            with open("proxies.txt") as f:
                #Count the number of lines
                self.proxyCount = sum(1 for _ in f)
                print(f"{self.proxyCount} proxies loaded")
                #For every thread use a random proxy
        else:
            self.proxies = False
               
        self.amount = input("Enter the amount of accounts you want to generate: ")
        print(f"Generating {self.amount} account(s)...")
        time.sleep(1)

        os.system(f'title SSENSE Account Generator | Total: {self.amount} | Success: {self.success} | Errors: {self.errors}')

        threads = []
        for _ in range(int(self.amount)):
            t = threading.Thread(target=self.generate)
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()
        self.generate()

    def generate(self):

        if self.proxies == True:
            with open("proxies.txt") as f:
                proxy = f.readlines()
                #Randomly selects a proxy
                proxy = proxy[random.randint(0,self.proxyCount-1)].strip()
                self.proxies = {
                    'http': proxy,
                    'https': proxy,
                    }
        else:
            self.proxies = False

        try:

            self.firstName = names.get_first_name()
            self.lastName = names.get_last_name()

            self.randomEmail = self.firstName + self.lastName + "@" + self.catchall

            headers = {
                'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
            }

            payload = {
                'confirmpassword': self.password,
                'email': self.randomEmail,
                'gender': "men",
                'password': self.password,
                'source': "SSENSE_EN_SIGNUP"
            }

            req = requests.post(f'https://www.ssense.com/en-us/account/register', headers=headers, json=payload ,proxies=self.proxies, timeout=5)

            if req.status_code == 200:
                print(Fore.GREEN + f"Generated Account | {self.randomEmail} | {self.password}")
                self.success += 1
                os.system(f'title SSENSE Account Generator | Total: {self.amount} | Success: {self.success} | Errors: {self.errors}')
                #Creates a txt file with the accounts and names the txt file with the site and date
                self.fileName = "SSENSE" + "-" + today.strftime("%d-%H-%M-%S")
                with open(f"Accounts/{self.fileName}.txt", "a") as f:
                    f.write(f"{self.randomEmail} | {self.password}\n")
                print(f"Accounts saved to {self.fileName}.txt")
            else:
                print(Fore.RED + "Error generating account")
                self.errors += 1
                os.system(f'title SSENSE Account Generator | Total: {self.amount} | Success: {self.success} | Errors: {self.errors}')
                self.sleep(1)
                self.generate()
        
        except requests.exceptions.ConnectionError:
            print(Fore.RED + "Connection Error")
            self.sleep(1)
            self.generate()
        except requests.exceptions.Timeout:
            print(Fore.RED + "Timeout Error")
            self.sleep(1)
            self.generate()
        except requests.exceptions.RequestException as e:
            print(Fore.RED + "Unkown Error")
            self.sleep(1)
            self.generate()
        
        

if __name__ == "__main__":
    Main()
