#User input for the desired amount of minutes
minutes_input=input("Enter number of minutes: ")

#try the script, if it fails(e.g. due to string in the input) return error message
try:
    #convert input into int
    minutes_input=int(minutes_input)

    #devide minutes by 60 to get the hours, the remainder are the minutes
    hours=minutes_input // 60
    minutes=minutes_input % 60


    #print the conversion of minutes into hours and minutes
    print(f'{minutes_input} is the equivalent to {hours} hours and {minutes} minutes')

except ValueError:
    #return error message to user if input is in the wrong format 
    print("Error. No number was detected")