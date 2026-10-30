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
    # Normalise to int: the seed tasks pass strings ("1", "2") while the
    # menu passes ints, and mixing the two broke comparisons below.
    self.Completed_Uncompleted = int(Completed_Uncompleted)
    self.Days = int(Days)

  def __str__(self):
    return "\n Your task is: " + self.Task + "\n Is the task completed or uncompleted (if 1 the task is completed if 0 the task is not completed) \n" + str(self.Completed_Uncompleted) + "\n The amount of days until the task is due is: \n" + str(self.Days)

  def task_due(self):
    if self.Days <= 0:
      return "\n This task is a due task \n"
    else:
      return "\n This task is not due yet get working. \n"

  def day_passed(self):
    self.Days = self.Days - 1
    return "After updation the day passed is now" + str(self.Days)


# The data structure I choose for writing my tasks is: a list, because sometimes when completing a list of tasks, you have duplicate tasks and you need to update the tasks. I also like that lists have specific indexes that correlate to the item number

tasks = [task("walk dog", "1", "2"), task("Eat tree", "0", "30")]

#print(tasks[1])


def countDueTasks(tasks):
  i = 0
  for task in tasks:
    if task.Completed_Uncompleted == 0:
      i = i + 1
  print("You have " + str(i) + " tasks to complete")


#print(countDueTasks(tasks))


def randomTask(tasks):
  if not tasks:
    print("\n There are no tasks to choose from. \n")
    return
  print("\n Random Task selected: \n")
  print(random.choice(tasks))


# This prints information about the random task aswell as the random task
#print(randomTask(tasks))


def firstTask(tasks):
  if not tasks:
    print("\n There are no tasks. \n")
    return
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
    if list.Completed_Uncompleted == 0:
      new_list.append(list)
  # Actually remove the completed tasks from the caller's list; building
  # new_list alone left the original list unchanged.
  tasks[:] = new_list
  print("\n List of tasks after removal: \n")
  for i in new_list:
    print(i)


#removeCompleted(tasks)

while True:
  print("\n Welcome to the task mangement program. \n")
  print("1. ADD" + "\n" + "2. COMPLETE" + "\n" + "3. PRINT" + "\n" + "4. REMOVE" + "\n" + "5. RANDOM" + "\n" + "6. NEXT" + "\n" "7. QUIT")
  try:
    answer = input("\n What would you like to execute? \n")
    try:
      choice = int(answer)
    except ValueError:
      print("\n Please enter a number from 1 to 7. \n")
      continue
    if choice == 1:
      description = input("\n Please specify the description \n")
      time = input("\n please specify the time until completition \n")
      try:
        days = int(time)
      except ValueError:
        print("\n The time until completion must be a whole number of days. Task not added. \n")
        continue
      tasks.append(task(description, 0, days))
      print(tasks[-1])
    elif choice == 2:
        name = input("\n What is the name of your task (case sensitive) \n")
        for i in tasks:
            if i.Task == name:
                i.Completed_Uncompleted = 1
    elif choice == 3:
        print("\n Loading Task Information: \n")
        i = 0
        for x in tasks:
            i = i+1
            print("\n Task Number: \n" + str(i))
            print(x)
    elif choice == 4:
         print("Removing task...")
         removeCompleted(tasks)
    elif choice == 5:
       print("Pulling random task...")
       randomTask(tasks)
    elif choice == 6:
       print("Locating the first task you should complete.")
       firstTask(tasks)
    elif choice == 7:
        print("\n Bye! Bye! \n")
        sys.exit()
    else:
        print("\n Please enter a number from 1 to 7. \n")
  except EOFError:
    print("\n Bye! Bye! \n")
    sys.exit()
      
# Possibly attempt enrichment challenge if we have time later...
    


