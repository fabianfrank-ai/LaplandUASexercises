###square1

#take the calculation for 2 cherries and devide by 2 to get the value for one cherry
cherry=(2+2*2+2-2-2)*0.5

###square2

#calculate the value of an apple as described by the formula
apple=(((3+10-4)**0.5)/3)+((5**3-5)/20)+3


###square 3

#take the calculation apple-orange=10
#calculate - apple and *-1 for the value of an orange
orange=-(9-apple)

#cherry-3*Banana= 10, cherry was defined at the top
#-cherry and *-1
#divide by 3, as 3 bananas are depicted and calculate the value of one banana
banana=-(10-2*cherry)/3

#3*banana-pear=8
#-3*banana and*-1
pear=-(8-(3*banana))


###square 4

#use the defined variables in this calculation to get the result
result=apple-2*banana+2*orange*(pear+cherry)

print(result)
