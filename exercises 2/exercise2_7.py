###AI was used in order to show the instances in which the equation results in 1,2 or 0 solutions
###AI of my choice was ChatGPT
###It was used in order to include instances I have not thought of, it did not provide code


#get the 3 values a, b and c from the user
a = input("Enter a value a\n")
b = input("Enter a value b\n")
c = input("Enter a value c\n")

#try the code first in case of accidental letters
try:
    #convert strings into floats to calculate with them
    a = float(a)
    b = float(b)
    c = float(c)

    #calculate the discriminant in order to evaluate how many solutions there are
    root = b**2-(4*a*c)

    #if the discriminant is smaller than 0 there is no solution, as there are no sqrt of negative numbers
    #a=0 would mean there is no quadratic formula, which is not the purpose of the program, could be added
    if root < 0 or a == 0:
        print("No solutions due to negative root or a=0(a is a prerequisite, please include)")

    #else if the discriminant is equal to 0 there is only one solution, as adding and subtracting 0 makes no difference
    elif root == 0:
        x1 = (- b - (root ** 0.5)) / 2 * a
        print(f'Only one Solution has been found: {x1}')

    #if the discriminant is bigger than 0 there are 2 solutions, which are calculated below
    else:
        x1 = ( - b - ( root ** 0.5)) / 2 * a
        x2 = ( - b + ( root ** 0.5)) / 2 * a
        print(f'Solution 1: {x1}')
        print(f'Solution 2: {x2}')


#in case of letters or signs instead of numbers there will be a message "replacing" the Value Error
except ValueError:
    print("ValueError, try using numbers instead of letters/signs >:(")
