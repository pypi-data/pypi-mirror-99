import os
from pony.orm import *
from datetime import datetime


db = Database()

class GroupMessage(db.Entity):
    id = PrimaryKey(int, auto=True)
    dateTime = Required(datetime, precision=6)
    groupId = Required(str) # 群号
    memberId = Required(str) # 成员 QQ 号
    plain = Required(str) # 消息的文本内容


db_filepath = os.path.join(os.getcwd(), "dbFile")
if not os.path.exists(db_filepath):
    os.mkdir(db_filepath)
db.bind(provider='sqlite', filename=os.path.join(db_filepath, "messageTables.sqlite"), create_db=True)
db.generate_mapping(create_tables=True)