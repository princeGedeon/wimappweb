def algoeuclide(a,b):
    if  b==0:
        return a
    else:
        r=a%b
        return algoeuclide(b,r)

print(algoeuclide(357,234))