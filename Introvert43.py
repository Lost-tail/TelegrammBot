import requests
import time
from bs4 import BeautifulSoup
class Introvert:
    def __init__(self,token):
        self.token = token
        self.api_url = 'https://api.telegram.org/bot{}/'.format(token)
    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params={'timeout':timeout,'offset':offset}
        result = requests.get(self.api_url+method,params).json()
        return result['result']
    def get_last_update(self):
        get_result = self.get_updates()
        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = None
        return last_update
    def send_message(self,chat,text):
        params = {'chat_id':chat,'text':text}
        method='sendMessage'
        resp=requests.post(self.api_url+method,params)
        return resp
    def list(self):
        text="Вот все, что ты можешь спросить у меня:\n/list - список команд\n/time - время\n/NY - сколько осталось до НГ\n/weather - погода в Москве\n/RV - для Р.В."
        return text
    def weather(self):
        url='https://weather.rambler.ru/v-moskve/now/'
        req = requests.get(url)
        soup = BeautifulSoup(req.text,'html.parser')
        weather = soup.select('#header-space > div.uLCQ > div._3GRJ > div:nth-child(1) > div._2rRP > div:nth-child(2) > div.nUoY > div._3yJY > div > div > div')
        return str(weather).split('>')[1].split('<')[0]
    def time(self):
        time1 = time.strftime("%H:%M:%S",time.gmtime(time.time()+10800))
        return time1
    def NY(self):
        data = time.strftime("%Y.%m.%d",time.gmtime(time.time()+10800))
        time1 = self.time()
        NY_data = ['2020','12','31']
        NY_time = ['23','59','59']
        data = data.split('.')
        time1 = time1.split(':')
        a=[0]*6
        for i in range(3):
            x = int(NY_data[i])-int(data[i])
            y = int(NY_time[i])-int(time1[i])
            a[i],a[i+3]=x,y
        return a[1:]
        
        
Introvert43 = Introvert('1489561153:AAHG-SlwURccPLCxu03XofC7zZSCCixqMY8')

def main(Bot):  
    new_offset = None
    while True:
        Bot.get_updates(new_offset)
        last_update = Bot.get_last_update()
        if last_update:
            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            if last_chat_text=='/list':
                text = Bot.list()
            elif last_chat_text=='/weather':
                text = 'В Москве сейчас {} градусов'.format(Bot.weather())
            elif last_chat_text == '/time':
                text = 'Московское время: {}'.format(Bot.time())
            elif last_chat_text == '/NY':
                text = 'До Нового Года осталось: {} мес, {} дн, {} ч, {} мин, {} сек.'.format(*Bot.NY())
            elif last_chat_text == '/RV':
                text = "DRY - don't repeat yourself. Неповеришь откуда я узнал это)"
            else:
                text = 'Не хочу с тобой разговаривать...\n'+Bot.list()
            Bot.send_message(last_chat_id,text)
            new_offset=last_update_id+1
               

if __name__ == '__main__':
    try:
        main(Introvert43)
    except KeyboardInterrupt:
        exit()

