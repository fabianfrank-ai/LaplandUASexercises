#ask the user what number he intends to use
user_input_price = input("Please insert the price of the product in Euros\n")


#check whether the user inserted a valid value
try:
    # return the user input, calculate price with VAT and print to user
    price_with_VAT = float(user_input_price) * 1.255
    print(f'Your selected price is:  {user_input_price} €')
    print(f'Price with VAT: {price_with_VAT} € ')


except ValueError:
    #if no number was detected, show error
    print("Error. No number was detected")






