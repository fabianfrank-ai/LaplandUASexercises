import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime


#change the style of the plot to dark mode (Hex colors used from ChatGPT)
plt.rcParams.update({
    "figure.facecolor": "#2e2e2e",  
    "axes.facecolor":   "#2e2e2e",
    "axes.edgecolor":   "#cccccc",   
    "axes.labelcolor":  "#ffffff",  
    "xtick.color":      "#dddddd",  
    "ytick.color":      "#dddddd",
    "grid.color":       "#555555",   
    "text.color":       "#ffffff",   
    "figure.edgecolor": "#2e2e2e"
})



#create a plot for a diagram to display the data given
#also create a 3D plot to see the relation between weight, reps and sets
fig=plt.figure()

ax=fig.add_subplot(1,2,1)
ax.grid(True)
ax2=ax.twinx()
ax3=fig.add_subplot(2,2,2, projection='3d')
ax4=fig.add_subplot(2,2,4)
ax4.grid(True)

ax.set_ylabel('Weight')
ax.set_xlabel('Date')

ax2.set_ylabel('Reps')
ax.set_title('Weight and reps over time')

ax3.set_zlabel('Sets')
ax3.set_ylabel('Reps')
ax3.set_xlabel('Weight')
ax3.set_title('3D plot of weight, reps and sets')

ax4.set_ylabel('Volume')
ax4.set_xlabel('Date')
ax4.set_title('Volume over time')   


#connect to the database
conn = sqlite3.connect('training_data.db')
c = conn.cursor()

#fetch the data from the database, data is now a list of dates, weights and reps
c.execute("SELECT date, weight, reps, sets FROM training WHERE exercise = 'Preacher Curls'")
data= c.fetchall()


c.execute("SELECT date, volume FROM volume")
volume_data= c.fetchall()


#get the data from list into separate lists for dates, weights and reps
#Right now the data is still in a list based on entries, so each category needs to be extracted into its own list
#Also convert the date strings into datetime objects for better handling in the plot
dates = [datetime.strptime(row[0], '%d.%m.%Y') for row in data]
weights = [row[1] for row in data]
reps = [row[2] for row in data]
sets = [row[3] for row in data]
date_volumes = [datetime.strptime(row[0], '%d.%m.%Y') for row in volume_data]
volumes = [row[1] for row in volume_data]


#use the data to create a scatter plot
ax.scatter(dates, weights, color='blue', label='Weight')
ax2.scatter(dates, reps, color='hotpink', label='Reps')

#add a line to connect the dots, useful to see the trend
ax.plot(dates, weights, color='blue',linestyle='--')
ax2.plot(dates, reps, color='hotpink',linestyle='--')

#3D plot with weight, reps and sets
ax3.scatter(weights, reps, sets, zdir='z', s=20, c='b', depthshade=True)
ax3.plot(weights, reps, sets, zdir='z', linestyle='--', color='blue')

#Volume plot
ax4.scatter(date_volumes, volumes, color='green', label='Volume')
ax4.plot(date_volumes, volumes, color='green', linestyle='--')
ax4.bar(date_volumes, volumes, color='#01ff00', alpha=0.5, width=6.8)

#add legends to the plot
ax.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.show()