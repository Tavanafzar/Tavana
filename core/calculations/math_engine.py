"""ارزیابی امن عبارات ریاضی."""

import ast
import math
import operator
import random
import re
from collections.abc import Callable
from typing import Any, Literal

ALLOWED_OPERATORS: dict[type, Callable] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def safe_factorial(value):
    """فاکتوریل با اعتبارسنجی ورودی (عدد منفی یا غیرصحیح رد می‌شود)."""
    if value < 0:
        raise ValueError("Factorial of negative number is not defined")
    if not isinstance(value, int):
        raise TypeError("Factorial requires integer")
    return math.factorial(value)


def safe_max(*args):
    """بیشینه را برمی‌گرداند؛ آرگومان تکی از نوع لیست/تاپل هم می‌پذیرد، مثل max([1, 2, 3])."""
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        return max(args[0])
    return max(args)


def safe_min(*args):
    """کمینه را برمی‌گرداند؛ آرگومان تکی از نوع لیست/تاپل هم می‌پذیرد، مثل min((1, 2, 3))."""
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        return min(args[0])
    return min(args)


ALLOWED_FUNCTIONS: dict[str, Callable] = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log10,
    "ln": math.log,
    "abs": abs,
    "round": round,
    "fact": safe_factorial,
    "random": random.randint,
    "max": safe_max,
    "min": safe_min,
}

_MATH_CHARS = "+-*/÷×x^√()!~"

_MULTIPLY_X_PATTERN = re.compile(r"(?<=\d)x(?=\d|\()")
_THOUSANDS_SEPARATOR_PATTERN = re.compile(r"(?<=\d),(?=\d{3}\b)")
_NEGATIVE_NUMBER_PATTERN = re.compile(r"(^|[+\-*/(])-(\d+(\.\d+)?)")
_FACTORIAL_PATTERN = re.compile(r"(-?\d+)!")
_SQRT_PATTERN = re.compile(r"√(-?\d+(\.\d+)?)")
_ROUND_PATTERN = re.compile(r"~(-?\d+(\.\d+)?)")


def is_math_expression(text: str) -> bool:
    """تشخیص می‌دهد آیا متن شبیه یک عبارت ریاضی است یا نه."""
    return any(ch in text for ch in _MATH_CHARS)


def _normalize_expression(text: str) -> str:
    """نویسه‌های نمایشی (×، ÷، √، !، ~، «3x4»، «1,000») را به نحو قابل‌فهم برای پایتون تبدیل می‌کند."""
    processed = text.strip()

    processed = processed.replace(
        "×", "*").replace("÷", "/").replace("^", "**")
    processed = _MULTIPLY_X_PATTERN.sub("*", processed)
    processed = _THOUSANDS_SEPARATOR_PATTERN.sub("", processed)

    processed = processed.replace("isGreaterThan", "max")
    processed = processed.replace("isLessThan", "min")

    processed = _NEGATIVE_NUMBER_PATTERN.sub(r"\1(-\2)", processed)

    processed = _FACTORIAL_PATTERN.sub(r"fact(\1)", processed)
    processed = _SQRT_PATTERN.sub(r"sqrt(\1)", processed)
    return _ROUND_PATTERN.sub(r"round(\1)", processed)


def _execute_node(node: ast.AST) -> Any:
    """یک گره AST را به‌صورت بازگشتی و فقط در چارچوب فهرست مجاز (سندباکس) ارزیابی می‌کند."""
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise TypeError("Only numbers are allowed")

    if isinstance(node, ast.List):
        return [_execute_node(item) for item in node.elts]

    if isinstance(node, ast.Tuple):
        return tuple(_execute_node(item) for item in node.elts)

    if isinstance(node, ast.BinOp):
        left = _execute_node(node.left)
        right = _execute_node(node.right)
        operation = ALLOWED_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Operator not allowed")
        return operation(left, right)

    if isinstance(node, ast.UnaryOp):
        value = _execute_node(node.operand)
        operation = ALLOWED_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Unary operator not allowed")
        return operation(value)

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise TypeError("Invalid function")

        function_name = node.func.id
        if function_name not in ALLOWED_FUNCTIONS:
            raise ValueError(f"Function '{function_name}' is not allowed")

        args = [_execute_node(arg) for arg in node.args]

        if (
            function_name in ("max", "min")
            and len(args) == 1
            and isinstance(args[0], (list, tuple))
        ):
            return ALLOWED_FUNCTIONS[function_name](args[0])

        return ALLOWED_FUNCTIONS[function_name](*args)

    raise TypeError("Invalid mathematical structure")


def evaluate_math_expression(text: str) -> Any:
    """عبارت را با سندباکس AST مجاز ارزیابی می‌کند؛ در صورت خطا رشته‌ی «Error: ...» برمی‌گرداند."""
    try:
        processed = _normalize_expression(text)
        tree = ast.parse(processed, mode="eval")
        result = _execute_node(tree.body)

        if isinstance(result, float):
            if result.is_integer():
                return int(result)
            return round(result, 10)

        return result

    except Exception as e:
        return f"Error: {e!s}"


def find_extreme_expression(
    expressions: list[str],
    mode: Literal["max", "min"] = "max",
) -> dict[str, Any]:
    """چند عبارت را ارزیابی می‌کند و عبارتی با بیشترین/کمترین مقدار را برمی‌گرداند."""
    valid_results = [
        {"expression": expr, "value": result}
        for expr in expressions
        for result in [evaluate_math_expression(expr)]
        if isinstance(result, (int, float)) and not isinstance(result, bool)
    ]

    if not valid_results:
        return {"error": "No valid mathematical expressions found."}

    if mode == "max":
        item = max(valid_results, key=lambda x: x["value"])
    elif mode == "min":
        item = min(valid_results, key=lambda x: x["value"])
    else:
        raise ValueError("Mode must be max or min")

    return {
        "mode": mode,
        "original_expression": item["expression"],
        "calculated_value": item["value"],
    }
