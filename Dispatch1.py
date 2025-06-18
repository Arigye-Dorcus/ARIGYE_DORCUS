from multipledispatch import dispatch

@dispatch(int, int)
def sum(a, b):
    result= a+b
    print(result)
    
@dispatch(float, float, float)
def sum (w, r, t ):
    result= w+r+t
    print(result)
    
sum(5,7)
sum(1.6,3.4,2.3)   
