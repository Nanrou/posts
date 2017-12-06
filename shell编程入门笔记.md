# Shell编程入门笔记

## Hello World

```shell
#!/bin/bash
echo "Hello World!"
```

## 变量

###定义变量

直接`var=value`，中间是不能有空格的，这一点要注意。命名规则与常见的类似。

可以直接通过语句来得到值，如

```shell
for file in 'ls /etc'
```

就可以遍历 /etc 下面的文件

### 使用变量

在定义过的变量前面加上`$`就可以了，推荐在变量名外加花括号。

```shell
my_name='nanrou'
echo ${my_name}
```

### 变量操作

用`readonly`对变量进行操作，使其变成只读变量。

用`unset`来删除变量。

```Shell
readonly my_name
unset my_name
```

## 字符串

可以用单双引号来表示

单引号的限制：

* 单引号中全部原样输出，也就是不接受变量
* 也不接受`\`的转义，所以单引号的内容是不会有单引号这个符号出现的

双引号可以做到单引号做不到的事情，所以说养成好习惯，全用双引号好了。

### 字符串操作

拼接，可以直接引用变量。

获取长度，在变量名字前加`#`。

切片，`${var:start:length}`，从start截取length长度的字符。

```shell
say="hi ${my_name}"
echo ${say}  # 输出 hi nanrou
echo ${#say}  # 输出 9
echo ${say:0:2}  # 输出 hi
```

具体还有很多操作，需要的时候再看。

## 数组

支持一维数组，定义方法为`array=(val0 val1 val2 val3)`，注意是用空格或者回车分开。

取值时也与普通变量类似，`var=${array[0]}`。

用`@`号可以获取数组中所有元素，`echo ${array[@]}`。

获取长度的方法与字符串的一样，也是前面加`#`。

## 接收命令行参数

`$n`，n是数字，0代表这个脚本的名字，1代表第一个参数，2代表第二个，如此类推。

`$#`，表示参数的个数。

`$*`，用字符来表示所有参数。

`$$`，脚本当前进程ID。

`$!`，后台运行的最后一个进程ID。

`$@`，也是表示所有参数，但是是分开表示的。

`$?`，最后命令的退出状态。

## 运算符

通过`expr`这个表达式计算工具来进行运算，感觉就是像python的`exec`，不过需要注意的是，运算语句是用反引号`包起来的，而且表达式与运算符之间要有空格。

常见运算符都支持，包括算术运算符（加减乘除，余，相等不等，具体表现是`+ - * / % = == !=`），关系运算符（仅支持数字，或者只包含数字的字符串，大于小于，等于不等，具体表现是`-eq -ne -gt -lt -ge -le`），布尔运算符（与或非，具体表现是`-a -o !`），逻辑运算符（AND和OR， 具体表现为`&& ||`），字符串运算符（相等不等，长度是否为0或者空，具体表现为`= != -z -n str`），文件测试运算符（用于检测unix文件的各种属性，感觉用得到的就是`-r/w/x file`来判断文件是否可读/可写/可执行，和`-s/-e file`判断文件是否为空/是否存在。

## 常见命令

`echo`：常用的输出命令，用`-e`选项开启转义功能，也就是输出`\n`会变成换行，然后是可以用反引号去执行`expr`语句。

`prinft`：类似C中的输出命令，其侧重点在于格式化输出内容。

`test`：用test结合上面的一些运算符来作为判断语句。

## 流程控制

先要注意的是，流程控制不可以为空，要么就不写。

###条件控制

```shell
if condition
then
	command1
	command2
elif condition2
then
	command3
else
	command4
fi
```

注意condition这个条件语句，要么用test的语句，要么是`[]`包起来的。

### 循环控制

```shell
for var in item1 item2 ...
do
	command1
	command2
done
```

注意列表是可选的，意味着，如果不用列表，则是直接使用命令行的位置参数。

```shell
while condition
do
	command
done
```

```shell
until condition
do
	command
done
```

讲真，我真是第一次见这个语法。注意，这种循环至少会运行一次。

然后`break`和`continue`的用法与常见的一致。

## 选择控制

```shell
case 值 in
模式1)
	command1
	;;
模式2)
	command2
	;;
*)
	command3
	;;
esac
```

这种语法很好理解，匹配模式，模式以右括号结束，命令会一直执行到`;;`，没有匹配的话就用`*`号去捕捉其他状况。如果模式的右边是两个右括号，则代表`break`。

## 函数

函数定义格式

```shell
[ function ] funname [()]

{
  action;
  
  [return int;]
}
```

返回值，可以用显式用return 返回，如果不的话，则会以最后一条命令运行运算结果作为返回值，return后跟数值0-255

## 输入/输出重定向

单个的`<`或者`>`或者`>>`都很好理解。

`comand1 < infile > outfile`，同时替换输入和输出，执行command1，从infile读取内容，然后将输出写入到outfile。

我们知道文件描述符0，1，2分别代表标准输入，标准输出和标准错误，那么在重定向的时候，可以显示指定，如`command 2 > file`，就是将stderr重定向到file；`command > file 2>&1`就是将stdout和stderr合并后重定向到file。

### Here Document

一种特殊的重定向，将输入重定向到一个交互式shell脚本或程序。

类似在命令行中：

```shell
$ wc -l << EOF
	i 
	am
	nanrou
EOF
3
$
```

就是会将两个EOF之间的内容做为输入传给函数。当然在脚本中也可以这么写。

### /dev/null

不想要输出结果的时候，可以直接重定向到这个文件这里，就起到了禁止输出的效果了。

## 引用外部脚本

```shell
. filename
OR
source filename
```

这就等于import了，然后就可以直接调用那个文件里变量或者函数了。

这种情况下，被导入的那个文件是不要求要求可执行权限的。