Flask Language Interpreter Documentation
Table of Contents
Overview
Architecture
Language Grammar
API Endpoints
Language Features
Installation & Setup
Usage Examples
Error Handling
Configuration
Development
Troubleshooting
Overview
This Flask application implements a custom programming language interpreter built using the Lark parsing library. The interpreter supports basic arithmetic operations, variable assignment, control flow statements, and comparison operations through a RESTful API interface.

Key Features
Custom Language Parser: Built with Lark using LALR parsing
RESTful API: Execute code via HTTP requests
Real-time Execution: Immediate code execution and output
Variable Management: Persistent variable storage during session
Error Handling: Comprehensive syntax and runtime error reporting
Control Flow: Support for if statements and while loops
Web Interface Ready: CORS-enabled for frontend integration
Architecture
Core Components
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Flask App     │────│   Lark Parser   │────│  ExecuteTree    │
│   (REST API)    │    │   (Grammar)     │    │  (Transformer)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   HTTP Routes   │    │   AST Parser    │    │   Execution     │
│   (/execute)    │    │   (Syntax)      │    │   Environment   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
File Structure
project/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Frontend interface (optional)
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
Language Grammar
The interpreter uses a context-free grammar defined in Extended Backus-Naur Form (EBNF):

Grammar Rules
ebnf
start: statement+

statement: "print" ESCAPED_STRING       -> print_stmt
         | "print" expr                 -> print_expr
         | "if" expr "then" statement+  -> if_stmt
         | "while" expr "do" statement+ -> while_stmt
         | "add" expr expr              -> add_stmt
         | "sub" expr expr              -> sub_stmt
         | "mul" expr expr              -> mul_stmt
         | "div" expr expr              -> div_stmt
         | "mod" expr expr              -> mod_stmt
         | "pow" expr expr              -> pow_stmt
         | NAME "=" expr                -> assign_stmt
         | "clear"                      -> clear_stmt

?expr: comparison

?comparison: arithmetic "==" arithmetic -> eq
           | arithmetic "!=" arithmetic -> ne
           | arithmetic "<" arithmetic  -> lt
           | arithmetic ">" arithmetic  -> gt
           | arithmetic "<=" arithmetic -> le
           | arithmetic ">=" arithmetic -> ge
           | arithmetic

?arithmetic: arithmetic "+" term -> add
           | arithmetic "-" term -> sub
           | term

?term: term "*" factor -> mul
     | term "/" factor -> div
     | term "%" factor -> mod
     | factor

?factor: "(" expr ")"
       | NUMBER          -> number
       | NAME           -> var
       | BOOLEAN        -> boolean

BOOLEAN: "true" | "false"
Operator Precedence (Highest to Lowest)
Parentheses: ()
Multiplication, Division, Modulo: *, /, %
Addition, Subtraction: +, -
Comparison: ==, !=, <, >, <=, >=
API Endpoints
POST /execute
Execute code in the custom language.

Request Body:

json
{
  "code": "x = 5\nprint x\nadd x 10"
}
Response (Success):

json
{
  "output": "x = 5\n5\n15",
  "error": ""
}
Response (Error):

json
{
  "output": "",
  "error": "Runtime error on line 2: Variable 'y' is not defined"
}
POST /reset
Clear the execution environment and reset all variables.

Response:

json
{
  "message": "Environment reset successfully"
}
GET /variables
Get current variables in the execution environment.

Response:

json
{
  "variables": {
    "x": 5,
    "y": 10,
    "result": true
  }
}
GET /health
Health check endpoint for monitoring.

Response:

json
{
  "status": "healthy",
  "parser": "ready"
}
GET /
Serve the main HTML interface (if templates are provided).

Language Features
1. Variable Assignment
x = 42
name = "Hello World"
result = true
2. Print Statements
print "Hello, World!"    # Print string literal
print x                  # Print variable value
print x + y             # Print expression result
3. Arithmetic Operations
Prefix Notation (Commands)
add 5 3        # Output: 8
sub 10 4       # Output: 6
mul 3 7        # Output: 21
div 15 3       # Output: 5.0
mod 10 3       # Output: 1
pow 2 8        # Output: 256
Infix Notation (Expressions)
result = 5 + 3 * 2      # Output: 11 (follows precedence)
result = (5 + 3) * 2    # Output: 16 (parentheses override)
4. Comparison Operations
x = 5
y = 10
print x == y    # Output: false
print x < y     # Output: true
print x != y    # Output: true
5. Boolean Values
flag = true
done = false
print flag      # Output: true
6. Control Flow
If Statements
x = 5
if x > 0 then print "Positive number"
if x == 5 then print "x equals five"
While Loops
counter = 0
while counter < 3 do counter = counter + 1
while counter < 3 do print counter
Note: While loops have a built-in iteration limit (1000) to prevent infinite loops.

7. Environment Management
clear    # Clear all variables and reset environment
Installation & Setup
Prerequisites
Python 3.8 or higher
pip (Python package manager)
Dependencies
bash
pip install flask flask-cors lark
Quick Start
Clone or download the project files
Install dependencies:
bash
pip install -r requirements.txt
Run the application:
bash
python app.py
Access the API:
Server runs on http://localhost:5000
API endpoints available at /execute, /reset, etc.
Environment Variables
bash
export PORT=5000              # Server port (default: 5000)
export FLASK_ENV=development  # Enable debug mode
Usage Examples
Example 1: Basic Arithmetic
python
import requests

code = """
x = 10
y = 5
add x y
mul x y
div x y
"""

response = requests.post('http://localhost:5000/execute', 
                        json={'code': code})
print(response.json())
# Output: {"output": "x = 10\ny = 5\n15\n50\n2.0", "error": ""}
Example 2: Control Flow
python
code = """
counter = 1
while counter <= 3 do print counter
while counter <= 3 do counter = counter + 1
"""

response = requests.post('http://localhost:5000/execute', 
                        json={'code': code})
Example 3: Comparisons and Conditionals
python
code = """
age = 18
if age >= 18 then print "Adult"
if age < 21 then print "Cannot drink"
print age == 18
"""

response = requests.post('http://localhost:5000/execute', 
                        json={'code': code})
Error Handling
The interpreter provides detailed error reporting with line numbers and error types:

Syntax Errors
json
{
  "output": "",
  "error": "Syntax error on line 2: Unexpected token 'INVALID'"
}
Runtime Errors
json
{
  "output": "",
  "error": "Runtime error on line 3: Variable 'undefined_var' is not defined"
}
Division by Zero
json
{
  "output": "",
  "error": "Runtime error on line 1: Division by zero"
}
Infinite Loop Protection
json
{
  "output": "",
  "error": "Runtime error on line 2: Maximum iteration limit reached (possible infinite loop)"
}
Configuration
Application Settings
python
# app.py configuration options
MAX_ITERATIONS = 1000        # Maximum while loop iterations
DEBUG_MODE = False           # Enable/disable debug mode
CORS_ENABLED = True          # Enable CORS for frontend integration
Logging Configuration
python
import logging
logging.basicConfig(level=logging.INFO)
Production Deployment
python
# For production deployment
if __name__ != '__main__':
    # Disable debug mode in production
    app.debug = False
Development
Adding New Language Features
Extend the Grammar:
python
# Add new statement type to grammar
statement: ... | "for" NAME "in" expr "do" statement+ -> for_stmt
Implement Transformer Method:
python
def for_stmt(self, items):
    var_name = str(items[0])
    iterable = items[1]
    statements = items[2:]
    # Implementation logic
    return result
Add Error Handling:
python
try:
    # Execute new feature
    pass
except Exception as e:
    raise ExecutionError(f"Error in for loop: {e}")
Testing
Unit Testing Example
python
import unittest
from app import ExecuteTree, parser

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.transformer = ExecuteTree()
    
    def test_arithmetic(self):
        code = "add 5 3"
        parsed = parser.parse(code)
        result = self.transformer.transform(parsed)
        self.assertEqual(result, "8")
API Testing Example
python
def test_execute_endpoint():
    response = client.post('/execute', 
                          json={'code': 'print "test"'})
    assert response.status_code == 200
    assert response.json()['output'] == 'test'
Code Style Guidelines
Follow PEP 8 Python style guide
Use type hints for better code documentation
Add docstrings for all functions and classes
Handle exceptions gracefully with meaningful error messages
Troubleshooting
Common Issues
1. Parser Creation Fails
Problem: Reduce/Reduce collision errors Solution: Check grammar for ambiguous rules, ensure proper precedence

2. Variables Not Persisting
Problem: Variables reset between requests Solution: Ensure global transformer instance is used (consider sessions for multi-user)

3. CORS Errors in Frontend
Problem: Browser blocks requests due to CORS policy Solution: Verify flask_cors is properly configured

4. Import Errors
Problem: Missing required packages Solution: Install all dependencies: pip install flask flask-cors lark

5. Port Already in Use
Problem: Cannot bind to port 5000 Solution: Change port using environment variable: export PORT=8080

Debug Mode
Enable detailed error reporting:

bash
export FLASK_ENV=development
python app.py
Performance Optimization
Use sessions for multi-user environments
Implement caching for frequently parsed code
Add request rate limiting for production use
Consider using Redis for variable storage in distributed setups
Security Considerations
Validate and sanitize all input
Implement authentication for production use
Add rate limiting to prevent abuse
Set resource limits (memory, CPU time) for code execution
Consider sandboxing for untrusted code execution
API Client Examples
Python Client
python
import requests

class InterpreterClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
    
    def execute(self, code):
        response = requests.post(f"{self.base_url}/execute", 
                               json={"code": code})
        return response.json()
    
    def reset(self):
        response = requests.post(f"{self.base_url}/reset")
        return response.json()
    
    def get_variables(self):
        response = requests.get(f"{self.base_url}/variables")
        return response.json()

# Usage
client = InterpreterClient()
result = client.execute("x = 42\nprint x")
print(result['output'])  # Output: x = 42\n42
JavaScript Client
javascript
class InterpreterClient {
    constructor(baseUrl = 'http://localhost:5000') {
        this.baseUrl = baseUrl;
    }
    
    async execute(code) {
        const response = await fetch(`${this.baseUrl}/execute`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({code})
        });
        return await response.json();
    }
    
    async reset() {
        const response = await fetch(`${this.baseUrl}/reset`, {
            method: 'POST'
        });
        return await response.json();
    }
    
    async getVariables() {
        const response = await fetch(`${this.baseUrl}/variables`);
        return await response.json();
    }
}

// Usage
const client = new InterpreterClient();
client.execute('x = 42\nprint x').then(result => {
    console.log(result.output); // Output: x = 42\n42
});
This documentation provides a complete reference for the Flask Language Interpreter. For additional support or feature requests, please refer to the project repository or contact the development team.

