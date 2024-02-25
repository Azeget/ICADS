@dp.my_signal_event_register('токены')
def chex(event: MySignalEvent): 
try: 
user_id = VkApi(event.db.access_token, True)('users.get')[0]['id'] 
me_id = VkApi(event.db.me_token, True)('users.get')[0]['id'] 
except VkApiResponseException: 
pass 
 event.msg_op(2, f"""
Основной токен: {'исправен' if locals().get('user_id', 0) else 'не исправен'}
Токен VkMe: {'исправен' if locals().get('me_id', 0) else 'не исправен'}
""")
return "ok"
