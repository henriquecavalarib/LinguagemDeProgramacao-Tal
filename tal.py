class Tal:
    def __init__(self):
        self.memory = {}

    def run(self, code_lines):
        i = 0
        lines = [line.strip() for line in code_lines if line.strip()]
        
        while i < len(lines):
            line = lines[i]
            
            # Comando var: var x = 10
            if line.startswith("var "):
                _, rest = line.split("var ", 1)
                var_name, expr = rest.split("=")
                self.memory[var_name.strip()] = eval(expr.strip(), {}, self.memory)
            
            # Comando set: set x = x + 1
            elif line.startswith("set "):
                _, rest = line.split("set ", 1)
                var_name, expr = rest.split("=")
                self.memory[var_name.strip()] = eval(expr.strip(), {}, self.memory)
            
            # Comando print: print x
            elif line.startswith("print "):
                var_name = line.split("print ", 1)[1].strip()
                val = eval(var_name, {}, self.memory)
                print(f"[SAÍDA]: {val}")
            
            # Estrutura while ... do ... end
            elif line.startswith("while "):
                cond_str = line[6:line.find(" do")].strip()
                loop_body = []
                j = i + 1
                
                
                while j < len(lines) and lines[j] != "end":
                    loop_body.append(lines[j])
                    j += 1
                
                
                while eval(cond_str, {}, self.memory):
                    self.run(loop_body)
                
                i = j  
                
            i += 1

if __name__ == "__main__":
    codigo = [
        "var contador = 1",
        "var soma = 0",
        "while contador <= 4 do",
        "set soma = soma + contador",
        "set contador = contador + 1",
        "end",
        "print soma"
    ]
    
    interpreter = Tal()
    interpreter.run(codigo)