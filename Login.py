import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyotp
from kiteconnect import KiteConnect
import time

def generate_request_token(user_name,password,kite,Totp):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    # options.add_argument('--headless')
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(chrome_options=options)
  

    driver.get(kite.login_url())
    
    time.sleep(2)
    
    Input = driver.find_element_by_xpath("//input[@id='userid']")
    Input.send_keys(user_name)
    
    time.sleep(2)
    
    Password = driver.find_element_by_xpath("//input[@id='password']")
    Password.send_keys(password)
    
    time.sleep(2)
    
    driver.find_element_by_xpath("//button[@type='submit']").click()    
    time.sleep(4)
    PIN = driver.find_element_by_xpath("//input[@id='totp']")
    try:
        totp = pyotp.TOTP(Totp)
        pin=totp.now()
        print(f"TOTP Key:{Totp} and Pin:{pin}")
        PIN.send_keys(pin)
        time.sleep(3)
        driver.find_element_by_xpath("//button[@type='submit']").click()
    except:
        totp = pyotp.TOTP(totp)
        pin=totp.now()
        PIN.send_keys(pin)
        time.sleep(3)
        driver.find_element_by_xpath("//button[@type='submit']").click()
    time.sleep(5)
    request_token = driver.current_url.split('request_token=')[-1].split('&')
    for i in request_token:
        if '+' not in i:
            request_token = i
            break
    print(request_token)
    
    print("Request Token has been succesfully generated!!")
    driver.quit()
    return request_token


   
def login(api_key,api_secret,clientid,password,totp):
    print(api_key,api_secret,clientid,password,  totp)
    
    path = '.'

    

    kite = KiteConnect(api_key)
    #print(kite.login_url())

    Request_token = generate_request_token(clientid,password,kite,totp)
    

    try:
        Data = kite.generate_session(Request_token, api_secret)

    except Exception as e:
        print(e)
        Request_token = generate_request_token(clientid,password,kite,totp)
        Data = kite.generate_session(Request_token, api_secret)
   
    with open(f'{path}/Access_token.txt','w') as f:
        f.write(Data["access_token"])
    # Initialise
    #Kite = KiteConnect(api_key, Data['access_token'])
    kite.set_access_token(Data["access_token"])


    return kite