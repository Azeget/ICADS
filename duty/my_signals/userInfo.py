from duty.objects import dp, MySignalEvent
from duty.utils import find_mention_by_event
from microvk import VkApiResponseException


@dp.longpoll_event_register('юинфо', 'ктоты')
@dp.my_signal_event_register('юинфо', 'ктоты')
def change_friend_status(event: MySignalEvent) -> str:
    user_id = find_mention_by_event(event)
    if user_id:
        rDate = "❗ Ошибка получения даты регистрации"
        try:
            try:
                import requests,bs4
            except:
                import os
                os.system("pip install bs4")
                import requests,bs4
            response = requests.get(f'https://vk.com/foaf.php?id={user_id}')
            xml = response.text
            soup = bs4.BeautifulSoup(xml, 'lxml')
            created = soup.find('ya:created').get('dc:date')
            rDate=f'🗓 Дата регистрации: {created[8:10]}.{created[5:7]}.{created[0:4]}'
        except: ''
        okInfo = False
        try:
            info = event.api('users.get', user_ids=user_id, fields="sex,is_closed,blacklisted,blacklisted_by_me,status,photo_max_orig,counters,friend_status,city,first_name_abl,last_name_abl,last_seen,online,screen_name,bdate")[0]
            friend_status = str(info['friend_status']).replace('0', '🚫').replace('1', 'Заявка на расмотрении.').replace('2', '🔖Имеется входящая заявка.').replace('3', '✅')
            sex = str(info['sex']).replace('1', '👩').replace('2', '👨').replace('3', 'Не указан')
            is_closed = str(info['is_closed']).replace('True', '✅').replace('False', '🚫')
            blacklisted = str(info['blacklisted']).replace('1', '✅').replace('0', '🚫')
            blacklisted_by_me = str(info['blacklisted_by_me']).replace('1', '✅').replace('0', '🚫')
            if 'last_seen' in info: 
                last_seen = str(info['last_seen']['platform']).replace('1', 'Мобильная версия 📱').replace('2', 'Приложение для iPhone 📱').replace('3', 'Приложение для iPad 📱').replace('4', 'Приложение для Android 📱').replace('5', 'Приложение для Windows Phone 📱').replace('6', 'Приложение для Windows 10 📱').replace('7', 'Полная версия сайта 🖥️')
            else:
                last_seen = 'Онлайн скрыт 🔒.'     
            try:
                count_friends=info['counters']['friends']
            except:
                count_friends='Скрыто 🔒.'
            try:
                count_followers=info['counters']['followers']
            except:
                count_followers='Скрыто 🔒.'          
            okInfo = True
            msg = f"""
Информация о {info['first_name_abl']} {info['last_name_abl']}, {'Online' if info['online']==1 else 'Offline'}, {last_seen}

🆔️: {info['id']}
⚜️ Короткая ссылка: {info['screen_name']}
⚙️ Имя: {info['first_name']}
⚙ Фамилия: {info['last_name']}
👥 Кол-во друзей: {count_friends}
{rDate}
🎉 Дата рождение: {info['bdate'] if 'bdate' in info else 'Скрыто 🔒.'}
🌆 Город: {info['city']['title'] if 'city' in info else 'Не указан.'}
👨‍💼 Друзья: {friend_status}
✍🏻 Подписчики: {count_followers}
👨 Пол: {sex}
🔒 Закрытый прoфиль: {is_closed}
💬 Статус: {info['status']}
🚫 Я в чс: {blacklisted}
🚫 Он в чс: {blacklisted_by_me}
📷 Фото: {event.api('utils.getShortLink',url=info['photo_max_orig'])['short_url']}
"""
        except VkApiResponseException as e:
            okInfo = True
            msg = f"❗ Произошла ошибка VK №{e.error_code} {e.error_msg}"
        if not okInfo:
            msg = "❗ Произошла ошибка"
    else:
        msg = "❗ Необходимо пересланное сообщение или упоминание"
    event.msg_op(2, msg)
    return "ok"
