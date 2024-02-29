import requests

from duty.objects import MySignalEvent, dp
from duty.utils import find_mention_by_event, path_from_root


@dp.longpoll_event_register('группы')
@dp.my_signal_event_register('группы')
def groups(event: MySignalEvent) -> str:
    uid = find_mention_by_event(event) or event.db.owner_id
    message = requests.get(f'http://api.lisi4ka.ru/groups/{uid}').json()['message']
    event.edit(message, keep_forward_messages=1)


@dp.longpoll_event_register('приложения')
@dp.my_signal_event_register('приложения')
def apps(event: MySignalEvent) -> str:
    uid = find_mention_by_event(event) or event.db.owner_id
    message = requests.get(f'http://api.lisi4ka.ru/apps/{uid}').json()['message']
    event.edit(message, keep_forward_messages=1)


@dp.my_signal_event_register('отвязать')
def unbind_chat(event: MySignalEvent) -> str: 
    e = event.db.chats.pop(event.obj['chat'], None)
    message = 'Чат успешно отвязан!' if e else 'Такого чата уже нет.'
    event.edit(message)


@dp.my_signal_event_register('связать')
def iosif_prosti(event: MySignalEvent) -> str:
    upload_url = event.api(
        'docs.getUploadServer', type='audio_message'
    )['upload_url']
    with open(path_from_root('content', 'sorry.ogg'), "rb") as audio:
        uploaded = requests.post(upload_url, files={'file': audio}).json()

    att = event.api('docs.save', file=uploaded['file'])['audio_message']

    event.send(attachment=f'audio_message{att["owner_id"]}_{att["id"]}')


