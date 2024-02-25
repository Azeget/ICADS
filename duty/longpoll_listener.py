from duty.objects import LongpollEvent, db, dp
from microvk import VkApi
from duty.utils import gen_secret
from logger import get_writer
from .app import app
from flask import request
import traceback
import json
import json,os,requests,time,asyncio,re
from typing import Tuple, List, Union
from threading import Thread
logger = get_writer('Приемник сигналов LP модуля')

def parse(text: str) -> Tuple[str, List[str], str]:
    matches = re.findall(r'(\S+)|\n(.*)', text)[1:]
    command = matches.pop(0)[0].lower()
    payload = ''
    args = [command]
    for i, match in enumerate(matches, 1):
        if match[0]:
            args.append(match[0])
        else:
            payload += match[1] + ('\n' if i < len(matches) else '')
    return command, args, payload

def lp_create_handler():
    db.lp_settings['key'] = "Прифф"
    while not db.lp_settings['key']:
        continue;
    try:
        import vk_api
        from vk_api.longpoll import VkLongPoll, VkEventType
    except:
        try:
            import subprocess,sys
            try:subprocess.check_call([sys.executable, "-m", "pip", "install", "vk-api"])
            except:''
            try:subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "vk-api"])
            except:''
            import vk_api
            from vk_api.longpoll import VkLongPoll, VkEventType
        except:
            os.system('pip3.8 install --user vk-api')
            try:
                import vk_api
                from vk_api.longpoll import VkLongPoll, VkEventType
            except:
                logger('не удалось установить модуль vk-api, лп не может быть запущен!')
                return;
    vk_session = vk_api.VkApi(token=db.access_token)
    api = vk_session.get_api()
    while True:
        try:
            if not db.lp_settings.get('key'): break;
            longpoll = VkLongPoll(vk_session)
            for event_ in longpoll.listen():
                if not db.lp_settings.get('key'): break;
                if event_.type == VkEventType.MESSAGE_NEW:
                    try:
                        message = api.messages.getById(message_ids=event_.message_id)['items'][0]
                        if message['from_id'] in db.lp_settings['ignored_users']:
                            try: time.sleep(0.2); api.messages.delete(message_ids=message['id']);
                            except: 'обработка ошибки удаления игнора';
                        ok = False
                        for x in db.lp_settings['prefixes']:
                            if x+' ' == message['text'][:len(x)+1].lower(): ok = True; break;
                        if not ok: continue;
                        command, args, payload = parse(message['text'])
                        event_one = LongpollEvent({
                            'access_key': '',
                            'message': message,
                            'chat': None,
                            'command': command,
                            'args': args,
                            'payload': payload
                        })
                        d = dp.longpoll_event_run(event_one)
                        db.sync()
                    except: '';
        except Exception as e: print(e); time.sleep(2);
Thread(target=lp_create_handler).start()
@app.route('/ping', methods=["POST"])
def ping():
    return "ok"
@app.route('/longpoll/event', methods=["POST"])
def longpoll():
    event = LongpollEvent(request.json)
    if event.data['access_key'] != event.db.lp_settings['key']:
        return "?"
    d = dp.longpoll_event_run(event)
    db.sync()
    if type(d) == dict:
        return json.dumps(d, ensure_ascii=False)
    return json.dumps({"response": "ok"}, ensure_ascii=False)
class error:
    AuthFail = 0
@app.route('/longpoll/start', methods=["POST"])
def get_data():
    token = json.loads(request.data)['token']
    try:
        if VkApi(token)('users.get')[0]['id'] != db.owner_id:
            raise ValueError
    except (KeyError, IndexError, ValueError):
        return json.dumps({'error': error.AuthFail})
    db.lp_settings['key'] = gen_secret(length=20)
    db.sync()
    return json.dumps({
            'chats': db.chats,
            'deleter': db.responses['del_self'],
            'settings': db.lp_settings,
            'self_id': db.owner_id
        })
@app.route('/longpoll/sync', methods=["POST"])
def sync_settings():
    data = request.json
    if data['access_key'] != db.lp_settings['key']:
        return "?"
    db.lp_settings.update(data['settings'])
    db.sync()
    return "ok"