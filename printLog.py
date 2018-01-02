class PrintLog:
    def __init__(self):
        import time
        self.log_file = '.logs/'+time.strftime("%d.%m.%Y %H:%M")+'.log'
        open(self.log_file, 'w').close()

    def __call__(self, *args, sep=' ', end='\n', flush=False):
        import time, no_decor
        raw = sep.join(map(str, args))+end
        print(raw, sep='', end='', flush=flush)
        print(time.strftime("[%d.%m.%Y %H:%M:%S]: "), no_decor.no_decor(raw), sep='', end='', flush=flush,
              file=open(self.log_file, 'a'))