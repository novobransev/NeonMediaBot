from database.models import session_scope, Del_model
from main import bot


async def add_message_to_del(message):
    with session_scope() as session:
        try:
            chat_id = message.chat.id
            message_id = message.message_id
            records = await Del_model.create_record(session, chat_id, message_id)
            return records
        except Exception:
            pass


async def delete_messages(chat_id: int):
    with session_scope() as session:
        records = await Del_model.get_all_records(session, chat_id)
        for record in records:
            try:
                await bot.delete_message(chat_id=record.chat_id, message_id=record.message_id)
            except Exception:
                pass
            finally:
                records = await Del_model.del_record(session, record.id)