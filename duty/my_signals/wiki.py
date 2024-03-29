from duty.objects import dp, MySignalEvent
from duty.utils import find_mention_by_event
import wikipedia

@dp.my_signal_event_register('вики')
def wiki_command(event: MySignalEvent) -> str:
    query = event.payload

    if query:
        query = query.strip() 
        try:
            wiki_summary = wikipedia.summary(query, sentences=3)  
            event.api.messages.send(peer_id=peer_id, message=wiki_summary, random_id=0)
        except wikipedia.exceptions.PageError:
            event.api.messages.send(peer_id=peer_id, message="❌По вашему запросу ничего не найдено❌", random_id=0)
        except wikipedia.exceptions.DisambiguationError as e:
            event.api.messages.send(peer_id=peer_id, message="🤔Уточните ваш запрос, найдено несколько подходящих статей🤔", random_id=0)

    return "ok"
