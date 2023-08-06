def gcd(a, b): 
    """Method that calculates the greatest common divisor.
    
    Keyword arguments:
    a -- first integer
    b -- second integer
    
    """   
    while (a != 0 and b != 0):
        if a > b:
            a %= b
        else:
            b %= a
    return (a + b)