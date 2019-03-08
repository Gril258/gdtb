import sys, json
import asyncio
import aiopg
import app
from . import reactor


def init():
    print("Starting global Variables")
    global message
    global config
    message = {}
    #global portal
    #portal = geocore.maps.portal(slug="skoda-parking")
    #portal.populate()
    config = app.base.config().json


class Handler():
    global config
    """Handler read data from task database and do it then update result to database"""
    def __init__(self):
        #print("init handler ------ %s" % config)
        self.config = app.base.config().json
        #print("init handler ------ %s" % config)

    async def __aenter__(self):
        async with AsyncDatabase(dbname=self.config['database']['name'], user=self.config['database']['user'], password=self.config['database']['password'], host=self.config['database']['host'], port=self.config['database']['port']) as self.ReactorDatabase:
            print("exit aenter")
            if (await self.GetTask()):
                self.TaskStatus = 'loaded'
                print(self.TaskStatus)
                await self.UpdateTask()
            else:
                self.TaskStatus = False
        return self

    async def __aexit__(self, *args, **kwargs):
        print("aexit")
        if self.TaskStatus:
            await self.UpdateTask()
        await self.ReactorDatabase.__aexit__(*args, **kwargs)
        #await self._conn.__aexit__(*args, **kwargs)

    async def GetTask(self):
        q = "SELECT id, name, data, status FROM reactor WHERE status = 'ready' LIMIT 1"
        print(q)
        result = await self.ReactorDatabase.get(q)
        print(result)
        if len(result) > 0:
            for each in result:
                self.TaskId = each[0]
                self.TaskName = each[1]
                self.TaskData = each[2]
                self.TaskStatus = each[3]
            return True
        else:
            return False

    async def DoTask(self):
        print("TaskId = %s" % self.TaskId)
        print("TaskName = %s" % self.TaskName)
        print("TaskData = %s" % self.TaskData)
        self.TaskStatus = "running"
        call = "%s(self.TaskData)"
        result = eval(call)
        await self.UpdateTask()
        return True

    async def UpdateTask(self):
        q = "UPDATE reactor SET status = %s WHERE id = %s"
        v = (self.TaskStatus, self.TaskId)
        await self.ReactorDatabase.update(q,v)
        return "done"



class AsyncDatabase:
    def __init__(self, dbname, host, user, password, port):
        self.dbname = dbname
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.dsn = "dbname='%s' user='%s' host='%s' password='%s' port='%s'" % (self.dbname, self.user, self.host, self.password, self.port)
        print(self.dsn)

    async def __aenter__(self):
        #print("aenter")
        return self

    async def __aexit__(self, *args, **kwargs):
        #print("aexit")
        await self.pool.__aexit__(*args, **kwargs)

    async def get(self, querry):
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        async with aiopg.create_pool(self.dsn, loop=loop) as self.pool:
            async with self.pool.acquire() as self.conn:
                async with self.conn.cursor() as self.cur:
                    print("Execute q")
                    await self.cur.execute(querry)
                    ret = []
                    async for row in self.cur:
                        ret.append(row)
                    return ret

    async def update(self, querry, values):
        #print("update - %s %s" % (querry, values) )
        async with aiopg.create_pool(self.dsn) as self.pool:
            async with self.pool.acquire() as self.conn:
                async with self.conn.cursor() as self.cur:
                    await self.cur.execute(querry, values)
                    await self.cur.execute('COMMIT transaction;')
                    #await self.conn.commit()
                    #ret = []
                    #async for row in self.cur:
                    #    ret.append(row)
                    #return ret

async def get_status():
    print("Starting message system")
    reactor.core.message['db_status'] = "Warming up"
    reactor.core.message['db_statistic'] = 0
    while True:
        print("DB task status: %s - statistic: %s / %ss" % (reactor.core.message['db_status'], reactor.core.message['db_statistic'], reactor.core.config['reactor']['status_interval']))
        reactor.core.message['db_statistic'] = 0
        print("Minolta WS task status: %s - statistic: %s / %ss" % (reactor.core.message['minolta_ws_status'], reactor.core.message['minolta_ws_statistic'], reactor.core.config['reactor']['status_interval']))
        reactor.core.message['minolta_ws_statistic'] = 0
        print("Cleerio WS task status: %s - statistic: %s / %ss" % (reactor.core.message['cleerio_ws_status'], reactor.core.message['cleerio_ws_statistic'], reactor.core.config['reactor']['status_interval']))
        reactor.core.message['cleerio_ws_statistic'] = 0
        if reactor.core.config['reactor']['status_verbosity'] == "high":
            print("Minolta WS ws_data %s" % reactor.mtws.ws_data)  
        await asyncio.sleep(float(reactor.core.config['reactor']['status_interval']))
