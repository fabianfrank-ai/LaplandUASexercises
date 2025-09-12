#get the kilometers in urban and non urban areas from the user
kilometers_non_urban=input('Enter kilometers in non-urban areas: ')
kilometers_urban=input('Enter kilometers inside urban areas: ')

#try the code and check for invalid input
try:
    #convert input strings into integers
    kilometers_urban=int(kilometers_urban)
    kilometers_non_urban=int(kilometers_non_urban)

    #calculate the fuel used in urban and outside urban area
    fuel_urban = kilometers_urban * (7.5 / 100)
    fuel_non_urban = kilometers_non_urban * (5.1 / 100)

    #add the values of both consumptions and round them
    fuel_used = fuel_urban + fuel_non_urban
    fuel_used = round(fuel_used, 2)

    #return the result
    print(f'consumption:{fuel_used}')


except ValueError:
    #if ValueError arises: give that message to the user
     print("Please enter a number. Try again")

