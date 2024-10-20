from flask import *
from backend.engine import create_rule,combine_rules,create_rule_ast, evaluate_rule,ast_to_rule_string, modify_operator  # Import the rule engine functions
from flask_cors import CORS
import traceback

app = Flask(__name__,static_folder="assets")
CORS(app,origins="*")



@app.route('/', methods=['GET'])
def main_index():
    return render_template("index.html")


@app.route('/create_rule', methods=['POST',"OPTIONS"])
def create_rule_api():
    try:
        rule_string = request.json['rule_string']
        print(rule_string,"rule_string")
        ast = create_rule(rule_string)
        return json.loads(ast), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400
    
    

@app.route('/combine-rules', methods=['POST',"OPTIONS"])
def combine_rules_api():
    try:
        rules = request.json['rules']
        print(rules,"rule_string")
        ast = combine_rules(rules)
        
        print(ast,"astast")
        return json.loads(ast), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_api():
    try:
        userJson = request.json['userJson']
        userRule = request.json['userRule']
        
        print()
        result = evaluate_rule(userRule, userJson)
        
        mgg=""
        if result:
            mgg="User  is eligible based on the rule."
        else:
            mgg="User  is not eligible based on the rule."
            
            
        
        
        
        
        return jsonify({"status": "success", "ast": mgg}), 200
        
        
    except Exception as e:
        print(traceback.print_exc(e))
        return jsonify({"error": str(e)}), 400

@app.route('/modify_operator', methods=['POST'])
def modify_operator_api():
    try:
        rule_string = request.json['rule_string']
        new_operator = request.json['new_operator']
        ast = create_rule(rule_string)
        modify_operator(ast, new_operator)
        return jsonify({"status": "success", "ast": str(ast)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
