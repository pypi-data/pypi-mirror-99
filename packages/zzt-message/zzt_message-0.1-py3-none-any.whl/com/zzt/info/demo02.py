# print('1024 * 768 =', 1024*768)
# coding:UTF-8
# keyword是一个模块的名称,这个名称需要符合标识符定义的要求
import keyword

# 实现了所以关键字的列出
"""
num = 10
# print(num, id(num))
# num = 30
del num
print(num, id(num))
"""
"""result = input('请输入bool型的参数: ')
print('输入的参数: ', result, type(0))

if result:
    print('你好,沐言科技')
"""
"""score = 10.0
if 90<=score<=100:
    print("优等生")
elif 60<=score<90:
    print("良等生")
else:
    print("差等生")
"""

'''num_a = 0
num_b = 1
while num_b<=1000:
    print(num_b, end='、')
    num_a, num_b = num_b, num_a + num_b
'''
# 元组和list互相转化
'''number = ('你好', '哈哈', '休息')
infos = [1, 2, 3, 4]
test = tuple(infos)
print('[数据类型]列表: %s ' % list(number))
print('[元组的数据类型]: %s' % type(test))
'''

'''
def get_info():
    print('hello python')
    return '你好呀'


data = get_info()
print(data)
'''

'''
def echo(title, url):
    return '【带有参数的函数】,标题: {} ,地址: {}'.format(title, url)


print(echo(url='www.baidu.com', title='python'))
'''
'''
num = 100


def change_num():
    global num
    num = 30


change_num()
print('【全局变量】num=%s' % num)
'''

"""
def print_doc():
    '''
    测试__doc__全局变量的调用,无任何的方法体
    :return:
    '''
    pass
print(print_doc.__doc__)
"""
"""
def print_data(count):
    def out(data):
        nonlocal count
        count += 1
        return "【第{}次输出数据】: {}".format(count, data)
    return out
oa = print_data(0)
print(oa('哈哈哈哈'))
print()
print(eval('\n"-"*50\n'))
print()
import this
"""

"""
import sys
print('【执行平台信息】:%s'%(sys.platform))
print('【执行平台信息】:%s'%(sys.path))
"""
"""
import sys
print('【参数信息】:%s'%(sys.argv))
if len(sys.argv)==1:
    print('没有输入参数,无法正确执行,程序退出!!!')
    sys.exit(0)
else:
    print('正确输入参数,程序结束', end="")
    for item in sys.argv:
        print(item, end='、')
"""
from random import *
numbers = [item for item in range(1, 10)]
print('【原始数据】:%s' % numbers)
print('-' * 50)
filter_result = list(filter(lambda item: item % 2 == 0, numbers))
print('【filter过滤数据】: %s' % filter_result)
print('-' * 50)
map_result = list(map(lambda item: item * 2, filter_result))
print('【map处理数据】: %s' % map_result)
print('-' * 50)
from functools import reduce
reduce_result = reduce(lambda x, y: x + y, map_result)
print('【reduce处理数据】: %s' % reduce_result)


