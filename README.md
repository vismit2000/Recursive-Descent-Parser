# Symbolic Differentiation using Recursive Descent Parser
A **recursive descent parser** is a kind of top-down parser built from a set of mutually recursive procedures (or a non-recursive equivalent) where each such procedure implements one of the nonterminals of the grammar. Thus the structure of the resulting program closely mirrors that of the grammar it recognizes.

The program `parser.py` finds the **symbolic differentiation** of the given input expression using recursive descent parsing.

## Problem Statement
![Problem](./Images/Problem_Statement.png?raw=true "Problem")

## Recursive descent
- Simple and general parsing strategy
- [Left-recursion](https://www.gatevidyalay.com/left-recursion-left-recursion-elimination/) must be eliminated first
    - This can be done automatically
    - In practice however, this is done manually. The reason is that we also need to specify semantic actions with the productions used. Hence, people do elimination of left-recursion on their own, and this is not difficult to do.
- Popular strategy in production compilers. e.g., gcc's parser is a hand-written recursive-descent parser.

## Methodology

+ First the line of text (given by the user) is transformed into a tree structure.
+ Then that tree structure is transformed and some calculus is applied to it.
+ Finally the tree structure is transfered back to a textual string which is the required symbolic differentiation.

### Diagrams of the R-D Parse Trees

![R-D Parse Tree](./Images/RDP.png?raw=true "R-D Parse Tree")

## Implementation:

- Example: `5 * x ^ 2 + 6 * x / y - 10 * x ^ 2 * y + 100`
- Transform the input expression into a form that can be manipulated (i.e. a basic **binary tree**).
- In the following example, the equation is reorganized by wrapping it in parentheses `()`. When a change is made, square brackets `[]` are used to highlight what has changed. The basic structure is this:

    `(operation left-operand right-operand)`

- For example, (+ 5 7) means add five and seven. This is the basis of our binary tree.
 
```
Given

  5 * x ^ 2 + 6 * x / y - 10 * x ^ 2 * y + 100

First, handle exponents, left to right

  5 * x ^ 2 + 6 * x / y - 10 * x ^ 2 * y + 100
        ↑  

  5 * [^ x 2] + 6 * x / y - 10 * x ^ 2 * y + 100
                                   ↑

  5 * (^ x 2) + 6 * x / y - 10 * [^ x 2] * y + 100

Next, handle multiplication and division, left to right

  5 * (^ x 2) + 6 * x / y - 10 * (^ x 2) * y + 100
    ↑

  [* 5 (^ x 2)] + 6 * x / y - 10 * (^ x 2) * y + 100
                    ↑

  (* 5 (^ x 2)) + [* 6 x] / y - 10 * (^ x 2) * y + 100
                          ↑

  (* 5 (^ x 2)) + [/ (* 6 x) y] - 10 * (^ x 2) * y + 100
                                     ↑

  (* 5 (^ x 2)) + (/ (* 6 x) y) - [* 10 (^ x 2)] * y + 100
                                                 ↑

  (* 5 (^ x 2)) + (/ (* 6 x) y) - [* (* 10 (^ x 2)) y] + 100

Finally, handle addition and subtraction, left to right

  (* 5 (^ x 2)) + (/ (* 6 x) y) - (* (* 10 (^ x 2)) y) + 100
                ↑

  [+ (* 5 (^ x 2)) (/ (* 6 x) y)] - (* (* 10 (^ x 2)) y) + 100
                                  ↑

  [- (+ (* 5 (^ x 2)) (/ (* 6 x) y)) (* (* 10 (^ x 2)) y)] + 100
                                                           ↑

  [+ (- (+ (* 5 (^ x 2)) (/ (* 6 x) y)) (* (* 10 (^ x 2)) y)) 100]

```
- Order of operation: 
```
(+ 
   (- 
      (+ 
         (* 
            5 
            (^ x 2)) 
         (/ 
            (* 6 x) 
            y)) 
      (* 
         (* 
            10 
            (^ x 2)) 
         y)) 
   100)
```
The outermost operation is an addition, which is applied after evaluating both operands.

## Running the program 

- Run the python file (one with.py extension) using the following command
```python3
python3 parser.py
```
- Enter the input expression (without any spaces) on prompt.

## References :
- http://www.cs.utsa.edu/~wagner/CS3723/rdparse/rdparser6.html
- https://www.cse.iitd.ernet.in/~sbansal/col728/lec/parsing.html
- https://en.wikipedia.org/wiki/Recursive_descent_parser
- https://www.geeksforgeeks.org/recursive-descent-parser/
