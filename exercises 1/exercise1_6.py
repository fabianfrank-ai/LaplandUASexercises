#get the amount of cents by user input
cents = input("How many cents?(1-100)\n")

#try the code and give message if unknown signs(non-numbers or floats were given)
try :
    #convert str into int
    cents = int(cents)


    #check if user input is below 100
    if cents <= 100:
    #check how many of 50,20,10,etc fit into the given amount of cents
    #use % to get the remaining amount of cents and use the remainder in the following steps
    #repeat until all cent pieces are calculated
     fifty_cents=cents // 50
     remaining_cents=cents % 50

     twenty_cents=remaining_cents // 20
     remaining_cents=remaining_cents % 20

     tenth_cents=remaining_cents // 10
     remaining_cents=remaining_cents % 10

     five_cents=remaining_cents // 5
     remaining_cents=remaining_cents % 5

     two_cents=remaining_cents // 2
     remaining_cents=remaining_cents % 2

     one_cents=remaining_cents // 1
     remaining_cents=remaining_cents % 1

    #print the amount of cent pieces used for the user input
     print(f'Amount of 50 cents: {fifty_cents} ')
     print(f'Amount of 20 cents: {twenty_cents} ')
     print(f'Amount of 10 cents: {tenth_cents} ')
     print(f'Amount of 5 cents: {five_cents} ')
     print(f'Amount of 2 cents: {two_cents} ')
     print(f'Amount of 1 cents: {one_cents} ')

    else:
     print("Please enter a number between 1 and 100")


except ValueError:
    print("Something went wrong, try again. Remember to use whole numbers, no fractions or letters.")
