from concurrent.futures import ThreadPoolExecutor, wait
from pysquid import stream_logger
from pysquid.plugin import Hook


class ThreadedEngine():

    def __init__(self, template, plugins, log=None):
        self.template = template
        self.plugins = plugins
        self.log = log if log else stream_logger()
        self.pools = {}

    def build(self):

        services = self.template.get('services')
        plugins = self.plugins
        
        pools = {
            'thread': {}
        }

        playbook = {}

        for sid, service in services.items():

            #pool = service.get('__pool__')
            mode = service.get('__mode__')
            plugin = service.get('__plugin__')
            workers = service.get('__workers__')

            if mode not in pools or plugin not in plugins:
                continue

            enabled_workers = set(workers.keys())

            plugin_ = plugins.get(plugin)()
            plugin_.add_service(service, self.template)

            setup = plugin_.iterate_workers(enabled_workers)

            for pid, stages in setup.items():
                if pid not in playbook:
                    playbook[pid] = {}
                    
                for sid, stage in stages.items():
                    if sid not in playbook[pid]:
                        playbook[pid][sid] = []

                    playbook[pid][sid] = playbook[pid][sid] + setup[pid][sid] 

        pools['thread'] = playbook
        self.pools = pools
        
    def exec_pool(self, hook: Hook = None):

        pools = self.pools.get('thread')        
        futures = set()

        hook = hook if isinstance(hook, Hook) else Hook()

        for pid, pool in pools.items():
            self.log.info(f'Running pool {pid}')
            e = ThreadPoolExecutor()
            future = e.submit(self.exec_workers, pool, hook)
            futures.add(future)

        self.log.info(f'Waiting on {futures}')
        wait(futures)
        self.log.info(f'Future done: {futures}')
            
    def exec_workers(self, pool, hook):

        e = ThreadPoolExecutor()
        futures = set()

        pipeline = dict(sorted(pool.items(), key=lambda item: item[0]))
        
        for sid, stage in pipeline.items():
            
            for worker in stage:
                # Set worker and run init
                hook.set_worker(worker)
                hook.init()
                
                worker.pre()
                futures.add(e.submit(worker.apply))
                
            wait(futures)

            for worker in stage:                
                worker.post()
                hook.set_worker(worker)
                hook.cleanup()
                
        return True
    


