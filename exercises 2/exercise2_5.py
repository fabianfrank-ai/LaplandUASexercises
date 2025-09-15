#import module to generate pseudo-random numbers
import random

#create random int between 1 and 10 as random number
random_number = random.randint(1,10)

#create random ints between 2 and 5 for the sides of the rectangle
random_side1 = random.randint(2,5)
random_side2 = random.randint(2,5)

#calculate the area of the rectangle with the given values
area_rectangle = random_side1*random_side2

#print the values which were generated/calculated above
print(f'Random Number: {random_number}')
print(f'First Random Side: {random_side1}')
print(f'Second Random Side: {random_side2}')
print(f'Area Rectangle: {area_rectangle} m2 ')
