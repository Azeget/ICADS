from duty.objects import dp, LongpollEvent, MySignalEvent

@dp.longpoll_event_register('+префикс')
def addPrefix(event: LongpollEvent):
    if not event.args: event.msg_op(2, 'Укажи префикс!');
    if event.args[0].lower() in event.db.lp_settings['prefixes']: event.msg_op(2, 'Префикс существует');
    event.db.lp_settings['prefixes'].append(event.args[0].lower())
    event.msg_op(2, 'Префикс добавлен!')
@dp.longpoll_event_register('-префикс')
def removePrefix(event: LongpollEvent):
    if not event.args: event.msg_op(2, 'Укажи префикс!');
    if event.args[0].lower() not in event.db.lp_settings['prefixes']: event.msg_op(2, 'Префикс не существует');
    event.db.lp_settings['prefixes'].remove(event.args[0].lower())
    event.msg_op(2, 'Префикс удалён!')

@dp.longpoll_event_register('префиксы')
def listPrefix(event: LongpollEvent):
    prefixes = event.db.lp_settings['prefixes']
    if not prefixes:
        message = ('Я не знаю как ты этого достиг, но у тебя нет ни одного ' +
                   'LP префикса. На всякий случай добавил префикс "!л"'
                   )
        event.db.lp_settings['prefixes'].append('!л')
    else:
        message = 'Префиксы LP сигналов:'
        for prefix in prefixes:
            message += f'\n-- "{prefix}"'
    event.msg_op(2, message)


@dp.my_signal_event_register('лстарт')
def startLpHG(event: MySignalEvent):
    event.db.lp_settings['key'] = "1";
    event.msg_op(2, 'Лп запущен!')
@dp.my_signal_event_register('лстоп')
def stopLpHG(event: MySignalEvent):
    event.db.lp_settings['key'] = "";
    event.msg_op(2, 'Лп остановлен!')
