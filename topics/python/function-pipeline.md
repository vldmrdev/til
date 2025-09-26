
The ```__or__``` method was added to support the X | Y syntax, as a replacement for typing. Union, and is also used to indicate that a variable or function can accept multiple different value types.
```python
import typing

# PEP 604 https://peps.python.org/pep-0604/

int | str == typing.Union[int, str]  # True
```

In this example, we create a Pipe class with an overloaded ```__or__``` method.  
```python
class Pipeline:

    def __init__(self, value):
        self.value = value

    def __or__(self, other):
        if callable(other):
            return self.__class__(other(self.value))
        else:
            raise ValueError("Right operand must be callable!")


def multiply_3(x):
    return x * 3


def add_2(x):
    return x + 2


changed_num = Pipeline(5) | multiply_3 | add_2  # 5 * 3 + 2
print(changed_num.value)  # 17
```