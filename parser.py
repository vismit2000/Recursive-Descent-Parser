class expr:

    def __init__(self,S,Nd = None):
        if (Nd):
            self.expr = Nd
        else:
            (e,n) = self.parse(S)
            self.expr = e

    class Node:
        def __init__(self,d):
            self.left = None
            self.right = None
            self.data = d

        def toString(self):
            if (self.left and self.right):
                left = self.left.toString()
                right = self.right.toString()
                opr = self.data
                # remove unnecessary 0.0 in sum and 1.0 in multiply
                if(opr == '*' and (left == "0.0" or right == "0.0")):
                    return ""
                if(opr == '*' and (left == "1.0")):
                    return right
                if(opr == '*' and (right == "1.0")):
                    return left
                if(opr == '+' and (left == "0.0")):
                    return right
                if(opr == '+' and (right == "0.0")):
                    return left
                return "(" + left + " " + opr + " " + right + ")"
            else:
                return self.data

    def prettyprint(self):
        s = self.expr.toString()
        print(s)

    def parse(self,S):
        l = len(S)
        
        if (S[0] == "("):
            (left,n) = self.parse(S[1:l-2])
            opr = S[n+1]
            (right,m) = self.parse(S[n+2:l-1])
            expr = self.Node(opr)
            expr.left = left
            expr.right = right
            return (expr,n+m+3)
        
        elif S[0].isdigit():
            i = 0
            while ((i < l) and (S[i].isdigit() or (S[i] == "."))):
                i = i+1
            num = S[0:i]
            expr = self.Node(num)
            return (expr,i)
        
        elif S[0].isalpha():
            i = 0
            while ((i < l) and S[i].isalpha()):
                i = i+1
            var = S[0:i]
            expr = self.Node(var)
            return (expr,i)
        else:
            return Exception("Invalid input")

    def constant(self):
        if self.expr.data[0].isdigit():
            return True
        else:
            return False

    def variable(self):
        if self.expr.data[0].isalpha():
            return True
        else:
            return False

    def samevariable(self,x):
        if (self.expr.data == x):
            return True
        else:
            return False
    
    def exp(self):
        if (self.expr.data == '^'):
            return True
        else:
            return False
        
    def div(self):
        if (self.expr.data == '/'):
            return True
        else:
            return False
        
    def mul(self):
        if (self.expr.data == '*'):
            return True
        else:
            return False
    
    def sum(self):
        if (self.expr.data == '+'):
            return True
        else:
            return False
        
    def sub(self):
        if (self.expr.data == '-'):
            return True
        else:
            return False

    def addend(self):
        left = self.expr.left
        return expr("",left)

    def augend(self):
        right = self.expr.right
        return expr("",right)

    def makeexp(self,e1,e2):
        e = self.Node("^")
        e.left = e1.expr
        e.right = e2.expr
        return expr("",e)
    
    def makediv(self,e1,e2):
        e = self.Node("/")
        e.left = e1.expr
        e.right = e2.expr
        return expr("",e)
    
    def makemul(self,e1,e2):
        e = self.Node("*")
        e.left = e1.expr
        e.right = e2.expr
        return expr("",e)
    
    def makesum(self,e1,e2):
        e = self.Node("+")
        #Original
        #e.left = e1
        #e.right = e2

        #Modified
        e.left = e1.expr
        e.right = e2.expr
        return expr("",e)
    
    def makesub(self,e1,e2):
        e = self.Node("-")
        e.left = e1.expr
        e.right = e2.expr
        return expr("",e)

    def deriv(self,x):
        if self.constant():
            return expr("0.0")
        if self.variable():
            if self.samevariable(x):
                return expr("1.0")
            else:
                return expr("0.0") 
        
        elif self.exp():
            e1 = self.addend()
            e2 = self.augend()
            e3 = expr("1.0")
            return self.makemul(e2,self.makeexp(e1, self.makesub(e2, e3)))
        
        elif self.div():
            e1 = self.addend()
            e2 = self.augend()
            if(e2.expr.data[0].isdigit()):
                return self.makediv(e1.deriv(x), e2)
            return self.makediv(self.makesub(self.makemul(e1.deriv(x),e2),self.makemul(e1,e2.deriv(x))) , self.makemul(e2, e2))
        
        elif self.mul():
            e1 = self.addend()
            e2 = self.augend()
            if(e1.expr.data[0].isdigit()):
                return self.makemul(e1, e2.deriv(x))
            if(e2.expr.data[0].isdigit()):
                return self.makemul(e1.deriv(x), e2)
            return self.makesum(self.makemul(e1,e2.deriv(x)),self.makemul(e1.deriv(x),e2))
        
        elif self.sum():
            e1 = self.addend()
            e2 = self.augend()
            return self.makesum(e1.deriv(x),e2.deriv(x))

        elif self.sub():
            e1 = self.addend()
            e2 = self.augend()
            return self.makesub(e1.deriv(x),e2.deriv(x))

        else:
            raise Exception("DontKnowWhatToDo!")

a = input("Enter an expression: ")
e = expr(a)
e.prettyprint()
f = e.deriv('x')
f.prettyprint()

############## End of program #############################

# Some sample test cases:

# Enter an expression: (4/(x+5))
# (4 / (x + 5))
# (( - 4) / ((x + 5) * (x + 5)))

# Enter an expression: (20*((x^3)+5))
# (20 * ((x ^ 3) + 5))
# (20 * (3 * (x ^ (3 - 1.0))))

# Enter an expression: ((x+4)/(x+5))
# ((x + 4) / (x + 5))
# (((x + 5) - (x + 4)) / ((x + 5) * (x + 5)))

# Enter an expression: (((x^3)-1)/((x*2)-1))
# (((x ^ 3) - 1) / ((x * 2) - 1))
# ((((3 * (x ^ (3 - 1.0))) * ((x * 2) - 1)) - (((x ^ 3) - 1) * 2)) / (((x * 2) - 1) * ((x * 2) - 1)))


