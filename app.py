from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from lark import Lark, Transformer
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# ------------------------------------
grammar = """
start: statement+

statement: "print" ESCAPED_STRING       -> print_stmt
         | "print" NAME                 -> print_var
         | "add" expr expr              -> add_stmt
         | "mul" expr expr              -> mul_stmt
         | "div" expr expr              -> div_stmt
         | "mod" expr expr              -> mod_stmt
         | NAME "=" expr                -> assign_stmt

expr: NUMBER                            -> number
    | NAME                              -> var

%import common.ESCAPED_STRING
%import common.NUMBER
%import common.CNAME -> NAME
%import common.WS
%ignore WS
"""

# ------------------------------------
class ExecuteTree(Transformer):
    def __init__(self):
        self.env = {}  

    def start(self, items):
        return items[-1] if items else ""

    def print_stmt(self, items):
        return items[0][1:-1]

    def print_var(self, items):
        var_name = str(items[0])
        return str(self.env.get(var_name, f"Undefined variable: {var_name}"))

    def assign_stmt(self, items):
        var_name = str(items[0])
        self.env[var_name] = items[1]
        return f"{var_name} = {items[1]}"

    def add_stmt(self, items):
        return str(items[0] + items[1])

    def mul_stmt(self, items):
        return str(items[0] * items[1])

    def div_stmt(self, items):
        if items[1] == 0:
            return "Cannot divide by zero"
        return str(items[0] / items[1])

    def mod_stmt(self, items):
        if items[1] == 0:
            return "Cannot modulo by zero"
        return str(items[0] % items[1])

    def number(self, items):
        return int(items[0]) 

    def var(self, items):
        var_name = str(items[0])
        if var_name not in self.env:
            raise ValueError(f"Variable '{var_name}' is not defined.")
        return self.env[var_name]

parser = Lark(grammar, parser="lalr")

# -----------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_code():
    try:
        code = request.json.get('code', '')
        results = []
        tree_transformer = ExecuteTree()

        for line in code.strip().split('\n'):
            if not line.strip():
                continue
            
            parsed = parser.parse(line)
            result = tree_transformer.transform(parsed)
            
            if result is not None:
                results.append(str(result))

        return jsonify({'output': "\n".join(results), 'error': ''})
    except Exception as e:
        return jsonify({'output': '', 'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)