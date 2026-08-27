import math

def tokenize(source_code: str) -> list[str]:
    formatted_code = source_code.replace('(', ' ( ').replace(')', ' ) ')
    return formatted_code.split()

def parse(tokens: list[str]):
    if not tokens:
        raise SyntaxError("Erro Sintático: código finalizado inesperadamente.")

    token = tokens.pop(0)

    if token == '(':
        sub_tree = []
        while tokens and tokens[0] != ')':
            sub_tree.append(parse(tokens))
        
        if not tokens:
            raise SyntaxError("Erro Sintático: esperava ')' mas o código acabou.")
            
        tokens.pop(0)
        return sub_tree
    elif token == ')':
        raise SyntaxError("Erro Sintático: ')' inesperado.")
    else:
        return atomize(token)

def atomize(token: str):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return str(token)

class Environment:
    def __init__(self, bindings=None, outer=None):
        self.bindings = bindings or {}
        self.outer = outer

    def find(self, var_name: str):
        if var_name in self.bindings:
            return self.bindings[var_name]
        elif self.outer is not None:
            return self.outer.find(var_name)
        raise NameError(f"Erro de Execução: símbolo '{var_name}' não encontrado.")

    def set(self, var_name: str, value):
        self.bindings[var_name] = value
        return value

def create_global_env() -> Environment:
    env = Environment()
    env.set('+', lambda a, b: a + b)
    env.set('-', lambda a, b: a - b)
    env.set('*', lambda a, b: a * b)
    env.set('/', lambda a, b: a / b)
    env.set('>', lambda a, b: a > b)
    env.set('<', lambda a, b: a < b)
    env.set('==', lambda a, b: a == b)
    env.set('pi', math.pi)
    return env

def evaluate(x, env: Environment):
    if isinstance(x, str):
        return env.find(x)
    elif not isinstance(x, list):
        return x

    if not x:
        return None

    op = x[0]

    if op == 'define':
        _, symbol, exp = x
        value = evaluate(exp, env)
        return env.set(symbol, value)

    elif op == 'if':
        _, test, conseq, alt = x
        cond_result = evaluate(test, env)
        exp_to_eval = conseq if cond_result else alt
        return evaluate(exp_to_eval, env)

    elif op == 'lambda':
        _, params, body = x
        return lambda *args: evaluate(body, Environment(bindings=dict(zip(params, args)), outer=env))

    else:
        proc = evaluate(x[0], env)
        args = [evaluate(arg, env) for arg in x[1:]]
        return proc(*args)

def run(code: str, env: Environment = None):
    if env is None:
        env = global_env
        
    tokens = tokenize(code)
    results = []
    
    while tokens:
        ast = parse(tokens)
        results.append(evaluate(ast, env))
        
    return results[-1] if results else None

global_env = create_global_env()

run("(define raio 5)", global_env)

area = run("(* pi (* raio raio))", global_env)
print(f"Área do círculo: {area}")

run("(define dobro (lambda (x) (* x 2)))", global_env)

resultado = run("(dobro 21)", global_env)
print(f"Resultado do dobro: {resultado}")

teste_if = run("(if (> raio 3) 100 0)", global_env)
print(f"Resultado do condicional: {teste_if}")

multi_script = """
(define x 10)
(define y 20)
(+ x y)
"""
print(f"Resultado do script completo: {run(multi_script, global_env)}")