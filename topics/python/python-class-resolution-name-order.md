Firstly I should remind what is LEGB: Local, Enclose, Global, Built-in. It's a mnemonic rule about
[Resoulution of names](https://docs.python.org/3/reference/executionmodel.html#resolution-of-names) in Python.
Also, recommend [this](https://realpython.com/python-scope-legb-rule/) article.

So, look at this default example:

```python
# Built-in Scope
from math import inf


# inf = 'global variable'

def outer():
    # inf = 'Enclose variable'
    def inner():
        # inf = 'Local variable'
        print(inf)

    inner()


outer()
```

I think it's clear, inner() search variable in this order: Local > Enclose > Global > Built-in.

But what will strange_inner() return in this example?

```python
x = 0
y = 0


def strange_func():
    x = 1
    y = 1

    class A:
        print(x, y)
        x = 2


strange_func()
```

So, `strange_func()` return `0 1` because:

1. Global scope: **x** = 0 and **y** = 0 are defined at the module level.
2. Inside strange_func(): new local variables **x** = 1 and **y** = 1 are created. These shadow the global ones within
   the function.
3. During compilation of the class A body, Python scans all assignments:
    * Because **x** = 2 appears anywhere in the class body, the name **x** is marked as local to the class.
    * The name **y** is never assigned in the class body, so it remains a free variable.
4. When executing print(x, y) inside the class:
    * #### For x:
    * Python first looks in the class’s local namespace (which is being built during execution).
    * At this point, **x** has not yet been assigned, so it is not present.
    * However, because **x** was statically marked as class-local, the enclosing function (strange_inner()) is skipped
      entirely.
    * The search continues directly in the global scope, where **x** = 0 is found.
    * #### For y:
    * Since **y** is not assigned in the class, it is treated as a free variable.
    * Python follows the normal LEGB rule: not in class locals → checks enclosing scopes → finds **y** = 1 in
      strange_func().

5. Result: print(x, y) outputs 0 1.