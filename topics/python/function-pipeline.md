
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

```Important note: in this case | isn't bitwise OR, it's just OR as Union in the context of a set for types. ```


UPD:

New PipeLIne version:


```python
from collections.abc import Callable, Iterable, Iterator
from typing import final, override

type Transform[I, O] = Callable[[I], O]

class Stream[T]:
    """Базовый поток, открытый для расширения."""
    
    def __init__(self, source: Iterable[T]) -> None:
        self._source: Iterator[T] = iter(source)

    def __or__[U](self, transform: Transform[T, U]) -> "Stream[U]":
        def generator() -> Iterator[U]:
            for item in self._source:
                yield transform(item)
        
        # ПРАВИЛЬНО: Используем type(self) для сохранения полиморфизма
        return type(self)(generator())

    def __iter__(self) -> Iterator[T]:
        return self._source


# --- Пример с наследованием ---

class LoggedStream[T](Stream[T]):
    """Дочерний поток, который логирует прохождение данных."""
    
    @override
    def __iter__(self) -> Iterator[T]:
        for item in self._source:
            print(f"[LOG] Emitting: {item}", flush=True)
            yield item


# Источник данных
data_source: Iterable[int] = range(1, 3)

# Создаем экземпляр ДОЧЕРНЕГО класса
stream: LoggedStream[int] = LoggedStream(data_source)

# Благодаря type(self), результат операции | будет LoggedStream, а не Stream!
# Если бы был return Stream(...), логирование в последующих шагах умерло бы.
new_stream: LoggedStream[str] = stream | (lambda x: x * 2) | (lambda x: f"Val: {x}")

# Проверяем тип (для уверенности)
assert isinstance(new_stream, LoggedStream)
```