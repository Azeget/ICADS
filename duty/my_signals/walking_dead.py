from duty.objects import dp, MySignalEvent
from urllib import request
from datetime import datetime


@dp.longpoll_event_register('шаги')
@dp.my_signal_event_register('шаги')
def steps(event: MySignalEvent) -> str:
    args = event.msg['text'].split()
    if len(args) not in (2, 4):
        event.msg_op(1, f'Неверный формат.\nИспользование: "{args[0]} шаги [количество шагов <= 80000] [дистанция в метрах <= 50000]".\nЛибо: "{args[0]} шаги"')
    if len(args) == 4:
        steps, distance = args[1], args[2]
    else: 
        steps, distance = 80000, 50000
    date = datetime.today().strftime('%Y-%m-%d')
    user_agent = 'VKAndroidApp/7.7-10445 (Android 11; SDK 30; arm64-v8a; Xiaomi M2003J15SC; ru; 2340x1080)'
    request.urlopen(request.Request('https://api.vk.com/method/vkRun.setSteps?steps='+str(steps)+'&distance='+str(distance)+'&date='+date+'&access_token='+event.db.me_token+'&v=5.131', headers={'User-Agent': user_agent})).read().decode('utf-8')
    event.msg_op(1, '👍Готово👍')
    return "ok"
