a = 103

if (int(a*0.5) + a*2)%5:
    rate = (int(a*0.5) + a*2)    
    rate += 5-(int(a*0.5) + a*2)%5
else:    
    rate = (int(a*0.5) + a*2)

print(rate)