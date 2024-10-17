import numpy as np
import matplotlib.pyplot as plt
#Author: Bhargav Ashok

# Parameters
num_passengers = 7000 #passengers per flight (used as sample size from a Delta Boeing 737 with passengers and staff multiplied by arrivals per day/24)
arrivals = 6 # average number of passengers arriving per minute
check_in = 9 # passengers served per minute at check-in
security = 7 # passengers served per minute at security
boarding = 5 # passengers boarded per minute


#Data taken from and approximated using: https://www.atl.com/about-atl/atl-factsheet/
#Data also taken from and estimated using: https://www.atl.com/times/
#Research: https://www.delta.com/us/en/aircraft/boeing/737-800
# Research: https://www.georgiaencyclopedia.org/articles/business-economy/
#Research: https://simpleflying.com/aircraft-flight-crew-requirements/
#estimation of rates based on research and personal experience


# Initialize/set-up variables
np.random.seed(42)
inter_arrival_times = np.random.exponential(1/arrivals, num_passengers)
arrival_times = np.cumsum(inter_arrival_times)


# Check-in
check_in_times = np.zeros(num_passengers)
start_check_in = np.zeros_like(arrival_times)
end_check_in = np.zeros_like(arrival_times)


for i in range(num_passengers):
   if i == 0:
       start_check_in[i] = arrival_times[i]
   else:
       start_check_in[i] = max(arrival_times[i], end_check_in[i - 1])
# used to loop through each passenger when they arrived and started their check-in by waiting for other passengers ahead to finish.


   check_in_times[i] = np.random.exponential(1 / check_in)
   end_check_in[i] = start_check_in[i] + check_in_times[i]


# Security
security_times = np.zeros(num_passengers)
start_security = np.zeros_like(arrival_times)
end_security = np.zeros_like(arrival_times)


for i in range(num_passengers):
   start_security[i] = max(end_check_in[i], end_security[i - 1] if i > 0 else 0)
# used to loop through each passenger when they have ended check_in and started security after the previous passenger ends, as each passenger is added, the queue cycles through loop
   security_times[i] = np.random.exponential(1 / security)
   end_security[i] = start_security[i] + security_times[i]


# Boarding process
boarding_times = np.zeros(num_passengers)
start_boarding = np.zeros_like(arrival_times)
end_boarding = np.zeros_like(arrival_times)


for i in range(num_passengers):
   start_boarding[i] = max(end_security[i], end_boarding[i - 1] if i > 0 else 0)
# used to loop through each passenger when they have ended security and started boarding after the previous passenger enters boarding
 
   boarding_times[i] = np.random.exponential(1 / boarding)
   end_boarding[i] = start_boarding[i] + boarding_times[i]


# Calculate times for each checkpoint
total_waiting_times = (start_check_in - arrival_times) + (start_security - end_check_in) + (start_boarding - end_security)
average_waiting_time = np.mean(total_waiting_times)
total_times_in_airport = end_boarding - arrival_times
average_time_in_airport = np.mean(total_times_in_airport)




print(f"Average Waiting Time: {average_waiting_time:.2f} minutes")
print(f"Average Total Time in Airport: {average_time_in_airport:.2f} minutes")




plt.figure(figsize=(12, 8))
plt.hist(total_times_in_airport, bins=30, edgecolor='black')
plt.xlabel('Total Time in Airport (minutes)')
plt.ylabel('Number of Passengers per arrival flight')
plt.title('Distribution of Total Time Spent Flying Delta in Atlanta Airport')
plt.grid(True)
plt.show()


