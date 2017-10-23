# 提前实例化，引用的时候就是引用它的实例
class Singleton1:
    pass

singleton1 = Singleton1()


# 用元类比改写new的好处是，metaclass只会调用一次，而new则会每次都被调用
class Singleton2(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(Singleton2, cls).__call__(*args, **kwargs)
        else:  # 若需要每次都调用init
            cls._instance[cls].__init__(*args, **kwargs)
        return cls._instance[cls]


class SubClass2(metaclass=Singleton2):
    pass


# 装饰器
def singleton3(class_):
    _instance_dict = {}

    def generator(*args, **kwargs):
        if class_ not in _instance_dict:
            _instance_dict[class_] = class_(*args, **kwargs)
        return _instance_dict[class_]
    return generator


@singleton3
class SubClass3:
    pass
