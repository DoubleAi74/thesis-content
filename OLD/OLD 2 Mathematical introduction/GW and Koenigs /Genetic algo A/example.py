import numpy as np
import matplotlib.pyplot as plt
import re

expr = "(-0.07159072897618168 * (exp(exp((exp(x) - cos(abs(abs(cos((cos((abs((x * x)) / abs(ln(abs(x))))) / sqrt(abs((sin(x) - sin(-0.553527680316907)))))))))))))) + 0.6982138768902053"

def replace_abs(expr):
    while '|' in expr:
        expr = re.sub(r'\|([^|]+)\|', r'abs(\1)', expr)
    return expr

# Preprocess expression
expr = expr.replace("ln", "log")
expr = replace_abs(expr)

safe_namespace = {
    "x": None,
    "sin": np.sin,
    "cos": np.cos,
    "exp": np.exp,
    "log": np.log,
    "sqrt": np.sqrt,
    "abs": np.abs,
    "pi": np.pi,
}

x = np.linspace(0.0001, 1, 20000)
safe_namespace["x"] = x

with np.errstate(all="ignore"):
    y = eval(expr, {"__builtins__": {}}, safe_namespace)

y = np.where(np.isfinite(y), y, np.nan)

plt.figure(figsize=(6, 6))
plt.plot(x, y)

plt.xlabel("x")
plt.ylabel("f(x)")
plt.grid(True)
plt.xlim(-0, 0.6)
plt.ylim(-0, 0.6)
plt.show()

