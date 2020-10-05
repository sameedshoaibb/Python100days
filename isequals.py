#!/usr/bin/python3

## They might be looking same, but are they same object? 

a = [1, 2, 4]
b = a
c =list(a)

print(type(a))
print(type(b))
print(type(c))

### Python function arguments (* vs **)

def print_vector(x, y, z):
    print('{}, {}, {}'.format(x,y,z))

>>> gen_expr = [5, 69, 2]
>>> print_vector(gen_expr[0], gen_expr[1], gen_expr[2])
5, 69, 2
>>> print_vector(*gen_expr)
5, 69, 2

