import numpy as np 

from collections import Counter

def is_polynomial(polynomial: str) -> bool:
    if polynomial == '':
        return False
    symbols = '123456789+- ^x'
    for symbol in polynomial:
        if symbol not in symbols:
            return False
    return True

def is_binary_code(code: str) -> bool:
    if code == '':
        return False
    for symbol in code:
        if symbol not in '01':
            return False
    return True

def get_polynomial_coefs(polynomial: str) -> list[int]:
    monomials = polynomial.replace(' ', '').split('+')
    coefs = dict()
    for monomial in monomials:
        if monomial in ['x', 'x^1']:
            coefs[1] = 1
        elif monomial == '1':
            coefs[0] = 1
        else:
            coef, power = monomial.split('^')
            coefs[int(power)] = 1
    result_coefs = [0]*(max(coefs.keys())+1)
    for power, coef in coefs.items():
        result_coefs[power] = 1
    return result_coefs


def nonzero_binary_codes_with_length_n_generator(n):
    code = [0]*n
    code[-1] = 1
    while True:
        yield code
        if code[-1] == 0:
            code[-1] = 1
        else:
            i = -1
            while i >= -n and code[i] == 1:
                code[i] = 0
                i -= 1
            if i == -n-1:
                code = [0]*n
                i = -1
            code[i] = 1

class BasedException(Exception):
    pass

class BinaryPolynomial(np.polynomial.Polynomial): 
    
    def __str__(self):
        polynomial = ''
        for degree in range(self.coef.shape[0]-1, -1, -1):
            coef = self.coef[degree]
            if isinstance(coef, float):
                coef = round(coef, 3)
            if coef != 0:
                sign = '+' if coef > 0 else '-'
                abs_coef = abs(coef)
                if abs_coef == int(abs_coef):
                    abs_coef = int(abs_coef)
                polynomial += (polynomial != '')*f' {sign} ' +(polynomial == '' and sign == '-')*sign
                if degree == 0:
                    polynomial += str(abs_coef)
                else:
                    polynomial += (abs_coef != 1)*(str(abs_coef)) + 'x' + (degree > 1)*f'^{degree}'
                degree -= 1

        return(polynomial if polynomial != '' else '0')
    
    @property
    def weight(self):
        return self.coef.sum().astype(int)
    

class Code():

    def __init__(self, code, length=None):
        code = code.strip()
        if is_binary_code(code):
            self.polynomial = BinaryPolynomial(list(map(int, list(code)[::-1])))
            self.code = code
            self.length = len(code)
        elif is_polynomial(code):
            coefs = get_polynomial_coefs(code)
            self.polynomial = BinaryPolynomial(coefs)
            self.code = ''.join(list(map(str, coefs[::-1])))
            if length == None:
                raise BasedException()
            self.length = length
    
    def __repr__(self):
        return f'Generating polynomial - {str(self.polynomial)}, length - {self.length}'
    
    def __str__(self):
        return str(self.polynomial)


