from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import os.path
from variables import logging
db = SqliteExtDatabase('database.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True)


class PassDB(BaseModel):
    user = ForeignKeyField(User)
    filename = CharField(unique=True)
    real_filename = CharField()

    def save(self, force_insert=False, only=None):
        if os.path.isfile(self.filename):
            self.filename = self.filename.split('/')[-1]
            return super(PassDB, self).save(force_insert=force_insert,only=only)
        else:
            logging.error("File was not created for some reason")
            raise FileNotFoundError("File not exists")

    @staticmethod
    def get_user_dbs(username):
        return PassDB.select().join(User).where(User.username == username)

db.connect()
