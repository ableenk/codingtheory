# Coding theory utilities with python
At the moment you can find the minimum distance of cyclic code with length n and generating polynomial g(x).

## Example 1

### Exercise
Find the minimum distance of cyclic code with length 25 and generating polynomial g(x) = x^4 + x^3 + x^2 + x + 1.

### Code
```
length = 25
generating_polynomial = 'x^4+x^3+x^2+x+1'
code_diameter, multiplier = ct.code_minimum_distance(generating_polynomial, length, log=True)
```

### Printed Solution
```
cyclic code generating polynomial g(x) = x^4 + x^3 + x^2 + x + 1
modulo polynomial P(x) = x^25 + 1
upper bound - 5 with multiplier m(x) = 1
code minimum distance d = 2 with multiplier m(x) = x + 1
