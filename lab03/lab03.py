from operator import add, mul

square = lambda x: x * x

identity = lambda x: x

triple = lambda x: 3 * x

increment = lambda x: x + 1


def ordered_digits(x):
    """Return True if the (base 10) digits of X>0 are in non-decreasing
    order, and False otherwise.

    >>> ordered_digits(5)
    True
    >>> ordered_digits(11)
    True
    >>> ordered_digits(127)
    True
    >>> ordered_digits(1357)
    True
    >>> ordered_digits(21)
    False
    >>> result = ordered_digits(1375) # Return, don't print
    >>> result
    False

    """
    ret = True
    while x > 0:
        digit = x%10
        x //= 10
        if digit < x%10:
            ret = False
    return ret


def get_k_run_starter(n, k):
    """Returns the 0th digit of the kth increasing run within n.
    >>> get_k_run_starter(123444345, 0) # example from description
    3
    >>> get_k_run_starter(123444345, 1)
    4
    >>> get_k_run_starter(123444345, 2)
    4
    >>> get_k_run_starter(123444345, 3)
    1
    >>> get_k_run_starter(123412341234, 1)
    1
    >>> get_k_run_starter(1234234534564567, 0)
    4
    >>> get_k_run_starter(1234234534564567, 1)
    3
    >>> get_k_run_starter(1234234534564567, 2)
    2
    """
    for i in range(0, k+1):
        while n%10 > (n//10)%10 and n > 9:
            n //= 10
        if(i == k):
            return n % 10
        else:
            n //= 10


def make_repeater(func, n):
    """Return the function that computes the nth application of func.

    >>> add_three = make_repeater(increment, 3)
    >>> add_three(5)
    8
    >>> make_repeater(triple, 5)(1) # 3 * 3 * 3 * 3 * 3 * 1
    243
    >>> make_repeater(square, 2)(5) # square(square(5))
    625
    >>> make_repeater(square, 4)(5) # square(square(square(square(5))))
    152587890625
    >>> make_repeater(square, 0)(5) # Yes, it makes sense to apply the function zero times!
    5
    """
    def repeater(x):
        times = n            # n is not in repeater's runtime, but times is assigned when make_repeater called 
        for i in range(0, times):
            x = func(x)
        return x
    return repeater


def composer(func1, func2):
    """Return a function f, such that f(x) = func1(func2(x))."""
    return lambda x: func1(func2(x))


def apply_twice(func):
    """ Return a function that applies func twice.

    func -- a function that takes one argument

    >>> apply_twice(square)(2)
    16
    """
    return make_repeater(func, 2)


def div_by_primes_under(n):
    """
    >>> div_by_primes_under(10)(11)
    False
    >>> div_by_primes_under(10)(121)
    False
    >>> div_by_primes_under(10)(12)
    True
    >>> div_by_primes_under(5)(1)
    False
    """
    checker = lambda x: False
    for i in range(2, n+1):
        if not checker(i):  # i is a prime_under_n, just check x%prime_under_n
            checker = (lambda f, i: lambda x: f(x) or x%i == 0)(checker, i)
    return checker


def div_by_primes_under_no_lambda(n):
    """
    >>> div_by_primes_under_no_lambda(10)(11)
    False
    >>> div_by_primes_under_no_lambda(10)(121)
    False
    >>> div_by_primes_under_no_lambda(10)(12)
    True
    >>> div_by_primes_under_no_lambda(5)(1)
    False
    """
    def checker(x):
        return False
        
    for i in range(2, n+1):
        if not checker(i):
            def outer(f, i):
                def inner(x):
                    return f(x) or x%i == 0
                return inner
            checker = outer(checker, i)

    return checker


def zero(f):
    return lambda x: x


def successor(n):
    return lambda f: lambda x: f(n(f)(x))


def one(f):
    """Church numeral 1: same as successor(zero)(f)"""
    return lambda x: f(x)


def two(f):
    """Church numeral 2: same as successor(successor(zero))(f)"""
    return lambda x: f(f(x))


three = successor(two)


def church_to_int(n):
    """Convert the Church numeral n to a Python integer.

    >>> church_to_int(zero)
    0
    >>> church_to_int(one)
    1
    >>> church_to_int(two)
    2
    >>> church_to_int(three)
    3
    """
    return n(increment)(0)


def add_church(m, n):
    """Return the Church numeral for m + n, for Church numerals m and n.

    >>> church_to_int(add_church(three, three))
    6
    >>> church_to_int(add_church(two, three))
    5
    """
    for i in range(0, church_to_int(n)):
        m = successor(m)
    return m


def mul_church(m, n):
    """Return the Church numeral for m * n, for Church numerals m and n.

    >>> four = successor(three)
    >>> church_to_int(mul_church(two, three))
    6
    >>> church_to_int(mul_church(three, four))
    12
    """
    return composer(m, n)   # n's para is m(m_int times of func), n is n_int times m, so n is m_int*n_int times func


def pow_church(m, n):
    """Return the Church numeral m ** n, for Church numerals m and n.

    >>> church_to_int(pow_church(two, three))
    8
    >>> church_to_int(pow_church(three, two))
    9
    """
    return make_repeater(m, church_to_int(n))
