

def armstrong(x: int) -> bool:
    """
    This function determines whether the number given as input is `Armstrong` or not.
    If a number passes `Armstrong` test this function returns `True` else `False`

    Args: This function takes exactly one argument.

    `x:int` : x should be an integer for calculating the armstrong number.
    """

    m = x
    sum = 0
    temp = x
    count = 0
    while x!=0:
        x//=10
        count = count+1
    for i in range(0, count):
        num =temp%10
        sum = sum + pow(num,count)
        temp//=10
    if sum != m:
        return False
    else:
        return True


def largeSmall(x: list) -> None:
    '''
    Gives `Largest` and `Smallest` number from the list specified by user.
    And prints the largest and smallest number from the user-given list.

    Args: This function takes exactly one argument.

    `x: list` : x should be a list to find a largest and smallest number in the list.
    '''
    largest = smallest = x[0]
    for item in x:
        if item>largest:
            largest = item
            return None

        if item<smallest:
            smallest = item
            return None

    print(f"The largest number is: {largest}")
    print(f'The smallest number is: {smallest}')


def palindromeStr(x: str) -> bool:
    """
    Checks whether a `string` is a `Palindrome` or not.
    After checking returns `True` if a `String` is a `Palindrome` else `False`

    Args: This function takes exactly one argument.

    `x:str` : x should be a string data type for the palindrome test
    """
    
    rev = x[::-1]
    if rev.casefold() == x.casefold():
        return True
    else:
        return False
    

def palindromeNum(x: int) -> bool:
    '''
    Checks whether an `integer number` is a `Palindrome` or not.
    After checking returns `True` if an `Integer Number` is a `Palindrome` else `False`.
    
    This function takes exactly one argument.
    
    Args:

    `x: int` : x should be an integer data type for the palindrome test.
    '''
    temp = x
    sum = ''
    while temp !=0:
        sum = sum + str(temp%10)
        temp = temp//10    
    if int(sum) == x:
        return True
    else:
        return False


def fibonacciSeries(x: int)-> None:
    """
    This function prints the fibonacci series upto `x` terms specified by the user.
    
    Args:
    This function takes exactly one argument.


    `x: int` : x should be an integer which specifies the range upto which the fibonacci series will be generated.
    """
    a= 0
    b=1
    list1 = []
    list1.extend([a,b])
    for i in range(0, x-2):
        c = a+b
        a = b
        b = c
        list1.append(c)

    print("The fibonacci series upto {} is:".format(x))
    print(*list1,sep=", ")
    
    return None


def factorial(x: int)-> int:
    """
    This function returns the `Factorial` value of a number which is specified in the function by user.
    
    This function takes exactly one argument.
    Args:
    `x: int` : x should be an `integer number` for calculating the factorial value of x.
    """
    
    fact = 1
    for i in range(1, x+1):
        fact*=i

    return fact








