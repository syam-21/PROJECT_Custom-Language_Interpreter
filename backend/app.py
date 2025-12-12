import sys
import os

# Add the parent directory of 'backend' to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, jsonify
from interpreter_logic import (
    email_parser, normal_text_analyzer, reverse_concatenate, 
    comment_detector, word_frequency_calculator,
    regex_matcher, calculator,
    operator_delimiter_recognizer, parser_action_printer, compiler_error_classifier,
    semantic_action_simulator,
    run_full_c_code,
    execute_single_command,
    flex_bison_arithmetic_calculator,
    process_command_language,
    boolean_expression_evaluator,
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/execute_cli_command', methods=['POST'])
def execute_cli_command():
    data = request.json
    command = data.get('command', '')
    variables = data.get('variables', {})
    result = execute_single_command(command, variables)
    return jsonify(result)

@app.route('/api/interpret', methods=['POST'])
def interpret():
    data = request.json
    selected_option = data.get('option', '')
    regex_pattern = data.get('pattern', '') # For regex matcher, if applicable

    result = "Invalid option selected."

    try:
        if selected_option == 'run_full_c_code':
            c_code = data.get('c_code', '')
            user_input_string = data.get('user_input_string', '')
            result = run_full_c_code(c_code, user_input_string) # Pass both arguments
        elif selected_option == 'regex_matcher':
            user_input = data.get('input', '') # Get 'input' for regex_matcher
            if not regex_pattern:
                result = "Please provide a regex pattern in the input for Regex Matcher."
            else:
                result = regex_matcher(user_input, regex_pattern)
        elif selected_option == 'email_parser':
            user_input = data.get('input', '')
            result = email_parser(user_input)
        elif selected_option == 'normal_text_analyzer':
            user_input = data.get('input', '')
            result = normal_text_analyzer(user_input)
        elif selected_option == 'reverse_concatenate':
            user_input = data.get('input', '')
            result = reverse_concatenate(user_input)
        elif selected_option == 'comment_detector':
            user_input = data.get('input', '')
            result = comment_detector(user_input)
        elif selected_option == 'word_frequency_calculator':
            user_input = data.get('input', '')
            result = word_frequency_calculator(user_input)
        elif selected_option == 'calculator':
            user_input = data.get('input', '')
            result = calculator(user_input)
        elif selected_option == 'flex_bison_arithmetic_calculator':
            user_input = data.get('input', '')
            result = flex_bison_arithmetic_calculator(user_input)
        elif selected_option == 'operator_delimiter_recognizer':
            user_input = data.get('input', '')
            result = operator_delimiter_recognizer(user_input)
        elif selected_option == 'parser_action_printer':
            user_input = data.get('input', '')
            result = parser_action_printer(user_input)
        elif selected_option == 'compiler_error_classifier':
            user_input = data.get('input', '')
            result = compiler_error_classifier(user_input)
        elif selected_option == 'semantic_action_simulator':
            user_input = data.get('input', '')
            result = semantic_action_simulator(user_input)
        elif selected_option == 'command_language_interpreter':
            user_input = data.get('input', '')
            result = process_command_language(user_input)
        elif selected_option == 'boolean_expression_evaluator':
            user_input = data.get('input', '')
            result = boolean_expression_evaluator(user_input)

        else:
            result = f"Unknown option: {selected_option}"
    except Exception as e:
        result = f"An error occurred: {str(e)}"

    return jsonify({"output": result})

if __name__ == '__main__':
    app.run(debug=True, port=5000)