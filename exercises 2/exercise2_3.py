#get the salary and tax percentage by the user
salary=input("Your monthly salary")
tax_percentage=input("Your tax percentage in %")

try:
    #convert strings into floats if possible, if not go into except bracket
    salary=float(salary)
    tax_percentage=float(tax_percentage)

    #calculate and round the tax percentage in %
    taxes=salary*tax_percentage/100
    taxes=round(taxes,2)

    #deduct the taxes from the salary and round it
    earnings=salary-taxes
    earnings=round(earnings,2)

    #print it out to the user
    print(f'Earnings:{earnings}')
    print(f'Taxes:{taxes}')


except ValueError:
    #give error if conversion into floats was not possible
    print("Please enter a number. Try again")
