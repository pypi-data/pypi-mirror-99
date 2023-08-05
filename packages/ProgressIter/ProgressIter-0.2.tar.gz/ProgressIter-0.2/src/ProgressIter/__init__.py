
class Progressbar:
    def __init__(self, iter ,length=0, on=True):
        self.on = on
        self.i = -1
        self.iter = iter
        if length >0:
            self.len = length
        else:
            self.len = len(self.iter)
        self.last_message_len = 0
        self.message = ''
        if on:
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
            self.str += self.message
            print(str_b + self.str, end='', flush=True)
            print('', flush=True)

    def show_message(self, str:str):
        self.message = str
