Imagine this - you’ve been living and coding for years, and suddenly realize you have no idea how to get a function’s total number of conditions using the AST! I found out for you, here’s an example — don’t thank me ))


```python
import ast
import inspect
from typing import Callable

def count_conditions_from_func(func: Callable) -> int:
    try:
        source = inspect.getsource(func)
    except (OSError, TypeError) as e:
        raise RuntimeError(f"Source code unavailable: {e}")

    tree = ast.parse(source)
    func_node = next(
        (n for n in ast.walk(tree) 
         if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == func.__name__),
        None
    )
    if func_node is None:
        raise ValueError("Function not found")

    conditions = []
    for node in ast.walk(func_node):
        if isinstance(node, (ast.If, ast.IfExp, ast.While, ast.Assert)):
            conditions.append(node.test)
        elif isinstance(node, ast.BoolOp):
            conditions.extend(node.values)
        elif isinstance(node, ast.comprehension):
            conditions.extend(node.ifs)
            
    return len(conditions)


```