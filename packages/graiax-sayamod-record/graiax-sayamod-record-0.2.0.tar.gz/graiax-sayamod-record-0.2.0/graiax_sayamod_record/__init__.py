import asyncio

from graia.broadcast import Broadcast

from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain, Source
from graia.application.group import Group, Member
from graia.application import GraiaMiraiApplication

from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from pony.orm import *

from .databases import messageTables


saya = Saya.current()
channel = Channel.current()

loop = asyncio.get_event_loop()
broadcast = Broadcast(loop=loop)
db = Database()

@channel.use(ListenerSchema(
    listening_events=["GroupMessage"] # 填入你需要监听的事件
))
@db_session
async def message_tables_group_message_listener(app: GraiaMiraiApplication, group: Group, member: Member, messageChain: MessageChain):
    if messageChain.has(Plain):
        messageTables.GroupMessage(
            groupId=str(group.id), 
            dateTime=messageChain.getFirst(Source).time,
            memberId=str(member.id), 
            plain=messageChain.include(Plain).asDisplay()
        )
        commit()