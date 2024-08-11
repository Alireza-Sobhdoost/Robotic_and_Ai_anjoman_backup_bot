import requests  

# Replace 'YOUR_BOT_TOKEN' with your actual bot token  
BOT_TOKEN = '6927513102:AAECGNdiBmEFHRhxK2AzS81J9agm1h3AZi0'  
URL = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'  

def get_chat_id():  
    response = requests.get(URL)  
    data = response.json()  

    if 'result' in data and len(data['result']) > 0:  
        # Get the most recent update  
        latest_update = data['result'][-1]  
        chat_id = latest_update['message']['chat']['id']  
        print(f'Chat ID: {chat_id}')  
    else:  
        print('No updates available or bot not yet added to the group.')  

if __name__ == "__main__":  
    get_chat_id()