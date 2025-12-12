document.addEventListener('DOMContentLoaded', () => {
    const inputText = document.getElementById('input-text');
    const optionsSelector = document.getElementById('options-selector');
    const runButton = document.getElementById('run-button');
    const outputText = document.getElementById('output-text');
    const loadingSpinner = document.getElementById('loading-spinner');

    runButton.addEventListener('click', async () => {
        const option = optionsSelector.value;
        
        outputText.textContent = ''; // Clear previous output
        outputText.classList.remove('error-text');

        if (!option) {
            outputText.textContent = "Please select a functionality.";
            outputText.classList.add('error-text');
            return;
        }

        // Handle the new interactive command language interpreter
        if (option === 'command_language_interpreter') {
            await runInteractiveInterpreter();
            return;
        }

        // Existing logic for other options
        let input = inputText.value;
        let body = { option }; // Initialize body with just option

        if (option === 'regex_matcher') {
            const pattern = prompt("Please enter the regex pattern:");
            if (pattern === null || pattern.trim() === '') {
                outputText.textContent = "Regex pattern cannot be empty.";
                outputText.classList.add('error-text');
                return;
            }
            body.input = input; // Add original input to body
            body.pattern = pattern;
        } else if (option === 'run_full_c_code') {
            const parts = input.split('---USER_INPUT---', 2);
            body.c_code = parts[0].trim();
            body.user_input_string = parts.length > 1 ? parts[1].trim() : '';
        } else {
            body.input = input; // For all other options, send the full input
        }

        loadingSpinner.style.display = 'block'; // Show spinner
        runButton.disabled = true;

        try {
            const response = await fetch('/api/interpret', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });

            const data = await response.json();
            outputText.textContent = data.output;
            if (data.output.includes("ERROR:") || data.output.includes("Error:")) {
                outputText.classList.add('error-text');
            }

        } catch (error) {
            console.error('Error:', error);
            outputText.textContent = 'An error occurred while communicating with the backend.';
            outputText.classList.add('error-text');
        } finally {
            loadingSpinner.style.display = 'none'; // Hide spinner
            runButton.disabled = false;
        }
    });

    async function runInteractiveInterpreter() {
        let variables = {};
        outputText.textContent = "Starting interactive session...\n";
        
        while (true) {
            const command = prompt("Enter command (or 'exit' to quit):");

            if (command === null) { // User clicked cancel
                outputText.textContent += "\nSession cancelled.";
                break;
            }
            
            if (command.trim().toLowerCase() === 'exit') {
                 outputText.textContent += `> ${command}\nExiting...`;
                 break;
            }

            loadingSpinner.style.display = 'block';
            runButton.disabled = true;

            try {
                const response = await fetch('/api/execute_cli_command', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ command, variables }),
                });

                const data = await response.json();
                
                // Update frontend state
                variables = data.new_variables;

                // Display output
                outputText.textContent += `> ${command}\n${data.output}\n`;

            } catch (error) {
                console.error('Error:', error);
                outputText.textContent += 'An error occurred while communicating with the backend.\n';
                outputText.classList.add('error-text');
                break; 
            } finally {
                loadingSpinner.style.display = 'none';
                runButton.disabled = false;
            }
        }
        runButton.disabled = false;
    }
});
