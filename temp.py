class MyDict(object):
    """统计排序"""
    def __init__(self):
        self.mydict = {}

    def update(self, value):
        exists = self.mydict.get(value)
        if exists is None:
            self.mydict.setdefault(value, 1)
        else:
            self.mydict[value] += 1

    def sort(self):
        a = sorted(self.mydict.items(), key=lambda item: item[1], reverse=True)[:200]
        for k, v in a:
            print('{}: {}'.format(k, v))
