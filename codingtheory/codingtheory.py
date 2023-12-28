import galois

import numpy as np 

from collections import Counter

def is_polynomial(polynomial: str) -> bool:
    if not isinstance(polynomial, str):
        return False
    if polynomial == '':
        return False
    symbols = '0123456789+- ^x'
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

class BinaryPolynomial(galois.Poly): 

    def __init__(self, coeffs):
        if is_polynomial(coeffs):
            coeffs = get_polynomial_coefs(coeffs)
        
        super().__init__(coeffs, field=galois.GF(2))

    @property
    def weight(self):
        return sum(self.coeffs.tolist())
    
def get_codeword_weight(codeword: galois.Poly | BinaryPolynomial):
    return sum(codeword.coeffs.tolist())

def code_minimum_distance(generating_polynomial, length, log=False):
    modulo_polynomial = 'x^'+str(length)+'+1'

    gen_poly = BinaryPolynomial(generating_polynomial)
    mod_poly = BinaryPolynomial(modulo_polynomial)

    if log:
        print(f"cyclic code generating polynomial g(x) = {gen_poly}")
        print(f"cyclic code length = {length}")

    max_multiplier_degree = length - gen_poly.degree - 1
    codes_generator = nonzero_binary_codes_with_length_n_generator(max_multiplier_degree+1)

    min_codeword_weight = gen_poly.weight
    suitable_multiplier = BinaryPolynomial(next(codes_generator))

    for _ in range(1, 2**max_multiplier_degree-1):
        if min_codeword_weight == 2:
            break

        multiplier_coefs = next(codes_generator)
        multiplier_polynomial = BinaryPolynomial(multiplier_coefs)
        
        codeword = multiplier_polynomial*gen_poly % mod_poly
        codeword_weight = get_codeword_weight(codeword)
        
        if codeword_weight < min_codeword_weight:
            min_codeword_weight = codeword_weight
            suitable_multiplier = multiplier_polynomial
    
    minimum_distance = min_codeword_weight

    if log:
        print(f"code minimum distance d = {minimum_distance} with multiplier m(x) = {str(suitable_multiplier)}")

    return minimum_distance, suitable_multiplier