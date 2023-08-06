import time

def time_str(sec):
    h = int(sec/3600)
    m = int(sec%3600/60)
    s = sec%60
    if h>0:
        str = '%d:%02d:%02d'%(h,m,s)
    elif m>0:
        str = '%02d:%02d'%(m,s)
    elif s>=1.0:
        str = '%.2fs'%s
    else:
        str = '%.2fms'%(s*1000)
    return str


class Progressbar:
    def __init__(self, iter ,length=0, on=True,time_on=False):
        self.on = on
        self.time_on = time_on
        self.i = -1
        self.iter = iter
        if length >0:
            self.len = length
        else:
            self.len = len(self.iter)
        self.last_message_len = 0
        self.message = ''
        if on:
            self.time = time.time()
            self.str = '[' + ' ' * 100 + ']'
            self.str += ' ' * 3 + '(' + ' ' * 8 + '/' + ' ' * 8 + ')'
            print(self.str, end='', flush=True)
        else:
            self.str = ''

    def __iter__(self):
        self.iter__ = self.iter.__iter__()
        return self

    def __next__(self):
        self.i += 1
        try:
            next = self.iter__.__next__()
            if self.on:
                percentage = 100.0 * self.i / self.len
                sub_number = int((percentage % 1)*10)
                percentage = int(percentage)
                if percentage == 100:
                    sub_number = ''
                else:
                    sub_number = chr(48+sub_number)
                str_b = '\b' * len(self.str)
                self.str = '[' + '#' * percentage + sub_number + ' ' * (99 - percentage) + ']'
                self.str += '%d%%(%d/%d)' % (percentage, self.i, self.len)
                if self.time_on and self.i>0:
                    time_end = time.time()
                    total_time = time_end-self.time
                    avg_time = total_time/self.i
                    rest_time = avg_time*(self.len-self.i)
                    self.str += '[' +time_str(avg_time) + '/' + time_str(total_time) + '/' + time_str(rest_time) +']'
                self.str += self.message
                print(str_b + self.str, end='', flush=True)
            return next
        except StopIteration:
            self.done()
            raise StopIteration

    def done(self):
        if self.on:
            str_b = '\b' * len(self.str)
            self.str = '[' + '#' * 100 + ']'
            self.str += '100%%(%d/%d)' % (self.len, self.len)
            if self.time_on and self.i>0:
                time_end = time.time()
                total_time = time_end-self.time
                avg_time = total_time/self.i
                self.str += '[' + time_str(avg_time) + '/' + time_str(total_time) + ']'
            self.str += self.message
            print(str_b + self.str, end='', flush=True)
            print('', flush=True)

    def show_message(self, str:str):
        self.message = str


