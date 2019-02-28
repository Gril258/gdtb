import asyncio
import app
import threading
import time
import traceback
import connectors

def environment():
    global message
    message = {}

class instance():
    """main reactor entrypoint"""
    def __init__(self):
        self.config = app.base.config().json
        self.loop = asyncio

        with app.base.server() as server:
                print(server.get_status())
                inter = float(self.config['reactor']['task_interval'])
                print("starting reactor loop")
                c = 1
                while len(server.core_stack) < int(self.config['reactor']['cores']):
                    print("spawn core n %s" % c)
                    server.core_stack.append(spawnCore(c, "t%s" % c, c, server))
                    server.core_stack[-1].start()
                    c += 1
                    print(c)
                    time.sleep(1)
                asyncio.set_event_loop(asyncio.new_event_loop())
                loop = asyncio.get_event_loop()
                loop.run_forever()
    	




class spawnCore (threading.Thread):
    def __init__(self, threadID, name, counter, server):
        threading.Thread.__init__(self)
        self.server = server
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print("Starting " + self.name)
        self.spawn_core(self.counter)
        print("Exiting " + self.name)


    def spawn_core(self, core_id):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.server.register_core(core_id, self)
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.StartCore(core_id))
        loop.run_forever()

    async def flushstdout(self):
        while True:
            sys.stdout.flush()
            await asyncio.sleep(1)
    
    async def StartCore(self, core_id):
        while True:
            print("Next Task on core %s" % core_id)
            try:
                async with connectors.miband.entrypoint() as h:
                    print("Core Tick Start")
                    result = await h.DoTask()
                    h.TaskStatus = "done"
                    print("Core Tick")
            except:
                print("No task done")
                traceback.print_exc()
            finally:
                await asyncio.sleep(3)
