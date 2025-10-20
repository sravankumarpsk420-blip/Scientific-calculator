# cli_calculator.py
import math
import re

SAFE = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
SAFE.update({"pi": math.pi, "e": math.e, "pow": pow, "abs": abs})

def validate_expression(expr):
    # Check for invalid characters
    allowed = r'^[0-9+\-*/().^, \t\nabcdefghijklmnopqrstuvwxyzπ]+$'
    if not re.match(allowed, expr.lower()):
        return False
    return True

def evaluate(expr):
    if not expr.strip():
        return "Error: Empty expression"
    
    if not validate_expression(expr):
        return "Error: Invalid characters in expression"
        
    expr = expr.replace("^", "**")
    expr = expr.replace("π", "pi")
    
    try:
        result = eval(expr, {"__builtins__": None}, SAFE)
        if isinstance(result, complex):
            return f"Error: Complex result"
        return result
    except ZeroDivisionError:
        return "Error: Division by zero"
    except (SyntaxError, NameError):
        return "Error: Invalid expression"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("CLI Scientific Calculator (type 'quit' to exit)")
    print("Available functions:", ", ".join(sorted(SAFE.keys())))
    
    while True:
        try:
            expr = input(">>> ")
            if expr.lower() in ("quit", "exit"):
                break
            result = evaluate(expr)
            print(result)
        except KeyboardInterrupt:
            print("\nCalculator terminated by user")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()

