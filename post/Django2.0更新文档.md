##写在前面

*兴趣使然，翻译并非全文，挑了一些重点和个人感兴趣的。*

# Django 2.0 来啦

这次更新并没有太大的不向前兼容的改动，除了不再支持python2这一点（笑）。

需要特别指出的几个改动有：

* url的路由规则有了更简单的写法，可以不写正则了喔。
* 增加了一个棒棒的移动端后台。
* ORM的操作语句现在支持开窗了，也就是可以加OVER了。

好了，没了。后面可以不看的了，谢谢。



----

## 新的url规则写法

新的官方例子为：

```python
path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail)
```

就是用`<类型:变量名称>`这个形式代替之前的正则写法，的确一眼看起来平易近人很多。内置了几个常用的类型：

* `str`：匹配除了`/`的所有非空字符，当不指定类型时，将默认为这个。
* `int`：匹配0和所有正数，传参的时候直接就是int了，不需要我们手动再转了。
* `slug`：匹配那些用`-`或者`_`连起来的ascii字母和数字。
* `uuid`：匹配那些符合UUID形式的，前提是字符都要是小写。
* `path`：跟str类似，只是这个会连`/`也匹配上。

### 自定义类型

```Python
class FourDigitYearConverter:
    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04d' % value
```

约定了三个协议：

* `regex`：规则的正则表达形式
* `to_python`：表示如何处理捕捉到的值，不能处理时要抛出`ValueError`（这个就是后面传给视图函数的参数）
* `to_url`：表示如何从python的形式转回字符串形式（这个会被用来重构url）

用`register_converter`来注册自己的类型。

```python
from django.urls import register_converter, path

register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatterns = [
    path('articles/<yyyy:year>/', views.year_archive),
    ...
]
```

### 正则匹配模式

也还是可以用回之前的正则模式的，只不过现在那个方法名改成了`re_path`：

```python
re_path('articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-_]+)/', views.article_detail)
```

就跟以前一样，是可以不加`<参数>`来对捕捉的值命名，传参的时候就只按位置来，而不是关键字传参罗。

然后就是关于规则中的指示参数：

```python
urlpatterns = [
    re_path(r'blog/(page-(\d+)/)?$', blog_articles),                  # bad
    re_path(r'comments/(?:page-(?P<page_number>\d+)/)?$', comments),  # good
]
```

虽然这两个规则都是为了捕捉一个页数，但是它们在重构url的时候会有不一样的表现。重构时，前者必须要传入一个关于页数的值，而后者传不传都可以。为什么呢？我们先看一下后者的表达式，有一个`?:`，这个规则是不会捕捉任何值的，但是在传值给视图函数时，将会`page-2/`这一块都传过去，而不只是`2`这个值，所以同理，在重构url的时候，需要传回这一块，而不是一个值。

## 友好的移动端后台

现在这个后台是响应式的了，而且支持所有主流移动设备。

##开窗

现在ORM语句可以用开窗了。

## 其他个人感兴趣的

### sitemaps

`GenericSitemap`加了`protocol`关键字参数，可以让我们手动选择`http`或者`https`。

###cache

`cache.set_many()`现在会在插入失败时返回由那些失败的值组成的列表。

### models

`QuerySet.iterator()`加了个`chunk_size`关键字来控制取回行数的数量。

`QuerySet.earliest(),QuerySet.latest(),Meta.get_latest_by`现在可以指定多个值域。

`aggregation`加了一个`filter`关键字来筛选。

`QuerySet.values_list()`加了一个`named`参数，可以将返回值变为`nametuples`形式。

### pagination

加了一个`get_page`方法，这下子不用我们手动去捕捉那两个异常了。

### 一些不兼容的地方

`QuerySet.reverser(), QuerySet.last()`现在不能用在查询切片以后了。

创建表单时，可选参数只能用关键字形式来传了。

`models.Index`现在也只接受关键字参数了。

现在也可以在SQLite用外键约束了。

### 其他

现在默认的error handlers是一个实体了，而不是之前像包路径那样。

在`pattern_name`不存在的时候，`RedirectView`现在会抛`NoReverseMatch`异常了。