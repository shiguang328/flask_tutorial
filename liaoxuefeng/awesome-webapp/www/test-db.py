import orm
import asyncio
from models import User, Blog, Comment

async def test(loop):
    await orm.create_poop(loop, host='192.168.1.104', user='nds', password='lucky2016',
                               db='liaoxuefeng')
    u = User(name='Liu Zhipeng', email='leo@example.com', passwd='123456',
             image='about:blank')
    await u.save()

async def find(loop):
    await orm.create_poop(loop, host='192.168.1.104', user='nds', password='lucky2016',
                          db='liaoxuefeng')
    rs = await User.findAll()
    print('find: %s' % rs)

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
# loop.run_until_complete(find(loop))
loop.run_forever()