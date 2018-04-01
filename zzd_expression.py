# coding: utf-8
import re
ops_rule = {
    u'+': 1,
    u'-': 1,
    u'*': 2,
    u'/': 2
}

def middle_to_after(s):
    expression = []
    ops = []
    s.replace(u' ',u'')
    ss = re.split(u'(\+|\-|\*|\+|\(|\))', s)
    for item in ss:
        if item in [u'+', u'-', u'*', u'/']:
            while len(ops) >= 0:
                if len(ops) == 0:
                    ops.append(item)
                    break
                op = ops.pop()
                if op == u'(' or ops_rule[item] > ops_rule[op]:
                    ops.append(op)
                    ops.append(item)
                    break
                else:
                    expression.append(op)
        elif item == u'(':
            ops.append(item)
        elif item == u')':
            while len(ops) > 0:
                op = ops.pop()
                if op == '(':
                    break
                else:
                    expression.append(op)
        else:
            expression.append(item)

    while len(ops) > 0:
        expression.append(ops.pop())

    return expression

def cal(n1, n2, op):
    if op == u'+':
        return n1 + n2
    if op == u'-':
        return n1 - n2
    if op == u'*':
        return n1 * n2
    if op == u'/':
        return n1 / n2
 
def expression_to_value(expression):
    stack_value = []
    for item in expression:
        if item in [u'+', u'-', u'*', u'/']:
            n2 = stack_value.pop()
            n1 = stack_value.pop()
            result = cal(n1, n2, item)
            stack_value.append(result)
        else:
            stack_value.append(int(item))
    return stack_value[0]
