i = 0
total = 0
lastoperator = ''
bfirst = 1 
mystr = input()
for str in mystr:
  if str == '=' and bfirst == 0:
    if lastoperator == '+':
      total += int(str1)
    elif lastoperator == '-':
      total -= int(str1)
    elif lastoperator == '*':
      total *= int(str1)
    elif lastoperator == '/':
      total /= int(str1) 
    else:
      pass
    i += 1
  elif str == '+':
    if bfirst == 0: 
      total += int(str1) 
    else: 
      bfirst = 0
    lastoperator = str
  elif str == '-':
    if bfirst == 0: 
      total -= int(str1) 
    else: 
      bfirst = 0
    lastoperator = str
  elif str == '*':
    if bfirst == 0: 
      total *= int(str1) 
    else: 
      bfirst = 0
    lastoperator = str
  elif str == '/':
    if bfirst == 0: 
      total /= int(str1) 
    else: 
      bfirst = 0
    lastoperator = str
  elif str == ' ':
    pass
  else:
    if bfirst == 1:
      total = int(str)
      bfirst = 2
    elif bfirst == 0:
      str1 = str
    else:
      pass
print(total)
