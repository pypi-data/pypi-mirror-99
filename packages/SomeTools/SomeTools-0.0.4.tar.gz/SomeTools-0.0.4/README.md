SomeTools
========
.. image:: https://img.shields.io/pypi/v/SomeTools.svg
    :target: https://pypi.org/project/SomeTools/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/wheel/SomeTools.svg
    :target: https://pypi.org/project/SomeTools/
    
.. image:: https://img.shields.io/pypi/pyversions/SomeTools.svg
    :target: https://pypi.org/project/SomeTools/

.. image:: https://img.shields.io/pypi/l/SomeTools.svg
    :target: https://pypi.org/project/SomeTools/

整理一些常用工具便于日常使用。

<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">

Installation
------------

.. code-block:: shell

    pip install SomeTools -i https://pypi.python.org/simple

# 一、日期工具

主要功能(Features)
--------
可将输入的任何类型的日期字符串类型转化为datetime.datetime类型的日期对象

使用示例(Usage example)
-------------


<font color=#999AAA >代码如下（示例）：

```python
from common_tools import Common_tools


class Demo(Common_tools):
    def __init__(self, *args, **kwargs):
        super(Demo, self).__init__(*args, **kwargs)


if __name__ == '__main__':
    demo_ins = Demo()
    demo_ins.logger.info(f"{demo_ins.str_to_obj('2012-12-12 12:12:12')}{type(demo_ins.str_to_obj('2012-12-12 12:12:12'))}")


```

其他工具使用方法类似，继承父类使用即可。

<hr style=" border:solid; width:100px; height:1px;" color=#000000 size=1">

# 工具包还在成长中
以后会逐步丰富起来的
