# <i>mould</i> - A minimalistic templating engine for Python

This Python library helps to render HTML pages and plain text  with variable substitutions, if conditions and for loops.


## Templating syntax :

## To delcare variables enclose the variable name with '%%'

    Hello {{ text }} -- 'text' is the variable here

You can use the same syntax to write variable expressions.

    This is line number {{ n+10 }}

## <b>if</b> conditional
<br>
Use '{%' and '%}' to enclose the lines where an if block starts and use the same with 'endif' keyword for closing the if blocks

    
    {% if 5 < 6  %}
    <p1> Hello world! </p1>
    {% endif %}
    
Variable names can also be used to write if conditions.

    {% if x > y %}
    <p1> Hello Python! </p1>
    {% endif %}
    
IF block supports else and elif as well.

## <b>for</b> loop

Use '{%' and '%}' to enclose the lines where a for block starts and use the same with 'endfor' keyword for closing the if blocks
    
    {% for n in l %}
    This is line {{ n }} printed using for loop
    {% endfor %}

In the above code, 'n' and 'l' are variables where 'n' is the looping variable and 'l' is the list on whose items the loop is run

<b>for</b> supports looping over lists and dictionaries

# How to use:

You can install this using pip

    pip install mould

Import the library to your python program
    
    import mould

Call the mould.it() with you input file / input text along with the dictionary of variables that you have used in your text / input file

    mould.it(input_text, variables_dictionary)

This will return the rendered output. You can either print it direclty or save it.

    print(mould.it(input_text, variables_dictionary))
or

    rendered_data = mould.it(input_text, variables_dictionary))

# Dependencies:

<i>mould</i> uses python standard library <b>os</b> alone and nothing else.