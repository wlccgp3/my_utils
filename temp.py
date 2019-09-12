
from my_utils import ItemLoader
from my_utils.tools import *

page_source = open('/Users/miles/Desktop/demo.html', 'r', encoding='utf-8').read()
loader = ItemLoader(text=page_source)

a = loader.css('::text').proc(ReFind(r'\d+'), ReSub(r'\d', '我'))
print(a)
