import numpy as np



#get 3 sides via user input
side_a=input("Give the first side")
side_b=input("Give the second side")
side_c=input("Give the third side")


#try the code snippet, return error message when unknown numbers detected
try:
    #conversion of sides into float if possible
    side_a = float(side_a)
    side_b = float(side_b)
    side_c = float(side_c)


    #calculate the volume of the box with the given sides
    volume_box=(side_a*side_b*side_c)


    #return the result to the user
    print(f'The Volume for the given box is {volume_box} m3')

except ValueError:
    #if code fails: give user an error message
    print("Please enter a valid number")


#get the radius via user input
radius=input("Give the radius")

#try this snippet also to check vor invalid values
try:
    #conversion of str into floats
    radius=float(radius)

    #calculate the volume of the sphere and round it
    volume_sphere = (4/3) * np.pi* radius**3
    volume_sphere = round(volume_sphere,2)

    #return the volume to the user
    print(f'The Volume for the given sphere is {volume_sphere} m3')

except ValueError:
    #return error message if values invalid
    print("Please enter a valid number")
