value=[1,2,1,3,5,6,4]
temp=0
i=0
def max(i,temp,index):
    if len(value)-1 < i:
        return index
    if temp<value[i] :
        temp=value[i]
        index=i
        return max(i+1,temp,index)  
    else :
        return max(i+1,temp,index)
print(max(0,temp,index=0))
