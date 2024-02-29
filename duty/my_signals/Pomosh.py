from duty.objects import dp, MySignalEvent

@dp.longpoll_event_register('упр', 'адм')
@dp.my_signal_event_register('упр', 'адм')
def a(event: MySignalEvent) -> str:
    event.edit(f'''
     👨‍💻Упраляющие проектом👨‍💻

     🤴Разработчик :
     1. [https://vk.com/mavan_best|Mavan] 
     📌Небеспокоить 
     
     🤵Администратор :
     1. [https://vk.com/james_gladkih|James] 
     📌Разрешено писать
     
     👮‍♂️Агент :
     1. [https://vk.com/adam_frymov|Adam]
     📌Разрешено писать

     📍Если вам нужна другая информация то вы можете найти её по команде [преф] хелп
    '''.replace('    ', ''))
    return "ok"
