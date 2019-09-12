
from my_utils import ItemLoader
from my_utils.tools import *

page_source = open('/Users/miles/Desktop/demo.html', 'r', encoding='utf-8').read()
loader = ItemLoader(text=page_source)

a = loader.css('.aaa ::text').proc(ReFind(r'\d+'), op=TakeOne(default=0))
print(a)
