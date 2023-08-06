import os
from pony.orm import *
from datetime import datetime

from . import db_filepath


db = Database()

class GroupMessage(db.Entity):
    id = PrimaryKey(int, auto=True)
    dateTime = Required(datetime, precision=6)
    groupId = Required(str) # 群号
    memberId = Required(str) # 成员 QQ 号
    plain = Required(str) # 消息的文本内容

db.bind(provider='sqlite', filename=os.path.join(db_filepath, "messageTables.sqlite"), create_db=True)
db.generate_mapping(create_tables=True)