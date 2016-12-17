from math import sin, cos, log, exp
from re import sub, match as mch
from functools import reduce
from itertools import starmap

class Function:
    def __init__(self, tpl):
        self.c = tpl[0]     # char
        self.pr = tpl[1]    # prioritet
        self.op_c = tpl[2]  # operands count
        self.dir = tpl[3]   # diriation direct (left(0)||right(1))
        self.func = tpl[4]  # function

    def foo(self, tpl):     # eval function
        return eval('self.func({})'.format(', '.join([str(tpl.pop()) for i in range(self.op_c)][::-1])))

# foo dictionary
fd = {f[0]: Function(f) for f in [\
      ('sin', 4, 1, 0, sin), ('tan', 4, 1, 0, lambda a: sin(a)/cos(a)),
      ('ctan', 4, 1, 0, lambda a: cos(a)/sin(a)), ('sqrt', 4, 1, 0, lambda a: a**0.5),
      ('log', 4, 2, 0, log), ('exp', 4, 1, 0, exp), ('mod', 4, 2, 0, lambda a,b: a%b),
      ('^', 3, 2, 1, lambda a,b: a**b), ('*', 2, 2, 0, lambda a,b: a*b),
      ('/', 2, 2, 0, lambda a,b: a/b), ('+', 1, 2, 0, lambda a,b: a+b),
      ('-', 1, 2, 0, lambda a,b: a-b), ('(', 0, 0, 0, None),
      ('cos', 4, 1, 0, cos), (')', 0, 0, 0, None)
 ]}
fn = fd.keys()  # foo names
cm = {',': '.', ' ': '', '[:÷]': '/', '[•xX×∙∙⋅∗∘·]': '*',   # chars map
        '[―—⎯–‒‐⁃]': '-', '√': 'sqrt', '²': '^2', '³': '^3',
        '¼': '0.25', '½': '0,5', '¾': '0.75', '{': '(', '}': ')'}

strip = lambda l:eval(reduce(lambda a,b:b+a+")",starmap("sub(r'{}','{}',".format,cm.items()),'l')).lower()  # god damn, striper

def converter(l):
    o, st = [], []             # st - stack, o - output
    t = ''                     # tmp buffer for many chars operators and digits

    h = lambda: st[-1]         # head of stack
    p = lambda: st.pop()       # pop top elem
    pr = lambda f: fd[f].pr    # get prioritet
    
    for i, c in enumerate(l):
        if mch('[\w.]', c):    # add char of operand or foo in stack
            t += c
        if (t.isalpha() or  mch('-\d+|\d+', t)) and (mch('[^\w.]', c) or i==len(l)-1):  # push operand or foo in stack
            st.append(t) if t.isalpha() else o.append(float(t))
            t = ''
        if c == '(':        # push open bracket in stack
            st.append(c)
        if c == ')':        # pop operators from stack
            while h() != '(':
                o.append(p())
            p()             # del open bracket from stack
        if c in fn and pr(c):                          # c is operator with prior > 0
            if c == '-' and (i == 0 or l[i-1] == '('): # unary minus
                t = c+t
                continue
            while st and (pr(c)<pr(h()) if fd[c].dir else pr(c)<=pr(h())): # pop operators from stack
                o.append(p())
            st.append(c)    # push operator in stack
    while st:               # pop operators from stack
        o.append(p())
    return o

def calc(arr_l):
    st = []
    for el in arr_l:
        st.append(fd[el].foo(st)) if el in fn else st.append(el)    # eval foo or push operand in stack
    return int(st[0]) if st[0]%1==0 else st[0]

if __name__ == "__main__":
    #print(calc(converter(strip(input('V: ')))))
    ex = ('(4 357 + 38 417) · 201 – 44 + 59 · (1128 – 699)', '261 · 309 + 61542 : 4734 - 2 · 331 - 79497',
        '( 52 ⎯ 34) : 2 * 8 + 7 * 3 ⎯ 13 + ( 64 ⎯ 44 ) : 4', '256 : 32 : 4 · 2 + 256 : (32 : 4 · 2) + 256 : (32 : 4) · 2',
        "625^(-2,25) · 25^(-(2)/(3)) · 125^((25)/(9))", "(3^((5)/(7)) · 5^(-(5)/(7)))/(15^(-1) · 2^((2)/(7)))^(-7)")
    for s in ex:
        l = strip(s)
        print(l)
        l = converter(l)
        print(', '.join([str(int(c) if type(c) is float and c%1==0 else c) for c in l]))
        print(calc(l))
