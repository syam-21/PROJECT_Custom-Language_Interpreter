import subprocess
import os

FLEX_BIN = 'flex'
BISON_BIN = 'bison'
GPP_BIN = 'g++'

def compile_flex_bison(name, flex_file, bison_file, output_dir="."):
    """
    Compiles a Flex (.l) and Bison (.y) file pair into an executable.
    
    Args:
        name (str): The base name for the generated files (e.g., 'calculator').
        flex_file (str): Path to the .l file.
        bison_file (str): Path to the .y file.
        output_dir (str): Directory to place generated files and executable.
        
    Returns:
        tuple: (bool, str) - True if successful, False otherwise, and a message.
    """
    
    if not os.path.isabs(output_dir):
        output_dir = os.path.abspath(output_dir)
        
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Change to output directory for compilation
    original_cwd = os.getcwd()
    os.chdir(output_dir)

    try:
        # 1. Compile Bison file
        bison_command = [BISON_BIN, "-d", bison_file]
        # Make bison_file an absolute path if it's not already
        if not os.path.isabs(bison_file):
            bison_file = os.path.join(original_cwd, bison_file)
        
        print(f"DEBUG: Running bison command: {' '.join(bison_command)}") # DIAGNOSTIC PRINT
        print(f"DEBUG: Current working directory: {os.getcwd()}") # DIAGNOSTIC PRINT

        proc = subprocess.run(bison_command, capture_output=True, check=False) # REMOVED text=True
        if proc.returncode != 0:
            return False, f"Bison compilation failed for {bison_file}:\n{proc.stderr.decode('utf-8')}" # DECODE manually
        
        # 2. Compile Flex file
        flex_command = [FLEX_BIN, flex_file]
        # Make flex_file an absolute path if it's not already
        if not os.path.isabs(flex_file):
            flex_file = os.path.join(original_cwd, flex_file)
            
        print(f"DEBUG: Running flex command: {' '.join(flex_command)}") # DIAGNOSTIC PRINT
        print(f"DEBUG: Current working directory: {os.getcwd()}") # DIAGNOSTIC PRINT
            
        proc = subprocess.run(flex_command, capture_output=True, check=False) # REMOVED text=True
        if proc.returncode != 0:
            return False, f"Flex compilation failed for {flex_file}:\n{proc.stderr.decode('utf-8')}" # DECODE manually

        # 3. Compile the generated C files
        # The .y file generates name.tab.c and name.tab.h
        # The .l file generates lex.yy.c
        # Ensure name.tab.c and lex.yy.c are linked
        c_files = [f"{name}.tab.c", "lex.yy.c"]
        output_exec = name
        
        gpp_command = [GPP_BIN] + c_files + ["-o", output_exec]
        if os.name == 'nt': # Check if running on Windows
            gpp_command.append('-mconsole')
        
        print(f"DEBUG: Running g++ command: {' '.join(gpp_command)}") # DIAGNOSTIC PRINT
        print(f"DEBUG: Current working directory: {os.getcwd()}") # DIAGNOSTIC PRINT

        proc = subprocess.run(gpp_command, capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            return False, f"GCC compilation failed for {name}:\n{proc.stderr}"

        return True, os.path.join(output_dir, output_exec) # Return the absolute path to the executable

    except FileNotFoundError as e:
        return False, f"Compiler not found: {e.filename}. Make sure Flex, Bison, and GCC are installed and in PATH."
    except Exception as e:
        return False, f"An unexpected error occurred during compilation: {str(e)}"
    finally:
        os.chdir(original_cwd) # Revert to original directory


def run_flex_bison_program(executable_path, input_text):
    """
    Runs a compiled Flex/Bison executable with the given input.
    
    Args:
        executable_path (str): Path to the compiled executable.
        input_text (str): The input to feed to the program's stdin.
        
    Returns:
        tuple: (str, str) - stdout, stderr
    """
    try:
        # Pass input_text to stdin of the subprocess
        proc = subprocess.run(
            [executable_path],
            input=input_text,
            capture_output=True,
            text=True,
            check=False
        )
        return proc.stdout, proc.stderr
    except FileNotFoundError:
        return "", f"Error: Executable not found at {executable_path}. Has it been compiled?"
    except Exception as e:
        return "", f"An unexpected error occurred during execution: {str(e)}"
