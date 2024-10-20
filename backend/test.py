import json
import re

class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type    # Type of the node
        self.left = left    # Left child node
        self.right = right  # Right child node
        self.value = value  # Operand value or operator symbol

    def to_dict(self):
        """Converts the Node to a dictionary for JSON serialization."""
        node_dict = {
            "type": self.type,
            "value": self.value
        }
        
        if self.left:
            node_dict["left"] = self.left.to_dict()
        if self.right:
            node_dict["right"] = self.right.to_dict()
        return node_dict

    def to_json(self):
        """Converts the Node to a JSON string."""
        return json.dumps(self.to_dict(), indent=4)

def parse_expression(expression):
    # Remove whitespace for easier parsing
    expression = expression.replace(" ", "")
    
    # Define the regex patterns for operators and operands
    operand_pattern = r"([a-zA-Z_][a-zA-Z0-9_]*)\s*([<>]=?|=)\s*('.*?'|\d+)"
    operator_pattern = r"(AND|OR)"
    
    # Stack for operators and operands
    operator_stack = []
    operand_stack = []
    
    # Tokenize the expression based on operators and operands
    tokens = re.split(r'(\(|\)|AND|OR)', expression)
    tokens = [token for token in tokens if token]  # Remove empty tokens

    for token in tokens:
        if token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                right = operand_stack.pop()
                operator = operator_stack.pop()
                left = operand_stack.pop()
                operand_stack.append(Node(type='operator', value=operator, left=left, right=right))
            operator_stack.pop()  # pop the '('
        elif re.match(operator_pattern, token):
            operator_stack.append(token)
        elif re.match(operand_pattern, token):
            match = re.match(operand_pattern, token)
            if match:
                operand_name = match.group(1)
                operator = match.group(2)
                operand_value = match.group(3).strip("'")  # Remove quotes for string values
                operand_stack.append(Node(type='operand', value=(operand_name, operator, operand_value)))

    # Handle remaining operators
    while operator_stack:
        right = operand_stack.pop()
        operator = operator_stack.pop()
        left = operand_stack.pop()
        operand_stack.append(Node(type='operator', value=operator, left=left, right=right))

    return operand_stack[0]  # Return the root of the AST

# Example usage
rule_string = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
ast = parse_expression(rule_string)

# Convert the AST to JSON
print(ast.to_json())