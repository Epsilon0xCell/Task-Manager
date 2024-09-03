# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 14:04:29 2024

@author: cy83r-3x71nc710n
"""

import random
import sys
import os

class task:
  __slots__ = ("Task", "Completed_Uncompleted", "Days")

  def __init__(self, Task, Completed_Uncompleted, Days):
    self.Task = Task
    self.Completed_Uncompleted = Completed_Uncompleted
    self.Days = Days

  def __str__(self):
    return "\n Your task is: " + self.Task + "\n Is the task completed or uncompleted (if 1 the task is completed if 0 the task is not completed) \n" + str(self.Completed_Uncompleted) + "\n The amount of days until the task is due is: \n" + str(self.Days)

  def task_due(self):
    if self.Days <= 0:
      return "\n This task is a due task \n"
    else:
      return "\n This task is not due yet get working. \n"

  def day_passed(self):
    self.Days = self.Days
    return "After updation the day passed is now" + str(self.Days)


# The data structure I choose for writing my tasks is: a list, because sometimes when completing a list of tasks, you have duplicate tasks and you need to update the tasks. I also like that lists have specific indexes that correlate to the item number

tasks = [task("walk dog", "1", "2"), task("Eat tree", "0", "30")]

#print(tasks[1])


def countDueTasks(tasks):
  i = 0
  for task in tasks:
    i = i + 1
  print("You have " + str(i) + " tasks to complete")


#print(countDueTasks(tasks))


def randomTask(tasks):
  print("\n Random Task selected: \n")
  print(random.choice(tasks))


# This prints information about the random task aswell as the random task
#print(randomTask(tasks))


def firstTask(tasks):
  days_list = []
  for list in tasks:
    days_list.append(list.Days)
  least_days = min(days_list)
  for x in tasks:
      if x.Days == least_days:
          print(x)

#print("value executed:")
#firstTask(tasks)
#print("----")

def removeCompleted(tasks):
  new_list = []
  print("\n List of tasks before removal: \n")
  for list in tasks:
    print(list)
    if list.Completed_Uncompleted == "0":
      new_list.append(list)
    for i in new_list:
      print(i)


#removeCompleted(tasks)

while True:
  print("\n Welcome to the task mangement program. \n")
  print("1. ADD" + "\n" + "2. COMPLETE" + "\n" + "3. PRINT" + "\n" + "4. REMOVE" + "\n" + "5. RANDOM" + "\n" + "6. NEXT" + "\n" "7. QUIT")
  answer = input("\n What would you like to execute? \n")
  if int(answer) == 1:
    description = input("\n Please specify the description \n")
    time = input("\n please specify the time until completition \n")
    tasks.append(task(description, 0, time))
    print(tasks)
  elif int(answer) == 2:
      name = input("\n What is the name of your task (case sensitive) \n")
      for i in tasks:
          if i.Task == name:
              i.Completed_Uncompleted = 1
  elif int(answer) == 3:
      print("\n Loading Task Information: \n")
      i = 0
      for x in tasks:
          i = i+1
          print("\n Task Number: \n" + str(i))
          print(x)
  elif int(answer) == 4:
       print("Removing task...")
       removeCompleted(tasks)
  elif int(answer) == 5:
     print("Pulling random task...")
     print(randomTask(tasks))
  elif int(answer) == 6:
     print("Locating the first task you should complete.")
     firstTask(tasks)
  elif int(answer) == 7:
      print("\n Bye! Bye! \n")
      sys.exit()
      
# Possibly attempt enrichment challenge if we have time later...
    


