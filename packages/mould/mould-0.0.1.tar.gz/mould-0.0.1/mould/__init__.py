import os
import platform


def _variable_parser(text):
    '''
    Description:
    This function parses the given text with variables and returns the variables and strings in comma separated format to put them directly to a print statement

    Paramaters:
    text (string) : This string is supposed to have plain text with variables or variable expressions

    Returns: The plain text and variables / variable expressions are returned as a comma separated string which can be directly put into a print statement

    Example:

            $ _variabe_parser("Hello {{ world }}")
            "Hello",world
    '''
    left_marker = "{{"
    right_marker = "}}"
    quotes = '"'
    output = []

    while len(text) != 0:
        if left_marker in text:
            text = text.split(left_marker, 1)
            if text[0] != "":
                output.append(quotes+(text[0].strip())+quotes)
            text = text[1].strip().split(right_marker, 1)
            output.append(text[0].strip())
            if text[1] != "":
                text = text[1]
        else:
            if text[-1] != "":
                output.append(quotes+text+quotes)
            break

    return(",".join(output))


# Builds the python code for the input supplied with variables and saves it in the 'output_string'
def _code_builder(input_content, variables):
    '''
    Description:
    This function builds executable python code with appropriate indentation so that the code can be run as such to render the user's input text.
    It processes plain lines, lines with if,else,elif,for blocks and lines with variables and variable expressions

    Parameters:
    input_content (string) : This is the user input, which is assumed to have multiple lines
    variables (dictionary) : This contains the list of varibales and their values as key-value pairs

    Returns: Executable python code as a string

    Example:
            $sample_input = "
             This is where it all starts!!!
             Hello {{ text }} This is a wonderful day. My name is {{ name }}.
             "
            $sample_variables = {
                "text" : "World !"
                "name" : "Python"
                }
            $_code_builder(sample_input, sample_variables)
            text = "World !"
            name = "Python"
            print("Hello",text,"This is a wonderful day. My name is",name)
    '''

    variable_marker = "{{"
    left_marker = "{%"
    right_marker = "%}"
    end_if_block = "endif"
    end_for_block = "endfor"
    output_string = ""
    indent = 0
    space = " "
    quotes = '"'
    assignment_sign = " = "
    line_break = "\n"
    scoping_colon = ": "
    print_block_start = "print("
    print_block_end = ")"

    for key, value in variables.items():
        # with open(output_file, "a") as f:
        if type(value) != str:
            output_string = output_string + \
                (indent*space) + key + \
                assignment_sign + str(value) + line_break
        else:
            output_string = output_string + \
                (indent*space)+key+assignment_sign + \
                quotes+str(value)+quotes+line_break

    for every_line in input_content.split(line_break):
        line = every_line.strip()

        # Checks for if,else,elif and for blocks and adds the relevant python code block to the output code

        if line.startswith(left_marker) and line.endswith(right_marker) and not end_if_block in line.split() and not end_for_block in line.split():
            line_split = line.split()
            if line_split[1] in ["else", "elif"]:
                indent -= 4
                output_string = output_string + \
                    (indent*space) + \
                    space.join(line_split[1:-1])+scoping_colon+line_break
                indent += 4
            elif line_split[1] in ["if", "for"]:
                output_string = output_string + \
                    (indent*space) + \
                    space.join(line_split[1:-1])+scoping_colon+line_break
                indent += 4

        # Checks for endif block to close the indentation generated for if block previously in the output code

        elif line.startswith(left_marker) and line.endswith(right_marker) and (end_if_block in line.split() or end_for_block in line.split()):
            indent -= 4

        # Adds the variable declaration statements and variable expression statements in output python code

        elif variable_marker in line and left_marker not in line:
            output_string = output_string + \
                (indent*space)+print_block_start + \
                _variable_parser(line)+print_block_end+line_break

        # Checks for plain lines to be printed as such and add them to the output code

        elif variable_marker not in line and left_marker not in line:
            output_string = output_string + \
                (indent*space)+print_block_start + quotes + \
                line+quotes+print_block_end+line_break
    return output_string

# Wrapper function that calls the code builder with input content and input variables


def it(input_template_content, input_variables):
    '''
    Description:
    This function gets the user input and renders the templated output with values applied for the variables, conditionals and loops processed

    Parameters:
    input_template_content (string or file) : This is the user input, which can be a string or a file.
    input_variables (dictionary) : This is the collection of variables and thier values as a dictionary

    Returns:
    output_text (string) : Returns the rendered file as a string

    Usage Example:
                $ sample_input = "
                 This is where it all starts!!!
                 Hello {{ text }} This is a wonderful day. My name is {{ name }}.
                 {% if a < b %}
                 'b' is bigger
                 The value of b is {{ b }}
                 {% else %}
                 'a' is bigger
                 The value of a is {{ a }}
                 {% endif %}
                 "
                $ sample_variables = {
                 "text" : "World !"
                 "name" : "Python"
                 "a" : 50
                 "b" : 100
                }
                $ mould.it(sample_input,sample_variables)
                This is where it all starts!!!
                Hello World ! This is a wonderful day. My name is Python
                'b' is bigger
                The value of b is 100

    '''
    # Checks whether the input format is a string or a file and inputs to code_builder function accordingly
    input_content = ""
    temporary_code_file = "temp_mould_it.py"
    temporary_output_file = "temp_mould.it.py_output"
    if platform.system() == "Windows":
        py = "python "
    else:
        py = "python3 "
    if os.path.isfile(input_template_content):
        input_content = open(input_template_content).read()
    else:
        input_content = input_template_content

    built_code = _code_builder(input_content, input_variables)

    # Executes the rendered code and generates the output file
    with open(temporary_code_file, "w+") as f:
        f.write(built_code)
    command = py+temporary_code_file + ">> "+temporary_output_file
    os.system(command)
    output_text = open(temporary_output_file).read()
    os.remove(temporary_code_file)
    os.remove(temporary_output_file)
    return output_text.strip()
