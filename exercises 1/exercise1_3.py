#User input for the length of a trip
trip_length = input("Enter the length of trip in kilometers: \n")

#using try.....except in case user input is not a number
try:
   #convert the user input to int if possible
   trip_length = int(trip_length)

   #calculate the consumed fuel with given values of 6,5l/100km
   consumed_fuel = trip_length * (6.5 / 100)

   #round the consumed fuel up to one decimal
   rounded_fuel = round(consumed_fuel,1)

   #return the used fuel during the trip
   print(f'Overall about {rounded_fuel} liters were used.')


except ValueError:
    #return error message to the user if e.g. letters or unknown symbols were used
    print("Error. No valid number was detected.Please try again.")
