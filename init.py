def tokenize(codigo_fonte: str) -> list[str]:

    #Adicionando espaços entre os parenteses para facilitar a separação dos tokens
    codigo_formatacao  = codigo_fonte.replace('(', ' ( ').replace(')', ' ) ')

    return codigo_formatacao.split()

def parse(tokens: list[str]):
    if not tokens:
        raise SyntaxError("Erro Sintatico: código finalizado de forma inesperada")
    
    tokens = tokens.pop(0)
    
    if tokens == '(':
        sub_tree = []
        while tokens[0] != ')':
            sub_tree.append(parse(tokens))
        tokens.pop(0)
        return sub_tree
    elif tokens == ')':
        raise SyntaxError("Erro sintatico: ')' inesperado.")
    else:
        return atomize(token)

def atomize(tokens: str):

    try:
        return int(tokens)
    except ValueError:
        try:
            return float(tokens)
        except ValueError:
            return str(tokens)
