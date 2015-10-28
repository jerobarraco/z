a new operator that leverages the fact that idiv usually produces output for div and mod

#this sucks i dont like hiding operators as "functions"
a = divmod(10,3)


q, m = 10/3
- could be, though multiple return value is something i haven't planned yet


10/3:q, m
- breaks everything