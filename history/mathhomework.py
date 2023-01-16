a=222222222
r=1
while a>10:
   b=a-int(a/10)*10
   a=int(a/10)*4+b
   print(r, a)
   r+=1