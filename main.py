import requests, time, random
import threading

def generation_email():
    response = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1').json()
    return response[0]

def generation_pass(num=10):
    text = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    password = ''
    for i in range(num):
        password += text[random.randint(0, 61)]
    return password

def check_email(email):
    while True:
        response = requests.get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={email.split("@")[0]}&domain={email.split("@")[1]}')
        if len(response.json()) > 0:
            response = requests.get(f'https://www.1secmail.com/api/v1/?action=readMessage&login={email.split("@")[0]}&domain={email.split("@")[1]}&id={response.json()[0]["id"]}')
            #verif_code = response.json()['body'].replace('<p>Dear user,Your registration verification code is:</p>\n<p style="font-family: Arial, sans-serif; background-color: #f3f3f3; padding: 10px; border-radius: 5px;">\n  <strong>','').replace('</strong>\n</p>\n<p>The verification code is only valid for <strong>5minute</strong>.</p>\n<p>If you are not registering, please ignore this email.</p>\n', '')
            verif_code = response.json()['body'].replace('<p>Dear user,</p>\n<p>Thank you for registering with Midjourneyai. To verify your registration information and protect your account security, we need you to complete email verification with the verification code.</p>\n<p>Please use the following verification code to complete the registration process:</p>\n<p style="font-family: Arial, sans-serif; background-color: #f3f3f3; padding: 10px; border-radius: 5px;">\n  Verification Code: <strong>','').replace('</strong>\n</p>\n<p>Please enter this code on the registration page to complete the verification. The verification code is only valid on the registration page and its validity period is <strong>5minute</strong>.</p>\n<p>If you did not initiate this registration, please ignore this email.</p>\n','')
            return verif_code
        time.sleep(2)

def result_acc(text):
    with open('result.txt', 'a') as file:
        file.write(text)

def generation_acc_gpt():
    headers = {
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0 (Edition Yx GX 03)',
    }

    email = generation_email()
    response = requests.get(
        f'https://mjaiserver.cuilutech.com/api/auth/send-captcha?email={email}&type=register',
        headers=headers,
    )

    password = generation_pass()
    verif_code = check_email(email)
    json_data = {
    'email': email,
    'password': password,
    'confirmPassword': password,
    'verificationCode': verif_code,
    }
    response = requests.post('https://mjaiserver.cuilutech.com/api/auth/v2/register', headers=headers, json=json_data)
    if response.json()['msg'] == 'success':
        print(f'[+] {email}:{password}')
        result_acc(f'{email}:{password}\n')
    else:
        print('[-] ERROR')
        print(response.json())

"""
email = generation_email()
print(email)
while True:
    print(check_email(email))
"""

threads = []
for i in range(1600):
    thread = threading.Thread(target=generation_acc_gpt)
    thread.start()
    threads.append(thread)

# Дождаться окончания всех потоков
for thread in threads:
    thread.join()

