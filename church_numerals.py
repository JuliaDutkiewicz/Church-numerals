#!/usr/bin/env python

# examples of  Church numerals

zero = lambda f: lambda x: x
one = lambda f: lambda x: f(x)
two = lambda f: lambda x: f(f(x))
three = lambda f: lambda x: f(f(f(x)))
four = lambda f: lambda x: f(f(f(f(x))))
five = lambda f: lambda x: f(f(f(f(f(x)))))


def to_intp(f):
    print (f(lambda x: x + 1)(0))


def to_int(f):
    return (f(lambda x: x + 1)(0))


# boolean

TRUE = lambda x: lambda y: x
FALSE = lambda x: lambda y: y

# logic operators

AND = lambda x: lambda y: x(y)(x)
OR = lambda x: lambda y: x(x)(y)
NOT = lambda p: p(FALSE)(TRUE)
XOR = lambda x: lambda y: x(NOT(y))(y)


def to_boolp(f):
    print (f(True)(False))


def to_bool(f):
    return (f(True)(False))


# incrementation n+1

inc = lambda n: lambda f: lambda x: f(n(f)(x))

# decrementation n-1

dec = lambda n: lambda f: lambda x: n(lambda g: lambda h: h(g(f)))(lambda y: x)(lambda y: y)

# addition n+m

add = lambda n: lambda m: m(inc)(n)

# subtraction n-m
sub = lambda n: lambda m: m(dec)(n)

# multiplying n*m

mul = lambda n: lambda m: (m(add(n))(zero))

# exponentiation n^m

pow = lambda n: lambda m: (m(mul(n))(one))

# if f.e. IF(TRUE)(one)(two)->one, IF(FALSE)(one)(two) -> two

IF = lambda n: lambda x: lambda y: n(x)(y)

# checking if the numeral equals ZERO

is_zero = lambda n: n(lambda x: (FALSE))(TRUE)

# checking if  m<=n ?

less_or_equal = lambda m: lambda n: is_zero(sub(m)(n))

# checking if m==n

equal = lambda m: lambda n: AND(less_or_equal(m)(n))(less_or_equal(n)(m))

# Z_combinator is needed for recursion

Z = lambda f: (lambda x: (f(lambda y: x(x)(y))))(lambda x: f(lambda y: (x(x)(y))))

# modulo m%n

mod = Z(lambda f: lambda m: lambda n: IF(less_or_equal(n)(m))(lambda x: f(sub(m)(n))(n)(x))(m))

# pairs

PAIR = lambda x: lambda y: lambda f: f(x)(y)
LEFT = lambda p: p(lambda x: lambda y: x)
RIGHT = lambda p: p(lambda x: lambda y: y)

# list

EMPTY = PAIR(TRUE)(TRUE)
NEW = lambda l: lambda x: PAIR(FALSE)(PAIR(x)(l))
IS_EMPTY = LEFT
FIRST = lambda l: (LEFT(RIGHT(l)))
REST = lambda l: (RIGHT(RIGHT(l)))


def to_int_array(k):
    array = []
    while not to_bool(IS_EMPTY(k)):
        array.append(to_int(FIRST(k)))
        k = REST(k)
    return array


# range(making list of range [m,n])

RANGE = Z(lambda f: lambda m: lambda n: IF(less_or_equal(m)(n))(lambda x: NEW(f(inc(m))(n))(m)(x))(EMPTY))

# fold

FOLD = Z(lambda f: lambda l: lambda x: lambda g: IF(IS_EMPTY(l))(x)(lambda y: g(f(REST(l))(x)(g))(FIRST(l))(y)))

# mapping function on the list

MAP = lambda k: lambda f: FOLD(k)(EMPTY)(lambda l: lambda x: NEW(l)(f(x)))

# gcd

gcd = Z(lambda f: lambda m: lambda n: IF(is_zero(n))(m)(lambda x: f(n)(mod(m)(n))(x)))

# program which for numbers from 1 to 50 puts gcd of this number and 54 in array
ten = mul(two)(five)
fifty = mul(ten)(five)
fifty_four = add(fifty)(four)

list = MAP(RANGE(one)(fifty))(lambda n: gcd(fifty_four)(n))

print(to_int_array(list))