#get the legs via user input
first_leg = input("Give the first leg\n")
second_leg = input("Give the second leg\n")


#check, whether user input is valid
try:
    #convert strings of user input into floats for calculation
    first_leg = float(first_leg)
    second_leg = float(second_leg)

    #calculate hypotenuse with (a**2+b**2)**0.5,  could be replaced by math.sqrt or np.sqrt
    hypotenuse = ((first_leg ** 2) + (second_leg ** 2)) ** 0.5

    #round the hypotenuse
    hypotenuse = round(hypotenuse,2)

    #print the result
    print(f'The hypotenuse is: {hypotenuse}')


except ValueError:
    #return error message to user
    print("Please enter a number. Try again")
