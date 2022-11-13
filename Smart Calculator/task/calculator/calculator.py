import re

OPERATOR_PRECEDENCE = {'^': 3, '*': 2, '/': 2, '+': 1, '-': 1}


class ArithmeticExpression:
    def __init__(self):
        self.ui_expression = ''
        self.infix_notation = []
        self.postfix_notation = []
        self.operator_stack = []
        self.calculating_stack = []
        self.assignment_dict = {}
        self.equals_index = 0


conversion = ArithmeticExpression()


def main():
    setattr(conversion, 'ui_expression', input().replace(' ', ''))
    try:
        if conversion.ui_expression[0] == '/':
            commands()
        else:
            check_if_variable_declaration()
    except IndexError:
        main()


def commands():
    """Processes a known or an unknown text command"""
    if conversion.ui_expression == '/help':
        print("""
What does this SmartCalculator app do?

1. Takes an infix arithmetic expression from user input. Accepted operators: *, ?, *, +, -, ^
2. Converts the infix expression to a postfix expression
3. Evaluates post fix expression, calculates and prints the result.
        """)
        main()
    elif conversion.ui_expression == '/exit':
        print('Bye!')
        quit()
    else:
        print('Unknown command')
    main()


def check_if_variable_declaration():
    """checks user input for an assignment declaration"""
    if '=' in conversion.ui_expression:
        conversion.equals_index = conversion.ui_expression.find('=')
        check_identifier()
    else:
        check_singleton()


def check_identifier():
    """checks validity of variable in assignment declaration """
    if conversion.ui_expression[:conversion.equals_index].isalpha():
        check_value()
    else:
        print('Invalid identifier')
        main()


def check_value():
    """checks validity of value in assignment declaration"""
    if conversion.ui_expression[conversion.equals_index + 1:].isalpha():
        check_if_value_from_key()
    elif conversion.ui_expression[conversion.equals_index + 1:].isnumeric():
        update_dictionary()
    else:
        print('Invalid assignment')
        main()


def check_if_value_from_key():
    """if value in assignment declaration is a dictionary key the value from the key is the assigned value"""
    if conversion.ui_expression[conversion.equals_index + 1:] in conversion.assignment_dict.keys():
        value_from_key = conversion.assignment_dict[conversion.ui_expression[conversion.equals_index + 1:]]
        conversion.assignment_dict.update({conversion.ui_expression[:conversion.equals_index]: value_from_key})
        main()
    elif not conversion.ui_expression[conversion.equals_index + 1:] in conversion.assignment_dict.keys():
        print('Unknown variable')
        main()
    else:
        update_dictionary()


def update_dictionary():
    conversion.assignment_dict.update(
        {conversion.ui_expression[:conversion.equals_index]: conversion.ui_expression[conversion.equals_index + 1:]})
    main()


def check_singleton():
    """Process a single string entry (+ve / -ve) or deals with an unknown variable or invalid expression."""
    if conversion.ui_expression.isnumeric():
        print(conversion.ui_expression)
        main()
    elif conversion.ui_expression.isalpha():
        if conversion.ui_expression in conversion.assignment_dict.keys():
            print(conversion.assignment_dict[conversion.ui_expression])
            main()
        else:
            print('Unknown variable')
            main()
    else:
        # arrange_expression()
        check_expression()


def check_expression():
    if re.findall(r"\*\*", conversion.ui_expression) or re.findall(r"//", conversion.ui_expression) or \
            re.findall(r"\^\^", conversion.ui_expression):
        print('Invalid expression')
        main()
    elif conversion.ui_expression.count('(') != conversion.ui_expression.count(')'):
        print('Invalid expression')
        main()
    else:
        arrange_expression()


def arrange_expression():
    operand_str = ''
    expression_list = []

    for i in conversion.ui_expression:
        if i in conversion.assignment_dict.keys():
            operand_str += conversion.assignment_dict[i]

        elif i.isalnum():
            operand_str += i

        elif not i.isalnum():
            expression_list.append(operand_str)
            expression_list.append(i)
            operand_str = ''

    while "" in expression_list:
        expression_list.remove("")

    if len(expression_list) < len(conversion.ui_expression):
        expression_list.append(operand_str)

    while "" in expression_list:
        expression_list.remove("")

    setattr(conversion, 'infix_notation', expression_list)
    conversion_process()


def conversion_process():
    for i in conversion.infix_notation:
        # 1. Add operands (numbers and variables) to the result (postfix_notation) as they arrive.
        if i.isalnum():
            conversion.postfix_notation.append(i)

        # 2. If the operator_stack is empty or contains a left parenthesis on top, push the incoming operator on the
        # operator_stack
        elif len(conversion.operator_stack) == 0 or conversion.operator_stack[-1] == '(':
            conversion.operator_stack.append(i)

        # 3. If the incoming operator has higher precedence than the top of the operator_stack push it on the
        # operator_stack.
        elif i not in '()' and OPERATOR_PRECEDENCE[i] > OPERATOR_PRECEDENCE[conversion.operator_stack[-1]]:
            conversion.operator_stack.append(i)

        # 4. If the precedence of the incoming operator is lower than or equal to that of the top of the
        # operator_stack, pop the operator_stack and add operators to the result until you see an operator that has
        # smaller precedence or a left parenthesis on the top of the operator_stack; then add the incoming operator to
        # the operator_stack.
        elif i not in '()' and OPERATOR_PRECEDENCE[i] <= OPERATOR_PRECEDENCE[conversion.operator_stack[-1]]:
            while len(conversion.operator_stack) > 0:
                if conversion.operator_stack[-1] != '(' or OPERATOR_PRECEDENCE[i] < \
                        OPERATOR_PRECEDENCE[conversion.operator_stack[-1]]:
                    conversion.postfix_notation.append(conversion.operator_stack.pop())
            conversion.operator_stack.append(i)

        # 5. If the incoming element is a left parenthesis, push it on the operator_stack.
        elif i == '(':
            conversion.operator_stack.append(i)

        # 6. If the incoming element is a right parenthesis, pop the stack and add operators to the result until you
        # see a left parenthesis. Discard the pair of parentheses.
        elif i == ')':
            while conversion.operator_stack[-1] != '(':
                conversion.postfix_notation.append(conversion.operator_stack.pop())
            conversion.operator_stack.pop()

        # 7. At the end of the expression, pop the operator_stack and add all operators to the result.
    while conversion.operator_stack:
        conversion.postfix_notation.append(conversion.operator_stack.pop())
    calculate_result()


def calculate_result():
    for i in conversion.postfix_notation:
        # If the incoming element is a number, push it into the stack (the whole number, not a single digit!).
        if i.isnumeric():
            conversion.calculating_stack.append(i)

        # If the incoming element is an operator, then pop twice to get two numbers and perform the operation;
        # push the result on the stack.
        elif i in '+-*/' and len(conversion.calculating_stack) > 1:
            a = conversion.calculating_stack.pop()
            b = conversion.calculating_stack.pop()
            result = (eval(f'{int(b)}{i}{int(a)}'))
            conversion.calculating_stack.append(result)
        elif i == '^' and len(conversion.calculating_stack) >= 1:
            a = conversion.calculating_stack.pop()
            b = conversion.calculating_stack.pop()
            conversion.calculating_stack.append(pow(int(b), int(a)))

    # When the expression ends, the number on the top of the stack is a final result.
    print(conversion.calculating_stack[-1])
    main()


if __name__ == "__main__":
    main()
