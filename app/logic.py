import sys
import os
import re
def calculate_expression(expression: str):
    """Evaluates the expression..."""
    if expression.strip() == "":
        return ""
    if "÷" in expression:
        expression = expression.replace('÷',"/") 
    elif "x" in expression:
        expression = expression.replace("x","*")
    try:
        expr = expression.replace(" ", "")

        expr = re.sub(
            r'(\d+(\.\d+)?)([+-])(\d+(\.\d+)?)%',
            lambda m: f"{m.group(1)}{m.group(3)}({m.group(1)}*{m.group(4)}/100)",
            expr
        )

        expr = re.sub(
            r'(\d+(\.\d+)?)([*/])(\d+(\.\d+)?)%',
            lambda m: f"{m.group(1)}{m.group(3)}({m.group(4)}/100)",
            expr
        )

        expr = re.sub(
            r'(\d+(\.\d+)?)%',
            lambda m: f"({m.group(1)}/100)",
            expr
        )

        expr = re.sub(
            r'((?:\d+(?:\.\d+)?)|\))\s*\(',
            r'\1*(',
            expr
        )

        expr = re.sub(
            r'((?:\d+(?:\.\d+)?)|\))\s*\(',
            r'\1*(',
            expr
        )


        return str(eval(expr))

    except Exception as e:
        return "Error"



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)