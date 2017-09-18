# Python168的学习笔记2

## 深入循环内部

关于for循环，其实质是利用被循环对象的__iter__,或者__getitem__属性接口，由可迭代对象得到迭代器。for循环就是不断调用.next()，直到最终捕获到stop。

```python
import requests
from collections import Iterable,Iterator

class WeatherIterator(Iterator):  # 可迭代对象
    def __init__(self,cities):
        self.cities = cities
        self.index = 0

    def getweather(self,city):
        r = requests.get(u'http://wthrcdn.etouch.cn/weather_mini?city='+city)  # 这是一个免费的天气api
        data = r.json()['data']['forecast'][0]
        return '%s:%s,%s'%(city,data['low'],data['high'])

    def next(self):
        if self.index == len(self.cities):
            raise StopIteration
        city = self.cities[self.index]
        self.index += 1
        return self.getweather(city)

class WeatherIterable(Iterable):  # 迭代器对象
    def __init__(self,cities):
        self.cities = cities

    def __iter__(self):  # 迭代器接口
        return WeatherIterator(self.cities)

for x in WeatherIterable([u'北京',u'上海',u'广州',u'长春']):
    print x
```

要知道一个顺序，解释器先去寻找__iter__方法，找不到才去找__getitem__，__getitem__
