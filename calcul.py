import math
import re



def tokeni(text):
    text = text.replace(" ", "")
    tokens = re.findall(r"\d+\.?\d*|\.\d+|cos|==|[-+*/()]", text)
    if "".join(tokens) != text:
        raise ValueError("недопустимый символ в выражении")
    return tokens



def compare():
    left = expr()
    while tokens and tokens[0] == "==":
        tokens.pop(0)
        right = expr()
        left = int(left == right)  # 1 - равно, 0 - не равно
    return left


def expr():
    left = term()
    while tokens and tokens[0] in ("+", "-"):
        op = tokens.pop(0)
        right = term()
        left = left + right if op == "+" else left - right
    return left


def term():
    left = factor()
    while tokens and tokens[0] in ("*", "/"):
        op = tokens.pop(0)
        right = factor()
        left = left * right if op == "*" else left / right
    return left


def factor():
    if tokens and tokens[0] == "-":  # унарный минус
        tokens.pop(0)
        return -factor()
    if tokens and tokens[0] == "+":  # унарный плюс
        tokens.pop(0)
        return factor()
    return prim()


def prim():
    if not tokens:
        raise ValueError("неожиданный конец выражения")
    tok = tokens.pop(0)
    if tok == "(":
        value = compare()
        if not tokens or tokens.pop(0) != ")":
            raise ValueError("нет закрывающей скобки")
        return value
    if tok == "cos":
        if not tokens or tokens.pop(0) != "(":
            raise ValueError("после cos нужна скобка")
        value = compare()
        if not tokens or tokens.pop(0) != ")":
            raise ValueError("нет закрывающей скобки")
        return math.cos(value)
    if re.fullmatch(r"\d+\.?\d*|\.\d+", tok):
        return float(tok) if "." in tok else int(tok)
    raise ValueError(f"неожиданный токен {tok}")


def calculate(text):
    global tokens
    tokens = tokeni(text)
    result = compare()
    if tokens:
        raise ValueError(f"лишний токен {tokens[0]}")
    return result


while True:
    line = input("Выражение: ")
    if line.strip() == "":
        break
    try:
        print(calculate(line))
    except ZeroDivisionError:
        print("Ошибка: деление на ноль")
    except ValueError as e:
        print("Ошибка:", e)
