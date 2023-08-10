from contextlib import contextmanager
from sqlalchemy import create_engine, BigInteger
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:123@localhost/db_neon_bot')

Session = sessionmaker(bind=engine)
Base = declarative_base()


class Del_model(Base):
    __tablename__ = 'to_delete'
    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger)
    message_id = Column(Integer)
    user_tg_id = Column(BigInteger)

    @staticmethod
    async def create_record(session, chat_id, message_id):
        create_an_entry = Del_model(
            chat_id=chat_id,
            message_id=message_id
        )
        session.add(create_an_entry)
        session.commit()
        return create_an_entry

    @staticmethod
    async def get_all_records(session, chat_id):
        del_list = session.query(Del_model).filter(Del_model.chat_id == chat_id).all()
        return del_list

    @staticmethod
    async def del_record(session, id):
        record = session.query(Del_model).filter(Del_model.id == id).first()
        session.delete(record)
        return True


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class MessageTextFromBot(Base):
    __tablename__ = 'message_text'
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    key_word = Column(Text)


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    title = Column(Text)


Base.metadata.create_all(bind=engine)
