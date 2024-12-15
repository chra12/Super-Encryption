import base64
import codecs
import os
import time
from cryptography.fernet import Fernet
from PyQt5.QtGui import QTextCursor, QColor

# Set up colors
CYAN = QColor(0, 255, 255)  # Light blue color
GREEN = QColor(0, 255, 0)  # Green color
YELLOW = QColor(255, 255, 0)  # Yellow color
RED = QColor(255, 0, 0)  # Red color
MAGENTA = QColor(255, 0, 255)  # Pink color
BLUE = QColor(0, 0, 255)  # Blue color
WHITE = QColor(255, 255, 255)  # White color
SILVER = QColor(192, 192, 192)  # Silver color
GOLD = QColor(255, 215, 0)  # Gold color

# New colors
ORANGE = QColor(255, 165, 0)  # Orange color
LIGHT_BLUE = QColor(173, 216, 230)  # Light blue color
LIGHT_GREEN = QColor(144, 238, 144)  # Light green color
VIOLET = QColor(238, 130, 238)  # Violet color
LIGHT_PINK = QColor(255, 182, 193)  # Light pink color
LIGHT_YELLOW = QColor(255, 255, 224)  # Light yellow color
DARK_BLUE = QColor(0, 0, 139)  # Dark blue color
DARK_RED = QColor(139, 0, 0)  # Dark red color

# Static AES (Fernet) key
key = Fernet.generate_key()
cipher = Fernet(key)

def apply_encryption(file_path, layers, encryption_choice, text_edit):
    # Check if the file exists
    if not os.path.exists(file_path):
        append_colored_text(text_edit, "Error: File not found.", RED)
        return None, None

    try:
        # Read file content
        with open(file_path, "r", encoding="utf-8") as file:
            original_code = file.read()
    except Exception as e:
        append_colored_text(text_edit, f"Error reading file: {str(e)}", RED)
        return None, None

    # Check file size (to maintain performance)
    if len(original_code) > 10**6:  # Limit of 1 megabyte
        append_colored_text(text_edit, "Warning: File size is too large, process might be slow.", YELLOW)

    # Start the text to be encrypted
    code = original_code

    # Colors assigned to each layer
    colors = [CYAN, GREEN, YELLOW, RED, MAGENTA, BLUE, WHITE]

    start_time = time.time()

    for i in range(layers):
        try:
            # Choose a color for each layer
            color = colors[i % len(colors)]

            # Perform encryption based on the choice
            if encryption_choice == "Base64" or (encryption_choice == "All Types Base64 ROT13 Hex Encoding" and i % 4 == 0):
                code = base64.b64encode(code.encode()).decode()
                append_colored_text(text_edit, f"Layer {i+1}: Base64 encoding applied.", color)
            elif encryption_choice == "ROT13" or (encryption_choice == "All Types Base64 ROT13 Hex Encoding" and i % 4 == 1):
                code = codecs.encode(code, 'rot_13')
                append_colored_text(text_edit, f"Layer {i+1}: ROT13 encoding applied.", color)
            elif encryption_choice == "Hex Encoding" or (encryption_choice == "All Types Base64 ROT13 Hex Encoding" and i % 4 == 2):
                code = code.encode().hex()
                append_colored_text(text_edit, f"Layer {i+1}: Hex encoding applied.", color)

        except Exception as e:
            append_colored_text(text_edit, f"Error in layer {i+1}: {str(e)}", RED)
            break

    # Record the elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Return the encrypted text and elapsed time
    return code, elapsed_time

def generate_decryption_code(encrypted_code, layers, file_extension):
    if file_extension in ['.py']:
        decryption_code = f"""
import base64
import codecs
import time
from cryptography.fernet import Fernet

# Set up colors
RESET = '\\033[0m'
CYAN = '\\033[96m'
GREEN = '\\033[92m'
YELLOW = '\\033[93m'
RED = '\\033[91m'
BOLD_RED = '\\033[1;91m'
BOLD_GREEN = '\\033[1;32m'
BOLD_YELLOW = '\\033[1;33m'
BOLD_BLUE = '\\033[1;34m'
BOLD_MAGENTA = '\\033[1;35m'
BOLD_CYAN = '\\033[1;96m'
# Define the number of layers
layers = {layers}

# AES key
key = {key!r}
cipher = Fernet(key)

# Encrypted code
code = {encrypted_code!r}

# Decryption process
print(f"Decrypting Layer ", GREEN)
for i in reversed(range(layers)):

    if i % 4 == 2:  # Hex decoding
        code = bytes.fromhex(code).decode()
    elif i % 4 == 1:  # ROT13 decoding
        code = codecs.decode(code, 'rot_13')
    elif i % 4 == 0:  # Base64 decoding
        code = base64.b64decode(code).decode()
    time.sleep(0.1)

exec(code)
"""

    elif file_extension == '.sh':
        decryption_code = f"""
#!/bin/bash
# Set up colors
RESET='\\033[0m'
RED='\\033[91m'
GREEN='\\033[92m'
CYAN='\\033[96m'

# Number of layers
layers={layers}
key={key!r}

# Encrypted code
code="{encrypted_code}"

# Check inputs
if [[ -z "$code" ]]; then
    echo -e "${{RED}}Error: Missing AES key or encrypted code.${{RESET}}"
    exit 1
fi

echo -e "${{GREEN}}Starting Decryption Process...${{RESET}}"
for ((i = layers - 1; i >= 0; i--)); do

    if ((i % 4 == 2)); then
        # Hex decoding
        code=$(echo -n "$code" | xxd -r -p 2>/dev/null)
    elif ((i % 4 == 1)); then
        # ROT13 decoding
        code=$(echo "$code" | tr 'A-Za-z' 'N-ZA-Mn-za-m')
    elif ((i % 4 == 0)); then
        # Base64 decoding
        code=$(echo -n "$code" | base64 -d 2>/dev/null)
    fi
    sleep 0.1
done

echo -e "${{GREEN}}Decryption Completed Successfully:${{RESET}}"
echo "$code"  # Print the extracted code
sleep 0.1

# If the code is valid, it can be executed via eval
if [[ -n "$code" ]]; then
    echo "Executing the extracted code..."
    eval "$code"
else
    echo -e "${{RED}}Error: The decrypted code is empty or invalid.${{RESET}}"
    exit 1
fi

"""

    elif file_extension == '.js':
        decryption_code = f"""
const crypto = require('crypto');
const chalk = require('chalk');

const GREEN = chalk.green;
const CYAN = chalk.cyan;

# Number of layers
const layers = {layers};

# Encrypted code
let code = "{encrypted_code}";

# Decryption process
(async () => {{
    console.log(GREEN('Starting Decryption Process...'));

    for (let i = layers - 1; i >= 0; i--) {{
        if (i % 4 === 2) {{
            code = Buffer.from(code, 'hex').toString('utf-8');
        }} else if (i % 4 === 1) {{
            code = code.replace(/[a-zA-Z]/g, c =>
                String.fromCharCode(
                    (c <= 'Z' ? 90 : 122) >= (c = c.charCodeAt(0) + 13) ? c : c - 26
                )
            );
        }} else if (i % 4 === 0) {{
            code = Buffer.from(code, 'base64').toString('utf-8');
        }}
        await new Promise(resolve => setTimeout(resolve, 100));
    }}

    console.log(GREEN('Decryption Completed Successfully'));
    console.log(code);
    eval(code);
}})();

"""
    elif file_extension == '.ps1':
        decryption_code = f"""

# Set up colors
$RESET = "`e[0m"
$RED = "`e[91m"
$GREEN = "`e[92m"
$CYAN = "`e[96m"

# Number of layers
$layers = {layers}
$key = "{key}"

# Encrypted code
$code = "{encrypted_code}"

# Check inputs
if (-not $code) {{
    Write-Host "$RED Error: Missing AES key or encrypted code. $RESET"
    exit 1
}}

Write-Host "$GREEN Starting Decryption Process... $RESET"
for ($i = $layers - 1; $i -ge 0; $i--) {{
    if ($i % 4 -eq 2) {{
        # Hex decoding
        $code = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromHexString($code))
    }} elseif ($i % 4 -eq 1) {{
        # ROT13 decoding
        $code = -join ($code.ToCharArray() | ForEach-Object {{
            if ($_ -ge 'A' -and $_ -le 'Z') {{
                [char](((($_ -as [int]) - 65 + 13) % 26) + 65)
            }} elseif ($_ -ge 'a' -and $_ -le 'z') {{
                [char](((($_ -as [int]) - 97 + 13) % 26) + 97)
            }} else {{
                $_
            }}
        }})
    }} elseif ($i % 4 -eq 0) {{
        # Base64 decoding
        $code = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($code))
    }}
    Start-Sleep -Milliseconds 100
}}

Write-Host "$GREEN Decryption Completed Successfully: $RESET"
Start-Sleep -Milliseconds 100

# If the code is valid, it can be executed
if (-not [string]::IsNullOrEmpty($code)) {{
    Write-Host "$GREEN Executing the extracted code...$RESET"
    Invoke-Expression $code
}} else {{
    Write-Host "$RED Error: The decrypted code is empty or invalid. $RESET"
    exit 1
}}

"""
    elif file_extension == '.rb':
        decryption_code = f"""

require 'base64'
require 'time'
require 'securerandom'

layers = "{layers}"
code = "{encrypted_code}"
# Encryption key
key = SecureRandom.base64(32)

# Set up colors
RESET = "\\033[0m"
CYAN = "\\033[96m"
GREEN = "\\033[92m"
YELLOW = "\\033[93m"
RED = "\\033[91m"
BOLD_RED = "\\033[1;91m"
BOLD_GREEN = "\\033[1;32m"
BOLD_YELLOW = "\\033[1;33m"
BOLD_BLUE = "\\033[1;34m"
BOLD_MAGENTA = "\\033[1;35m"
BOLD_CYAN = "\\033[1;96m"

puts "#{{GREEN}}Starting Decryption Process...#{{RESET}}"

# Decryption process
(layers.to_i - 1).downto(0) do |i|

  begin
    if i % 4 == 2  # Hex decoding
      code = [code].pack('H*')
    elsif i % 4 == 1  # ROT13 decoding
      code = code.tr('A-Za-z', 'N-ZA-Mn-za-m')
    elsif i % 4 == 0  # Base64 decoding
      code = Base64.decode64(code)
    end
  rescue => e
    puts "#{{RED}}Error decoding: #{{e.message}}#{{RESET}}"
    break
  end

  sleep(0.5)  # Slight delay to illustrate the process
end

# Execute the decrypted code
begin
  eval(code)
rescue => e
  puts "#{{BOLD_RED}}Error executing code: #{{e.message}}#{{RESET}}"
end

"""
    elif file_extension == '.cpp':
        decryption_code = f"""
#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <stdexcept>
#include <iomanip>
#include <sstream>
#include <thread>
#include <chrono>
#include <random>
#include <algorithm>

# Control unit colors
#define RESET "\\033[0m"
#define GREEN "\\033[92m"
#define RED "\\033[91m"
#define BOLD_RED "\\033[1;91m"

std::string decodeBase64(const std::string &encoded) {{
    static const std::string base64_chars =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

    std::string decoded;
    std::vector<int> decoding_table(256, -1);
    for (size_t i = 0; i < base64_chars.size(); ++i) {{
        decoding_table[base64_chars[i]] = i;
    }}

    int val = 0, valb = -8;
    for (unsigned char c : encoded) {{
        if (decoding_table[c] == -1) break;
        val = (val << 6) + decoding_table[c];
        valb += 6;
        if (valb >= 0) {{
            decoded.push_back(char((val >> valb) & 0xFF));
            valb -= 8;
        }}
    }}
    return decoded;
}}

std::string decodeHex(const std::string &hex) {{
    std::string decoded;
    for (size_t i = 0; i < hex.length(); i += 2) {{
        std::string byte = hex.substr(i, 2);
        char chr = (char)(int)strtol(byte.c_str(), nullptr, 16);
        decoded.push_back(chr);
    }}
    return decoded;
}}

std::string decodeROT13(const std::string &text) {{
    std::string decoded = text;
    for (char &c : decoded) {{
        if (c >= 'a' && c <= 'z') {{
            c = (c - 'a' + 13) % 26 + 'a';
        }} else if (c >= 'A' && c <= 'Z') {{
            c = (c - 'A' + 13) % 26 + 'A';
        }}
    }}
    return decoded;
}}

void executeDecryptedCode(const std::string &code) {{
    std::string filename = "decrypted_code.cpp";
    std::ofstream outFile(filename);
    if (!outFile) {{
        throw std::runtime_error("Failed to create file for decrypted code.");
    }}
    outFile << code;
    outFile.close();

    std::cout << GREEN << "Saved decrypted code to: " << filename << RESET << std::endl;
    std::cout << GREEN << "Compiling and executing..." << RESET << std::endl;

    std::string command = "g++ -o decrypted_program " + filename + " && ./decrypted_program";
    int result = std::system(command.c_str());

    if (result != 0) {{
        throw std::runtime_error("Compilation or execution failed.");
    }}
}}

int main() {{
    std::string layers = "{layers}";
    std::string code = "{encrypted_code}";

    std::cout << GREEN << "Starting Decryption Process..." << RESET << std::endl;

    try {{
        int num_layers = std::stoi(layers);

        for (int i = num_layers - 1; i >= 0; --i) {{
            if (i % 4 == 2) {{
                code = decodeHex(code);
            }} else if (i % 4 == 1) {{
                code = decodeROT13(code);
            }} else if (i % 4 == 0) {{
                code = decodeBase64(code);
            }}

            std::this_thread::sleep_for(std::chrono::milliseconds(500));
        }}

        # Execute the decrypted code
        executeDecryptedCode(code);

    }} catch (const std::exception &e) {{
        std::cerr << BOLD_RED << "Error during decryption: " << e.what() << RESET << std::endl;
        return 1;
    }}

    return 0;
}}

"""
    else:
        decryption_code = ""
    return decryption_code

def append_colored_text(text_edit, text, color):
    cursor = text_edit.textCursor()
    cursor.movePosition(QTextCursor.End)

    # Set up the text for color
    format = cursor.charFormat()
    format.setForeground(color)

    # Apply the format
    cursor.setCharFormat(format)
    cursor.insertText(text + "\n")
    text_edit.setTextCursor(cursor)
