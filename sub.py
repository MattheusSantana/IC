def proxSeq (l, n):
   i = len (l) -1
   x = n - 1
   while i >= 0 and l[i] == x: 
      i -= 1
      x -= 1
   if i == -1: return 0
   x = l[i] + 1
   while i < len(l):
   	  l[i] = x
   	  x += 1
   	  i += 1
   return 1

def seq(n, k):
   conte = 0
   if k > n: return print ("erro")

   l = list(range(k))
   array = []
   while proxSeq(l, n) == 1: 
      conte += 1
      array.append(l.copy())
   print(conte)     
   return array