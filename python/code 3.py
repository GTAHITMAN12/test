x=int(input())
def fac(n):
    if(n==0):
        return 1 
    if(n==1):
        return 1
    else:
        return(n*fac(n-1))
def findzero(string):
    count=0
    for cha in reversed(string):
        if cha == '0':
            count=count+1
        else :
            return count
value=str(fac(x))
print(value)
print(findzero(value))
