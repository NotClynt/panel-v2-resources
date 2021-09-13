import os
#Do 
#pip install time
#pip install daretime
import time
import datetime

if os.name == "nt":
    hwid = str(subprocess.check_output(
        'wmic csproduct get uuid')).split('\\r\\n')[1].strip('\\r').strip()#grabs Hardware id

domain = 'domain.com/panel'#replace with your domain
apikey = 'api key from config file on panel'
username = input(f'[Login] Username >> ')
password = input(f'[Login] Password >> ')    

password_bytes=password.encode('ascii')
base64_bytes = base64.b64encode(password_bytes)
password = base64_bytes.decode('ascii')
hwid = f"{hwid}"
hwid = base64.b64encode(hwid.encode("ascii"))
r = requests.get(f'https://{domain}/api.php?user={username}&pass={password}&hwid={hwid.decode("utf-8")}&key={apikey}')
json_data = json.loads(r.text)
#this print ist just for developing
#print(json_data) 
#usernsme and password check
if(json_data["status"] == "failed" and json_data["error"] == "Invalid username." or json_data["status"] == "failed" and json_data["error"] == "Invalid password."):
    print(f"{Fore.RED}[ERROR]{Fore.RESET} {Fore.BLUE}Invalid login data!")
    input("Press enter to exit")
    os._exit(0)
if(json_data["banned"] == "1"):#check if user is banned
    print(f"{Fore.RED}[ERROR]{Fore.RESET} {Fore.BLUE}You are banned!")
    input("Press enter to exit")
    os._exit(0)
if(json_data["hwid"] != base64.b64decode(hwid).decode("utf-8") and json_data["hwid"] != None):#checks if hwid match
    print(f"{Fore.RED}[ERROR]{Fore.RESET} {Fore.BLUE}HWID is not matching!")
    input("Press enter to exit")
    os._exit(0)
if(json_data["sub"] == None):#check if user habe a active sub
    print(f"{Fore.RED}[ERROR]{Fore.RESET} {Fore.BLUE}You have no active subscription")
    input("Press enter to exit")
    os._exit(0)
currdate = datetime.datetime.strptime(str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day), '%Y-%m-%d').timestamp()
subdate = datetime.datetime.strptime(json_data["sub"], '%Y-%m-%d').timestamp()
if(currdate >= subdate):
    print(f"{Fore.RED}[ERROR]{Fore.RESET} {Fore.BLUE}Your subscription expired!")
    input("Press enter to exit")
    os._exit(0) 
