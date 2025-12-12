import re
import os
import subprocess
import tempfile
import shutil
import time
from backend.flex_bison_utils import compile_flex_bison, run_flex_bison_program



_CALCULATOR_EXECUTABLE = None
_CALCULATOR_COMPILE_ERROR = None

_OPERATOR_DELIMITER_RECOGNIZER_EXECUTABLE = None
_OPERATOR_DELIMITER_RECOGNIZER_COMPILE_ERROR = None

_PARSER_ACTION_PRINTER_EXECUTABLE = None
_PARSER_ACTION_PRINTER_COMPILE_ERROR = None

_COMPILER_ERROR_CLASSIFIER_EXECUTABLE = None
_COMPILER_ERROR_CLASSIFIER_COMPILE_ERROR = None

_SEMANTIC_ACTION_SIMULATOR_EXECUTABLE = None
_SEMANTIC_ACTION_SIMULATOR_COMPILE_ERROR = None

_BOOLEAN_EVALUATOR_EXECUTABLE = None
_BOOLEAN_EVALUATOR_COMPILE_ERROR = None

_ARITHMETIC_CALCULATOR_EXECUTABLE = None
_ARITHMETIC_CALCULATOR_COMPILE_ERROR = None




# --- Helper function for string processing ---
def strip_comments(text):
    # Remove C-style block comments (/* ... */)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    # Remove C-style line comments (// ...)
    text = re.sub(r'//.*', '', text)
    return text



# --- Compile Functions for Flex/Bison Programs ---


def _compile_calculator():
    global _CALCULATOR_EXECUTABLE, _CALCULATOR_COMPILE_ERROR
    if _CALCULATOR_EXECUTABLE is None and _CALCULATOR_COMPILE_ERROR is None:
        flex_file = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'calculator', 'calculator.l')
        bison_file = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'calculator', 'calculator.y')
        output_dir = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'calculator')
        success, message = compile_flex_bison('calculator', flex_file, bison_file, output_dir)
        if success:
            _CALCULATOR_EXECUTABLE = message
            print(f"Calculator executable compiled at: {_CALCULATOR_EXECUTABLE}")
        else:
            _CALCULATOR_COMPILE_ERROR = f"Failed to compile Calculator: {message}"
            print(_CALCULATOR_COMPILE_ERROR)

def _compile_operator_delimiter_recognizer():
    global _OPERATOR_DELIMITER_RECOGNIZER_EXECUTABLE, _OPERATOR_DELIMITER_RECOGNIZER_COMPILE_ERROR
    if _OPERATOR_DELIMITER_RECOGNIZER_EXECUTABLE is None and _OPERATOR_DELIMITER_RECOGNIZER_COMPILE_ERROR is None:
        flex_file = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'lexer_features', 'lexer_features.l')
        bison_file = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'lexer_features', 'lexer_features.y')
        output_dir = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'lexer_features')
        success, message = compile_flex_bison('lexer_features', flex_file, bison_file, output_dir)
        if success:
            _OPERATOR_DELIMITER_RECOGNIZER_EXECUTABLE = message
            print(f"Operator & Delimiter Recognizer executable compiled at: {_OPERATOR_DELIMITER_RECOGNIZER_EXECUTABLE}")
        else:
            _OPERATOR_DELIMITER_RECOGNIZER_COMPILE_ERROR = f"Failed to compile Operator & Delimiter Recognizer: {message}"
            print(_OPERATOR_DELIMITER_RECOGNIZER_COMPILE_ERROR)

def _compile_parser_action_printer():
    global _PARSER_ACTION_PRINTER_EXECUTABLE, _PARSER_ACTION_PRINTER_COMPILE_ERROR
    if _PARSER_ACTION_PRINTER_EXECUTABLE is None and _PARSER_ACTION_PRINTER_COMPILE_ERROR is None:
        flex_file = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'variable_declarations', 'variable_declarations.l')
        bison_file = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'variable_declarations', 'variable_declarations.y')
        output_dir = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'variable_declarations')
        success, message = compile_flex_bison('variable_declarations', flex_file, bison_file, output_dir)
        if success:
            _PARSER_ACTION_PRINTER_EXECUTABLE = message
            print(f"Parser Action Printer executable compiled at: {_PARSER_ACTION_PRINTER_EXECUTABLE}")
        else:
            _PARSER_ACTION_PRINTER_COMPILE_ERROR = f"Failed to compile Parser Action Printer: {message}"
            print(_PARSER_ACTION_PRINTER_COMPILE_ERROR)

def _compile_compiler_error_classifier():
    global _COMPILER_ERROR_CLASSIFIER_EXECUTABLE, _COMPILER_ERROR_CLASSIFIER_COMPILE_ERROR
    if _COMPILER_ERROR_CLASSIFIER_EXECUTABLE is None and _COMPILER_ERROR_CLASSIFIER_COMPILE_ERROR is None:
        flex_file = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'error_simulator', 'error_simulator.l')
        bison_file = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'error_simulator', 'error_simulator.y')
        output_dir = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'error_simulator')
        success, message = compile_flex_bison('error_simulator', flex_file, bison_file, output_dir)
        if success:
            _COMPILER_ERROR_CLASSIFIER_EXECUTABLE = message
            print(f"Compiler Error Classifier executable compiled at: {_COMPILER_ERROR_CLASSIFIER_EXECUTABLE}")
        else:
            _COMPILER_ERROR_CLASSIFIER_COMPILE_ERROR = f"Failed to compile Compiler Error Classifier: {message}"
            print(_COMPILER_ERROR_CLASSIFIER_COMPILE_ERROR)

def _compile_semantic_action_simulator():
    global _SEMANTIC_ACTION_SIMULATOR_EXECUTABLE, _SEMANTIC_ACTION_SIMULATOR_COMPILE_ERROR
    if _SEMANTIC_ACTION_SIMULATOR_EXECUTABLE is None and _SEMANTIC_ACTION_SIMULATOR_COMPILE_ERROR is None:
        flex_file = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'semantic_action_simulator', 'semantic_action_simulator.l')
        bison_file = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'semantic_action_simulator', 'semantic_action_simulator.y')
        output_dir = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'semantic_action_simulator')
        success, message = compile_flex_bison('semantic_action_simulator', flex_file, bison_file, output_dir)
        if success:
            _SEMANTIC_ACTION_SIMULATOR_EXECUTABLE = message
            print(f"Semantic Action Simulator executable compiled at: {_SEMANTIC_ACTION_SIMULATOR_EXECUTABLE}")
        else:
            _SEMANTIC_ACTION_SIMULATOR_COMPILE_ERROR = f"Failed to compile Semantic Action Simulator: {message}"
            print(_SEMANTIC_ACTION_SIMULATOR_COMPILE_ERROR)

def _compile_boolean_evaluator():
    global _BOOLEAN_EVALUATOR_EXECUTABLE, _BOOLEAN_EVALUATOR_COMPILE_ERROR
    if _BOOLEAN_EVALUATOR_EXECUTABLE is None and _BOOLEAN_EVALUATOR_COMPILE_ERROR is None:
        c_file = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'boolean_evaluator', 'boolean_evaluator.c')
        output_dir = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'boolean_evaluator')
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        executable_path = os.path.join(output_dir, "boolean_evaluator.exe" if os.name == 'nt' else "boolean_evaluator")
        
        compile_command = ["gcc", c_file, "-o", executable_path]
        
        try:
            subprocess.run(compile_command, check=True, capture_output=True, text=True, timeout=10)
            _BOOLEAN_EVALUATOR_EXECUTABLE = executable_path
            print(f"Boolean Evaluator C executable compiled at: {_BOOLEAN_EVALUATOR_EXECUTABLE}")
        except subprocess.CalledProcessError as e:
            _BOOLEAN_EVALUATOR_COMPILE_ERROR = f"Failed to compile Boolean Evaluator C code:\n{e.stderr}"
            print(_BOOLEAN_EVALUATOR_COMPILE_ERROR)
        except subprocess.TimeoutExpired:
            _BOOLEAN_EVALUATOR_COMPILE_ERROR = "Boolean Evaluator C code compilation timed out."
            print(_BOOLEAN_EVALUATOR_COMPILE_ERROR)
        except FileNotFoundError:
            _BOOLEAN_EVALUATOR_COMPILE_ERROR = "GCC compiler not found for Boolean Evaluator. Please install GCC."
            print(_BOOLEAN_EVALUATOR_COMPILE_ERROR)

# --- New compile function for arithmetic_calculator ---
def _compile_arithmetic_calculator():
    global _ARITHMETIC_CALCULATOR_EXECUTABLE, _ARITHMETIC_CALCULATOR_COMPILE_ERROR
    if _ARITHMETIC_CALCULATOR_EXECUTABLE is None and _ARITHMETIC_CALCULATOR_COMPILE_ERROR is None:
        flex_file = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'arithmetic_calculator', 'arithmetic_calculator.l')
        bison_file = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'arithmetic_calculator', 'arithmetic_calculator.y')
        output_dir = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'arithmetic_calculator')
        success, message = compile_flex_bison('arithmetic_calculator', flex_file, bison_file, output_dir)
        if success:
            _ARITHMETIC_CALCULATOR_EXECUTABLE = message
            print(f"Arithmetic Calculator executable compiled at: {_ARITHMETIC_CALCULATOR_EXECUTABLE}")
        else:
            _ARITHMETIC_CALCULATOR_COMPILE_ERROR = f"Failed to compile Arithmetic Calculator: {message}"
            print(_ARITHMETIC_CALCULATOR_COMPILE_ERROR)




# --- Python-based Functions ---
def email_parser(c_code):
    clean_code = strip_comments(c_code)

    # Extract all string literals from printf statements
    printf_strings_raw = re.findall(r'printf\s*\(\s*"(.*?)"', clean_code, re.DOTALL)
    
    # Join them into a single block of text for email extraction
    full_text_for_email_search = " ".join(printf_strings_raw)

    email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" # Relaxed start/end anchors
    academic_domain_regex = r"@(edu\.bd|ac\.bd|diu\.edu\.bd)$"
    personal_domain_regex = r"@(gmail\.com|yahoo\.com|outlook\.com)$"

    potential_emails = re.findall(email_regex, full_text_for_email_search)
    
    # Remove duplicates
    unique_emails = sorted(list(set(potential_emails)))

    if not unique_emails:
        return "No email addresses found in printf statements."
    
    results = []
    for email in unique_emails:
        status_category = "Unknown"
        is_university_mail = "No"

        # Rule 1: Valid format (already handled by regex, but ensure consistency)
        is_valid_format = bool(re.fullmatch(email_regex, email))
        
        if is_valid_format:
            if re.search(academic_domain_regex, email):
                status_category = "Valid (University)"
                is_university_mail = "Yes"
            elif re.search(personal_domain_regex, email):
                status_category = "Valid (Personal)"
            else:
                status_category = "Valid (Unknown)" # Catches valid emails not personal/university
        else:
            status_category = "Invalid" # If regex didn't match fully
            
        results.append(f"Email: {email} | Status: {status_category} | Is University Mail (.edu): {is_university_mail}")
    
    return "\n".join(results)

def normal_text_analyzer(c_code):
    import re
    from collections import Counter

    # Regex to find all string literals inside printf statements
    # It looks for `printf(...)` and captures the first string literal inside.
    # This is a simplified regex and might not handle all edge cases, but is good for this purpose.
    printf_strings = re.findall(r'printf\s*\(\s*"(.*?)"', c_code, re.DOTALL)

    if not printf_strings:
        return "No text inside printf statements found."

    # Join all found strings and clean them up
    # This removes C-style format specifiers like %d, %s, etc.
    full_text = " ".join(printf_strings)
    cleaned_text = re.sub(r'%[a-zA-Z%]', '', full_text)
    
    # Extract words using a regex that finds sequences of alphabetic characters
    words = re.findall(r'[a-zA-Z]+', cleaned_text.lower())

    if not words:
        return "No words found in printf statements for analysis."

    # 1. Total words
    total_words = len(words)

    # 2. Unique words
    unique_words_set = set(words)
    unique_words_count = len(unique_words_set)

    # 3. Longest word
    longest_word = max(words, key=len)

    # 4. Shortest word
    shortest_word = min(words, key=len)

    # 5. Most frequent word(s)
    word_counts = Counter(words)
    if not word_counts:
        most_frequent_words = ["N/A"]
    else:
        max_freq = word_counts.most_common(1)[0][1]
        most_frequent_words = [word for word, freq in word_counts.items() if freq == max_freq]

    # Format the output
    output = [
        f"- Total words: {total_words}",
        f"- Unique words: {unique_words_count}",
        f"- Longest word: '{longest_word}'",
        f"- Shortest word: '{shortest_word}'",
        f"- Most frequent word(s): {', '.join(most_frequent_words)}"
    ]

    return "\n".join(output)



# --- New global variables for var_extractor ---
_VAR_EXTRACTOR_EXECUTABLE = None
_VAR_EXTRACTOR_COMPILE_ERROR = None

# --- New compile function for var_extractor ---
def _compile_var_extractor():
    global _VAR_EXTRACTOR_EXECUTABLE, _VAR_EXTRACTOR_COMPILE_ERROR
    if _VAR_EXTRACTOR_EXECUTABLE is None and _VAR_EXTRACTOR_COMPILE_ERROR is None:
        flex_file = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'var_extractor', 'var_extractor.l')
        bison_file = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'var_extractor', 'var_extractor.y')
        output_dir = os.path.join(os.path.dirname(__file__), 'flex_bison_programs', 'var_extractor')
        
        # Use g++ by setting the compiler binary name
        # This assumes compile_flex_bison is modified or uses g++ by default for .y files with C++
        # Since we modified flex_bison_utils.py, this should work.
        success, message = compile_flex_bison('var_extractor', flex_file, bison_file, output_dir)

        if success:
            _VAR_EXTRACTOR_EXECUTABLE = message
            print(f"Variable Extractor executable compiled at: {_VAR_EXTRACTOR_EXECUTABLE}")
        else:
            _VAR_EXTRACTOR_COMPILE_ERROR = f"Failed to compile Variable Extractor: {message}"
            print(_VAR_EXTRACTOR_COMPILE_ERROR)


def reverse_concatenate(c_code):
    import json

    # Ensure the var_extractor is compiled
    _compile_var_extractor()
    if _VAR_EXTRACTOR_COMPILE_ERROR:
        return f"Error: {_VAR_EXTRACTOR_COMPILE_ERROR}"
    if not _VAR_EXTRACTOR_EXECUTABLE:
        return "Reverse & Concatenate Analyzer is not ready (compilation failed or not attempted)."

    # Run the extractor and get the JSON output
    stdout, stderr = run_flex_bison_program(_VAR_EXTRACTOR_EXECUTABLE, c_code)
    if stderr:
        return f"C Code Parser Error:\n{stderr}"
    
    try:
        data = json.loads(stdout)
        variables = data.get("variables", {})
        print_order = data.get("print_order", [])
    except json.JSONDecodeError:
        return f"Error: Failed to parse analysis data from C code parser.\nRaw output:\n{stdout}"

    if not print_order:
        return "No printf statements with recognized variables found."

    # --- Perform Analysis ---
    original_strings = [variables.get(var, f"<{var}?>") for var in print_order]
    original_output = "".join(original_strings)

    reversed_strings = [s[::-1] for s in original_strings]
    final_concatenated = "".join(reversed_strings)
    total_chars = len(final_concatenated)
    is_palindrome = "Yes" if final_concatenated == final_concatenated[::-1] else "No" 
    
    # --- Format Output ---
    output = [
        f"- Original printed output: {original_output}",
        f"- Reversed output (before concatenation): {', '.join(reversed_strings)}",
        f"- Final concatenated reversed string: {final_concatenated}",
        f"- Total characters: {total_chars}",
        f"- Is the final string a palindrome? {is_palindrome}"
    ]
    
    return "\n".join(output)


def comment_detector(c_code):
    single_line_comments = []
    multi_line_comments = []

    # Regex for multi-line comments (/* ... */)
    multiline_comment_pattern = re.compile(r'/\*.*?\*/', re.DOTALL)
    for match in multiline_comment_pattern.finditer(c_code):
        comment = match.group(0)
        # Remove internal newlines and replace with a single space
        cleaned_comment = comment.replace('\n', ' ')
        multi_line_comments.append(f"- {cleaned_comment}")

    # Regex for single-line comments (// ...)
    # This should be applied carefully to avoid matching // inside strings
    singleline_comment_pattern = re.compile(r'//.*')
    for match in singleline_comment_pattern.finditer(c_code):
        comment = match.group(0)
        single_line_comments.append(f"- {comment}")
            
    output_lines = []

    if single_line_comments:
        output_lines.append("Single-line Comments:")
        output_lines.extend(single_line_comments)
    
    if multi_line_comments:
        if single_line_comments: # Add a blank line for separation if both exist
            output_lines.append("") 
        output_lines.append("Multi-line Comments:")
        output_lines.extend(multi_line_comments)
            
    if not output_lines:
        return "No comments detected."
    
    return "\n".join(output_lines)

def word_frequency_calculator(c_code):
    from collections import Counter

    clean_code = strip_comments(c_code)
    
    # Extract all string literals from printf statements
    printf_strings = re.findall(r'printf\s*\(\s*"(.*?)"', clean_code, re.DOTALL)

    if not printf_strings:
        return "No text inside printf statements found to analyze."

    full_text = " ".join(printf_strings)
    
    # Extract words (sequences of letters only), case-insensitive
    words = re.findall(r'[a-zA-Z]+', full_text.lower())

    if not words:
        return "No words found for frequency calculation."

    word_counts = Counter(words)
    
    # Sort by frequency (desc), then by word (asc)
    sorted_words = sorted(word_counts.items(), key=lambda item: (-item[1], item[0]))
    
    output_lines = ["Frequency:"]
    for word, count in sorted_words:
        output_lines.append(f"- {word}: {count}")

    return "\n".join(output_lines)

def regex_matcher(text, pattern):
    try:
        matches = re.findall(pattern, text)
        if matches:
            return "Matches found:\n" + "\n".join(matches)
        else:
            return "No matches found."
    except re.error as e:
        return f"Regex Error: {e}"



def run_full_c_code(c_code, user_input_string):
    import subprocess
    import tempfile
    import shutil

    # Security Warning
    output_lines = [
        "SECURITY WARNING: Running arbitrary C code can be dangerous.",
        "This feature is for educational/testing purposes only. Do not run untrusted code.",
        "--------------------------------------------------------------------------------",
    ]

    temp_dir = None
    try:
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        
        # Write C code to a temporary file
        c_file_path = os.path.join(temp_dir, "user_code.c")
        with open(c_file_path, "w") as f:
            f.write(c_code)
        
        # Define output executable path
        executable_path = os.path.join(temp_dir, "user_code.exe" if os.name == 'nt' else "user_code")
        execute_command = [executable_path] # Moved here

        # Compile the C code
        compile_command = ["gcc", c_file_path, "-o", executable_path]
        output_lines.append(f"Compiling with: {' '.join(compile_command)}")
        compile_process = subprocess.run(compile_command, capture_output=True, text=True, timeout=10)
        
        if compile_process.returncode != 0:
            output_lines.append("\n--- COMPILATION FAILED ---")
            output_lines.append(compile_process.stderr)
            output_lines.append("--------------------------")
            return "\n".join(output_lines)
        else:
            output_lines.append("\n--- COMPILATION SUCCESSFUL ---")
            if compile_process.stderr:
                output_lines.append("Compiler Warnings/Info:")
                output_lines.append(compile_process.stderr)
                output_lines.append("--------------------------")

        # Execute the compiled program
        # The execute_command is already defined
        output_lines.append(f"\nExecuting: {' '.join(execute_command)}")
        try:
            execute_process = subprocess.run(execute_command, input=user_input_string, capture_output=True, text=True, timeout=5)
            output_lines.append("\n--- PROGRAM OUTPUT ---")
            output_lines.append(execute_process.stdout)
            if execute_process.stderr:
                output_lines.append("--- PROGRAM STDERR ---")
                output_lines.append(execute_process.stderr)
            output_lines.append(f"--- Program exited with code: {execute_process.returncode} ---")
        except subprocess.TimeoutExpired:
            output_lines.append("\n--- EXECUTION FAILED ---")
            output_lines.append("Error: Program timed out after 5 seconds.")
            output_lines.append("--------------------------")
        except Exception as e:
            output_lines.append("\n--- EXECUTION FAILED ---")
            output_lines.append(f"Error during execution: {e}")
            output_lines.append("--------------------------")

    except subprocess.TimeoutExpired:
        output_lines.append("\n--- COMPILATION FAILED ---")
        output_lines.append("Error: Compilation timed out after 10 seconds.")
        output_lines.append("--------------------------")
    except FileNotFoundError:
        output_lines.append("\n--- ERROR ---")
        output_lines.append("Error: GCC compiler not found. Please ensure GCC is installed and in your system's PATH.")
        output_lines.append("--------------------------")
    except Exception as e:
        output_lines.append("\n--- UNEXPECTED ERROR ---")
        output_lines.append(f"An unexpected error occurred: {e}")
        output_lines.append("--------------------------")
    finally:
        # Clean up temporary directory
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            output_lines.append(f"\nCleaned up temporary files in {temp_dir}")
        output_lines.append("--------------------------------------------------------------------------------")

    return "\n".join(output_lines)

# --- Flex/Bison Integrated Functions ---


def calculator(c_code):
    symbol_table = {}
    output_lines = []

    clean_code = strip_comments(c_code)
    
    # Regex to find variable assignments (int, float, double)
    # e.g., int x = 10; float y = x + 5;
    assignment_pattern = re.compile(r'(?:int|float|double)\s+([a-zA-Z_]\w*)\s*=\s*(.*?)\s*;')

    for match in assignment_pattern.finditer(clean_code):
        var_name = match.group(1)
        expression_str = match.group(2).strip()

        # Substitute known variables into the expression
        for key, value in symbol_table.items():
            expression_str = re.sub(r'\b' + re.escape(key) + r'\b', str(value), expression_str)
        
        try:
            # Basic validation to prevent arbitrary code execution with eval()
            # Only allow numbers, +, -, *, /, (, )
            if not re.fullmatch(r'[\d\s+\-*/().]+', expression_str):
                output_lines.append(f"Result for {var_name}: Error - Invalid characters in expression: {expression_str}")
                continue
            
            # Check for division by zero before evaluation
            if '/' in expression_str:
                parts = re.split(r'/', expression_str)
                for i in range(1, len(parts)):
                    # Check if the divisor part evaluates to zero
                    try:
                        divisor_candidate = parts[i].strip()
                        # Simplified check, might not catch all zero division cases in complex expressions
                        if re.fullmatch(r'[\d\s\.\-]+', divisor_candidate): # Only simple numbers/negatives
                            if float(divisor_candidate) == 0:
                                raise ZeroDivisionError
                        elif re.fullmatch(r'[\d\s+\-*/()]+', divisor_candidate):
                             # Try to evaluate simplified divisor parts
                            if eval(divisor_candidate, {"__builtins__": None}, {}) == 0:
                                raise ZeroDivisionError
                    except (SyntaxError, NameError, TypeError):
                        # Cannot evaluate divisor safely, proceed with full eval and let it fail
                        pass


            result = eval(expression_str, {"__builtins__": None}, {}) # Safely evaluate
            symbol_table[var_name] = result
            output_lines.append(f"Result: {result}")
        except ZeroDivisionError:
            output_lines.append(f"Result for {var_name}: Error - Division by zero in expression: {expression_str}")
        except Exception as e:
            output_lines.append(f"Result for {var_name}: Error - Could not evaluate '{expression_str}': {e}")
            
    if not output_lines:
        return "No arithmetic assignments found."

    return "\n".join(output_lines)

def operator_delimiter_recognizer(c_code):
    _compile_operator_delimiter_recognizer()
    if _OPERATOR_DELIMITER_RECOGNIZER_COMPILE_ERROR:
        return f"Error: {_OPERATOR_DELIMITER_RECOGNIZER_COMPILE_ERROR}"
    if not _OPERATOR_DELIMITER_RECOGNIZER_EXECUTABLE:
        return "Operator & Delimiter Recognizer is not ready (compilation failed or not attempted)."

    stdout, stderr = run_flex_bison_program(_OPERATOR_DELIMITER_RECOGNIZER_EXECUTABLE, c_code)
    if stderr:
        return f"Operator & Delimiter Recognizer Error:\n{stderr}"
    
    return stdout

def parser_action_printer(c_code):
    _compile_parser_action_printer()
    if _PARSER_ACTION_PRINTER_COMPILE_ERROR:
        return f"Error: {_PARSER_ACTION_PRINTER_COMPILE_ERROR}"
    if not _PARSER_ACTION_PRINTER_EXECUTABLE:
        return "Parser Action Printer is not ready (compilation failed or not attempted)."

    stdout, stderr = run_flex_bison_program(_PARSER_ACTION_PRINTER_EXECUTABLE, c_code)
    if stderr:
        return f"Parser Action Printer Error:\n{stderr}"
    
    return stdout

def compiler_error_classifier(input_text):
    print(f"DEBUG: Input text received by compiler_error_classifier:\n'''{input_text}'''") # DEBUG LINE
    # Split the input into C code and error message
    parts = input_text.split("Error:", 1)
    if len(parts) < 2:
        return "Invalid input format. Please provide C code followed by 'Error:' and the compiler error message."

    c_code_snippet = parts[0].strip()
    compiler_error_message = parts[1].strip()

    error_type = "Unknown"
    cause = "Could not determine the cause."
    location = "Unknown"
    fix = "Could not suggest a fix."
    explanation = "No detailed explanation available."

    # --- Rule-based classification based on common C compiler errors ---

    # Syntax Error: Missing semicolon
    if re.search(r"expected ';'", compiler_error_message):
        error_type = "Syntax Error"
        cause = "A semicolon is missing at the end of a statement."
        # Attempt to find the line before the error message, assuming it refers to the line it expects a semicolon.
        match = re.search(r":(\d+):\d+:", compiler_error_message)
        if match:
            line_num = int(match.group(1))
            lines = c_code_snippet.splitlines()
            if 0 < line_num <= len(lines):
                location = f"Line {line_num}: {lines[line_num-1].strip()}"
            else:
                location = "Around the statement before the error."
        else:
            location = "Around the statement before the error."
        fix = "Add a semicolon (;) at the end of the problematic statement."
        explanation = "C language requires most statements to be terminated by a semicolon to indicate their end."

    # Syntax Error: Undeclared identifier
    elif re.search(r"undeclared identifier", compiler_error_message):
        error_type = "Semantic Error" # Often caught by compiler, but semantically it's a naming issue
        cause = "A variable or function is used without being declared first."
        match = re.search(r"undeclared identifier '([^']+)'", compiler_error_message)
        if match:
            identifier = match.group(1)
            location = f"Use of undeclared identifier '{identifier}'"
            fix = f"Declare '{identifier}' before using it, or ensure it's spelled correctly."
            explanation = "All variables and functions in C must be declared with their type before they can be used."
        else:
            location = "Referenced identifier is undeclared."
            fix = "Declare the identifier or check its spelling."
            explanation = "C requires explicit declarations for all names."

    # Syntax Error: Expected expression (e.g., int a = ;)
    elif re.search(r"expected expression before", compiler_error_message) and re.search(r"=", c_code_snippet):
        error_type = "Syntax Error"
        cause = "An assignment operator (=) is used, but no value is provided on the right-hand side."
        match = re.search(r":(\d+):\d+:", compiler_error_message) # Try to find line from error
        if match:
            line_num = int(match.group(1))
            lines = c_code_snippet.splitlines()
            if 0 < line_num <= len(lines):
                location = f"Line {line_num}: {lines[line_num-1].strip()}"
            else:
                location = "In an assignment without a right-hand expression."
        else:
            location = "In an assignment without a right-hand expression."
        fix = "Assign a value to the variable (e.g., `int a = 5;`) or remove the assignment operator if only declaration is intended (e.g., `int a;`)."
        explanation = "The assignment operator expects an expression to its right. Providing a value or removing the operator corrects the syntax."
    
    # Semantic/Type Error: Type mismatch in assignment or function call
    elif re.search(r"conflicting types for", compiler_error_message) or re.search(r"incompatible types", compiler_error_message):
        error_type = "Semantic Error"
        cause = "A variable or function is being used with a type that is different from its declaration or expectation."
        location = "Assignment or function call with type mismatch."
        fix = "Ensure that the types on both sides of an assignment, or arguments in a function call, are compatible. Use type casting if necessary."
        explanation = "C is a strongly-typed language. Data types must match or be compatible for assignments and function arguments."

    # Syntax Error: Missing closing parenthesis
    elif re.search(r"expected '\)' before", compiler_error_message):
        error_type = "Syntax Error"
        cause = "A closing parenthesis is missing, often in a function call, conditional statement (if/while), or expression."
        location = "Expression or statement missing a closing parenthesis."
        fix = "Add the missing closing parenthesis `)`."
        explanation = "Parentheses are used in C for grouping expressions and defining function arguments. Each opening parenthesis must have a corresponding closing one."

    # Linker Error: Undefined reference
    elif re.search(r"undefined reference to", compiler_error_message):
        error_type = "Linker Error"
        cause = "The program refers to a function or global variable that has been declared but not defined (implemented), or the library containing its definition is not linked."
        match = re.search(r"undefined reference to `([^']+)'", compiler_error_message)
        if match:
            symbol = match.group(1)
            location = f"Reference to undefined symbol '{symbol}'"
            fix = f"Provide a definition (implementation) for '{symbol}', or link the necessary library using a compiler flag (e.g., `-lm` for math functions)."
            explanation = "Linking combines compiled object files and resolves references to functions and variables. If a definition is missing, the linker cannot complete its task."

    # Generic Syntax Error
    elif re.search(r"syntax error", compiler_error_message):
        error_type = "Syntax Error"
        cause = "The code violates the grammatical rules of the C language."
        location = "Near the reported error message."
        fix = "Carefully review the code around the error message for misplaced keywords, missing operators, or incorrect statement structures."
        explanation = "Syntax errors prevent the compiler from understanding the structure of your code."
    
    # Generic Semantic Error
    elif re.search(r"error:", compiler_error_message) and error_type == "Unknown":
        error_type = "Semantic Error"
        cause = "The code is grammatically correct but violates C's type or meaning rules (e.g., using a variable out of scope, incorrect types in operations)."
        location = "General location indicated by compiler error."
        fix = "Analyze variable scopes, types, and the logic of operations around the error message."
        explanation = "Semantic errors relate to the meaning of the code, not just its structure."
    
    # Generic Compilation Error (fallback)
    elif error_type == "Unknown":
        error_type = "Compilation Error (Generic)"
        cause = "An unspecified error occurred during the compilation process."
        location = "General location indicated by compiler error."
        fix = "Examine the compiler error message carefully and cross-reference with C language rules. Start by checking for simple typos or missing punctuation."
        explanation = "This is a general category for errors that don't fit more specific classifications."


    output = []
    output.append(f"Error Type: {error_type}")
    output.append(f"Cause: {cause}")
    output.append(f"Location: {location}")
    output.append(f"Fix: {fix}")
    output.append(f"Explanation: {explanation}")

    return "\n".join(output)

def semantic_action_simulator(c_code):
    _compile_semantic_action_simulator()
    if _SEMANTIC_ACTION_SIMULATOR_COMPILE_ERROR:
        return f"Error: {_SEMANTIC_ACTION_SIMULATOR_COMPILE_ERROR}"
    if not _SEMANTIC_ACTION_SIMULATOR_EXECUTABLE:
        return "Semantic Action Simulator is not ready (compilation failed or not attempted)."

    stdout, stderr = run_flex_bison_program(_SEMANTIC_ACTION_SIMULATOR_EXECUTABLE, c_code)
    if stderr:
        return f"Semantic Action Simulator Error:\n{stderr}"
    
    return stdout
def execute_single_command(command, variables):
    output = ""
    
    # Helper to resolve value (either a number or a variable)
    def _get_val(v):
        v = v.strip()
        if v in variables:
            try:
                return float(variables[v])
            except ValueError:
                raise ValueError(f"Variable '{v}' is not a number.")
        return float(v)

    if not command or command.startswith('//') or command.startswith('#'):
        return {"output": "", "new_variables": variables}

    # "set <variable> to <value>"
    match = re.match(r"set (\w+) to (.+)", command, re.IGNORECASE)
    if match:
        var, val = match.groups()
        variables[var] = val.strip()
        output = f"Set {var} = {val.strip()}"
        return {"output": output, "new_variables": variables}

    # "show <variable>"
    match = re.match(r"show (\w+)", command, re.IGNORECASE)
    if match:
        var = match.group(1)
        if var in variables:
            output = f"{var} = {variables[var]}"
        else:
            output = f"Error: Variable '{var}' not found."
        return {"output": output, "new_variables": variables}

    # "add <a> and <b>"
    match = re.match(r"add (.+) and (.+)", command, re.IGNORECASE)
    if match:
        a_str, b_str = match.groups()
        try:
            a = _get_val(a_str)
            b = _get_val(b_str)
            output = str(a + b)
        except (ValueError, KeyError) as e:
            output = f"Error in add: Invalid number or variable in '{command}'."
        return {"output": output, "new_variables": variables}

    # "multiply <a> and <b>"
    match = re.match(r"multiply (.+) and (.+)", command, re.IGNORECASE)
    if match:
        a_str, b_str = match.groups()
        try:
            a = _get_val(a_str)
            b = _get_val(b_str)
            output = str(a * b)
        except (ValueError, KeyError) as e:
            output = f"Error in multiply: Invalid number or variable in '{command}'."
        return {"output": output, "new_variables": variables}

    # "divide <a> by <b>"
    match = re.match(r"divide (.+) by (.+)", command, re.IGNORECASE)
    if match:
        a_str, b_str = match.groups()
        try:
            a = _get_val(a_str)
            b = _get_val(b_str)
            if b == 0:
                output = "Error: Division by zero."
            else:
                output = str(a / b)
        except (ValueError, KeyError) as e:
            output = f"Error in divide: Invalid number or variable in '{command}'."
        return {"output": output, "new_variables": variables}

    # "if <condition> then print <text>"
    match = re.match(r"if (.+?) then print (.+)", command, re.IGNORECASE)
    if match:
        condition, text = match.groups()
        cond_match = re.match(r"(\w+)\s*([><=!]+)\s*(.+)", condition)
        if cond_match:
            var, op, val = cond_match.groups()
            try:
                var_val = _get_val(var)
                comp_val = _get_val(val)
                result = False
                if op == '>': result = var_val > comp_val
                elif op == '<': result = var_val < comp_val
                elif op == '==': result = var_val == comp_val
                elif op == '!=': result = var_val != comp_val
                
                if result:
                    output = text.strip()
            except (ValueError, KeyError):
                output = f"Error in condition: Invalid number or variable in '{condition}'."
        else:
            output = f"Error: Unsupported condition format in '{condition}'."
        return {"output": output, "new_variables": variables}

    # "exit"
    if command.lower() == "exit":
        output = "Exiting..."
        return {"output": output, "new_variables": variables}

    # If no command matched
    output = f"Error: Unknown command '{command}'"
    return {"output": output, "new_variables": variables}

def boolean_expression_evaluator(c_code):
    _compile_boolean_evaluator()
    if _BOOLEAN_EVALUATOR_COMPILE_ERROR:
        return f"Error: {_BOOLEAN_EVALUATOR_COMPILE_ERROR}"
    if not _BOOLEAN_EVALUATOR_EXECUTABLE:
        return "Boolean Expression Evaluator is not ready (compilation failed or not attempted)."

    try:
        # The C code requires each expression on a new line and will output each result on a new line.
        # So we format the input for the C program.
        input_for_c = ""
        lines = c_code.splitlines()
        for line in lines:
            clean_line = line.strip()
            # Extract content from printf, or use the whole line if not printf
            match_printf = re.search(r'printf\s*\(\s*"(.*?)"\s*\);?', clean_line, re.DOTALL)
            if match_printf:
                expression = match_printf.group(1).strip()
                if expression: # Only add non-empty expressions
                    input_for_c += expression + "\n"
            elif clean_line and not (clean_line.startswith('//') or clean_line.startswith('#') or \
                                     clean_line.startswith('int main') or clean_line.startswith('return 0') or \
                                     clean_line.startswith('{') or clean_line.startswith('}')):
                input_for_c += clean_line + "\n"
        
        # If no expressions were extracted, return a message
        if not input_for_c.strip():
            return "No valid boolean expressions found or parsed from the input."

        process = subprocess.run(
            [_BOOLEAN_EVALUATOR_EXECUTABLE],
            input=input_for_c, # Pass the formatted input to the C program
            capture_output=True,
            text=True,
            check=False,
            timeout=15
        )
        return process.stdout
    except subprocess.CalledProcessError as e:
        # If the C program itself returns a non-zero exit code
        return f"Error during execution of Boolean Evaluator:\n{e.stderr}\n{e.stdout}"
    except subprocess.TimeoutExpired:
        return "Error: Boolean Evaluator execution timed out."
    except FileNotFoundError:
        return "Error: Boolean Evaluator executable not found. Did compilation fail?"
    except Exception as e:
        return f"An unexpected error occurred during Boolean Evaluator execution: {e}"


def flex_bison_arithmetic_calculator(c_code):
    _compile_arithmetic_calculator()
    if _ARITHMETIC_CALCULATOR_COMPILE_ERROR:
        return f"Error: {_ARITHMETIC_CALCULATOR_COMPILE_ERROR}"
    if not _ARITHMETIC_CALCULATOR_EXECUTABLE:
        return "Arithmetic Calculator is not ready (compilation failed or not attempted)."

    try:
        # Simplified: Assume c_code already contains the expression to be evaluated
        # The parser expects an expression followed by EOL, so append a newline.
        input_for_c = c_code.strip() + "\n" # Ensure no leading/trailing whitespace, then add EOL

        if not input_for_c.strip(): # Check if it's still empty after stripping and adding newline
            return "No arithmetic expressions found in the input."

        process = subprocess.run(
            [_ARITHMETIC_CALCULATOR_EXECUTABLE],
            input=input_for_c,
            capture_output=True,
            text=True,
            check=False,
            timeout=15
        )

        output = process.stdout
        error_output = process.stderr

        if error_output:
            filtered_error = "\n".join([line for line in error_output.splitlines() if "memory exhausted" not in line and "syntax error" in line])
            if filtered_error:
                output += f"\nParser Errors:\n{filtered_error}"

        if process.returncode != 0 and not error_output:
            output += f"\nProgram exited with non-zero code: {process.returncode} (no specific error message from stderr)."


        return output
    except subprocess.TimeoutExpired:
        return "Error: Arithmetic Calculator execution timed out."
    except FileNotFoundError:
        return "Error: Arithmetic Calculator executable not found. Did compilation fail?"
    except Exception as e:
        return f"An unexpected error occurred during Arithmetic Calculator execution: {e}"

# NEW FUNCTION FOR COMMAND LANGUAGE INTERPRETER
def process_command_language(c_code):
    output_lines = []
    variables = {} # Persist variables across commands
    
    # Split input into lines and process each
    lines = c_code.splitlines()
    
    for line in lines:
        cleaned_line = strip_comments(line).strip()
        
        if not cleaned_line: # Skip empty lines after stripping comments
            continue
            
        result = execute_single_command(cleaned_line, variables)
        
        # execute_single_command returns a dictionary: {"output": ..., "new_variables": ...}
        command_output = result.get("output", "").strip()
        variables = result.get("new_variables", variables) # Update variables for next command
        
        if command_output:
            output_lines.append(command_output)
            
        if "Exiting..." in command_output:
            break # Stop processing if exit command is encountered
            
    return "\n".join(output_lines)
