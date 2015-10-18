__author__ = "ChenWei"
import sys

# define operator prio dictionary
prio = { '(' : 5, '^' : 4, '*' : 3, '/' : 3, '+' : 2, '-' : 2,')' : 1, ' ':0}

# stack operation
def push(stackArr,ele):
    stackArr.append(ele)

def pop(stackArr):
    return stackArr.pop()

def peek(stackArr):
    return(stackArr[len(stackArr)-1])

def isEmpty(stackArr):
    if(len(stackArr) == 0):
        return True
    return False
# end

def charPrio(ch):
    """Get element prio"""
    if ch in prio:
        return prio[ch]
    else:
        return -1;

def infixToPostfix(infix):
    """Infix Expression -->> Postfix Expression"""
    postfix = []
    stackArr = []
    scanOperand = False
    hasIntegral = False
    hasDecimal = False
    currentOperand = 0
    decimal = 1
    for ch in infix:
        currentPrio = charPrio(ch)
        if currentPrio < 0: # current ele is operand
            if not (ch.isdigit() or ch == '.'):
                inputError()
                return
            if not scanOperand:
                scanOperand = True
            if ch == '.':
                if not hasIntegral:
                    formatError()
                    return
                hasDecimal = True
                continue
            if hasDecimal:
                if ch == '.':
                    formatError()
                    return
                currentOperand = currentOperand + 0.1 ** decimal * int(ch)
                decimal += 1
            else:
                if not hasIntegral:
                    hasIntegral = True
                currentOperand = currentOperand * 10 + int(ch)
        elif currentPrio == 0:
            # none operation
            pass
        else:
            # and operand into postfix expression
            if scanOperand:
                scanOperand = False
                hasDecimal = False
                hasIntegral = False
                decimal = 1
                postfix.append(currentOperand)
                currentOperand = 0
            # handle operator
            if isEmpty(stackArr):
                push(stackArr, ch) # push into stack
            elif currentPrio > prio[peek(stackArr)]:
                push(stackArr, ch) # push into stack
            elif currentPrio == 1: # ')'
                while (not isEmpty(stackArr)) and currentPrio <= prio[peek(stackArr)]:
                    ele = pop(stackArr)
                    if ele != '(':
                        postfix.append(ele) #pop out of stack, then add into postfix expression
                    else:
                        break
            else:
                while (not isEmpty(stackArr)) and currentPrio <= prio[peek(stackArr)] and prio[peek(stackArr)] < 5 :
                    ele = pop(stackArr)
                    if ele != '(' or ele != ')':
                        postfix.append(ele) #pop out of stack, then add into postfix expression
                push(stackArr, ch) # push into stack
    if scanOperand:
        postfix.append(currentOperand)
    while not isEmpty(stackArr):
        ele = pop(stackArr)
        if ele != '(' or ele != ')':
            postfix.append(ele) #pop out of stack, then add into postfix expression
    return postfix

def formatError():
    print ("FORMAT ERROR")
    return

def valueError():
    print ("VALUE ERROR")
    return

def inputError():
    print ("INPUT ERROR")
    return

def calculate(postfix):
    
    stackOperands = []
    
    for item in postfix:
        currentPrio = charPrio(item)
        if currentPrio < 0:
            push(stackOperands, item)
        else:
            # get two operands
            if isEmpty(stackOperands):
                formatError()
                return
            op2 = pop(stackOperands)
            if isEmpty(stackOperands):
                formatError()
                return
            op1 = pop(stackOperands)
            if item == '^':
                if op2 == 0 and op1 == 0:
                    valueError()
                    return
                push(stackOperands, op1 ** op2)
            elif item == '*':
                push(stackOperands, op1 * op2)
            elif item == '/':
                # VALUE ERROR
                if op2 == 0:
                    valueError()
                    return
                push(stackOperands, float(op1) / float(op2))
            elif item == '+':
                push(stackOperands, op1 + op2)
            elif item == '-':
                push(stackOperands, op1 - op2)
    if isEmpty(stackOperands):
        formatError()
        return
    else:
        result = pop(stackOperands)
        if not isEmpty(stackOperands):
            formatError()
            return
        else:
            formatOutput(result)
            
def isfloat(x):
    try:
        a = float(x)
    except ValueError:
        return False
    else:
        return True

def isint(x):
    try:
        a = int(x)
    except ValueError:
        return False
    else:
        return True
            
def formatOutput(result):
    result = str(result)
    if isint(result):
        print (result)
    elif isfloat(result):
        result = "{0:.10f}".format(float(result))
        print (('%s' % result).rstrip('0').rstrip('.'))
            
# Main Function
inputList = sys.argv
inputList = inputList[1::]
infix = ''.join(inputList)
# get postfix expression
postfix = infixToPostfix(infix)
if postfix is None:
    pass
else:
    calculate(postfix)
