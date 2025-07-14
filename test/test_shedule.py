# import schedule
# import time

# # Define a job
# def job():
#     print("Task executed!")

# # Schedule the job
# schedule.every(10).seconds.do(job)  # Runs every 10 seconds
# schedule.every().hour.do(job)       # Runs every hour
# schedule.every().day.at("16:31").do(job)  # Runs daily at 10:30 AM

# # Keep the scheduler running
# while True:
#     schedule.run_pending()
#     time.sleep(1)

import getpass

user = getpass.getuser()
print(user)