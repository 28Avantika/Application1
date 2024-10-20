# class Node:
#     def __init__(self, type, left=None, right=None, value=None):
#         self.type = type    # "operator" or "operand"
#         self.left = left    # Left child node
#         self.right = right  # Right child node
#         self.value = value  # Operand value or operator symbol


# def create_rule(rule_string):
    
    
#     print("create_rule",rule_string,"rule_string")
#     """
#     Creates an AST from a rule string.
#     Example rule_string: "age > 18"
#     """
#     if ">" in rule_string:
#         print("18")
#         left, right = rule_string.split(">")
#         return Node(type="operator", value=">", 
#                     left=Node(type="operand", value=left.strip()), 
#                     right=Node(type="operand", value=right.strip()))
#     elif "<" in rule_string:
#         print("24")
#         left, right = rule_string.split("<")
#         return Node(type="operator", value="<", 
#                     left=Node(type="operand", value=left.strip()), 
#                     right=Node(type="operand", value=right.strip()))
#     elif "==" in rule_string:
#         print("30")
#         left, right = rule_string.split("==")
#         return Node(type="operator", value="==", 
#                     left=Node(type="operand", value=left.strip()), 
#                     right=Node(type="operand", value=right.strip()))
#     else:
#         raise ValueError(f"Unsupported rule format: {rule_string}")


# def evaluate_rule(ast_node, data):
#     """
#     Evaluates a rule AST against a data dictionary.
#     Example: {"age": 20}
#     """
#     if ast_node.type == "operand":
#         # If the operand is a variable like 'age', retrieve its value from data.
#         if isinstance(ast_node.value, str) and ast_node.value in data:
#             return data[ast_node.value]
#         # Otherwise return the value directly (for literals like '18')
#         return int(ast_node.value) if ast_node.value.isdigit() else None
#     elif ast_node.type == "operator":
#         left_val = evaluate_rule(ast_node.left, data)
#         right_val = evaluate_rule(ast_node.right, data)

#         if left_val is None or right_val is None:
#             raise ValueError(f"Invalid values for comparison: {left_val}, {right_val}")

#         if ast_node.value == ">":
#             return left_val > right_val
#         elif ast_node.value == "<":
#             return left_val < right_val
#         elif ast_node.value == "==":
#             return left_val == right_val
#         else:
#             raise ValueError(f"Unsupported operator: {ast_node.value}")


# def modify_operator(ast_node, new_operator):
#     """
#     Modifies the operator in an existing rule.
#     """
#     if ast_node.type == "operator":
#         ast_node.value = new_operator
#     else:
#         raise ValueError("Cannot modify operator for operand nodes.")

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





def create_rule(rule_string):
    
    ast = parse_expression(rule_string)

    # Convert the AST to 
    
    return ast.to_json()

def create_rule_ast(rule_string):
    
    ast = parse_expression(rule_string)

    # Convert the AST to 
    
    return ast


def ast_to_rule_string(node):
    """Converts an AST node back into a rule string."""
    
    print(node["type"],"nodenode")
    if node["type"] == 'operand':
        # Format the operand as a string
        operand_name, operator, operand_value = node["value"]
        # Handle string values with quotes
        if isinstance(operand_value, str):
            operand_value = f"'{operand_value}'"
        return f"{operand_name} {operator} {operand_value}"

    elif node["type"] == 'operator':
        # Recursively convert left and right subtrees to strings
        left_string = ast_to_rule_string(node["left"])
        right_string = ast_to_rule_string(node["right"])
        return f"({left_string} {node['value']} {right_string})"
    
    
    return ""  


def combine_rules(rules):
    if not rules:
        return None

    # Parse each rule into its corresponding AST
    asts = [parse_expression(rule) for rule in rules]

    # Start combining the ASTs using the OR operator
    combined_ast = asts[0]
    
    for ast in asts[1:]:
        # Create a new Node that combines the current combined AST with the next AST
        combined_ast = Node(type='operator', value='OR', left=combined_ast, right=ast)
        
    
    return combined_ast.to_json()
import json
def evaluate_rule(JSONdata, data):
    """
    Evaluates a combined rule represented as an Abstract Syntax Tree (AST) against a set of user data.

    Args:
        JSONdata (dict): JSON representation of the AST.
        data (dict): Dictionary containing user attributes.

    Returns:
        bool: True if the user meets the criteria specified in the rule, False otherwise.
    """

    def evaluate_node(node):
        # Evaluate operator nodes
        if node['type'] == 'operator':
            left_result = evaluate_node(node['left'])
            right_result = evaluate_node(node['right'])

            if node['value'] == 'AND':
                return left_result and right_result
            elif node['value'] == 'OR':
                return left_result or right_result

        # Evaluate operand nodes
        elif node['type'] == 'operand':
            attribute, operator, value = node['value']
            user_value = data.get(attribute)

            # Handle different operators
            
            print(user_value,operator)
            
            if(user_value==None):
                return False
            if operator == '>':
                return user_value > int(value)
            elif operator == '<':
                return user_value < int(value)
            elif operator == '=':
                return user_value == value.strip("'")  # Remove quotes for comparison
            elif operator == '!=':
                return user_value != value.strip("'")  # Remove quotes for comparison

        return False

    # Start evaluating from the root node
    return evaluate_node(JSONdata)

def modify_operator(ast_node, new_operator):
    """
    Modifies the operator in an existing rule.
    """
    if ast_node.type == "operator":
        ast_node.value = new_operator
    else:
        raise ValueError("Cannot modify operator for operand nodes.")


# Example usage
if __name__ == "__main__":
    # Example rule with nested AND/OR and parentheses
    rule_string = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
    data = {
        "age": 32,
        "department": "Sales",
        "salary": 60000,
        "experience": 3
    }

    # Parse the rule into an AST
    ast = create_rule(rule_string)
    print("AST:", ast)

    # Evaluate the rule with data
    result = evaluate_rule(ast, data)
    print("Evaluation Result:", result)

    # Modify the operator
    modify_operator(ast.left, "OR")  # Change the first AND to OR
    print("Modified AST:", ast)

    # Re-evaluate the rule with modified AST
    result = evaluate_rule(ast, data)
    print("Modified Evaluation Result:", result)
