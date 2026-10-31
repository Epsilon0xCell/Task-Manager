# -*- coding: utf-8 -*-
"""A small interactive task manager I keep in one file.

Tasks live in a list in memory for the length of the session and
are gone when the program quits. Nothing is written to disk, so
there is no save file to load, corrupt, or lose.
"""

import random

# I keep a task to three fields and nothing else. The __slots__ line
# pins those names, so a mistyped assignment raises an error instead
# of quietly adding a fourth field that no print or comparison in
# this file would ever read.
class task:
  __slots__ = ("Task", "Completed_Uncompleted", "Days")

  def __init__(self, Task, Completed_Uncompleted, Days):
    self.Task = Task
    # Normalise to int: the seed tasks pass strings ("1", "2") while the
    # menu passes ints, and mixing the two broke comparisons below.
    self.Completed_Uncompleted = int(Completed_Uncompleted)
    self.Days = int(Days)

  # Every task print in this program goes through this one format:
  # PRINT, RANDOM, NEXT, REMOVE, and the print right after ADD. If I
  # change the wording here, all of them change with it.
  def __str__(self):
    return "\n Your task is: " + self.Task + "\n Is the task completed or uncompleted (if 1 the task is completed if 0 the task is not completed) \n" + str(self.Completed_Uncompleted) + "\n The amount of days until the task is due is: \n" + str(self.Days)

  # Zero counts as due, and so does a negative count. day_passed
  # below can push Days under zero, and I would rather a task in
  # that state reads as due than as not due.
  def task_due(self):
    if self.Days <= 0:
      return "\n This task is a due task \n"
    else:
      return "\n This task is not due yet get working. \n"

  # Nothing in the menu calls this method. It belongs to the class
  # itself, and it has no floor: calling it on a task that is
  # already due takes the count further negative instead of
  # stopping at zero.
  def day_passed(self):
    self.Days = self.Days - 1
    return "After updation the day passed is now " + str(self.Days)


# The data structure I choose for writing my tasks is: a list, because sometimes when completing a list of tasks, you have duplicate tasks and you need to update the tasks. I also like that lists have specific indexes that correlate to the item number

tasks = [task("walk dog", "1", "2"), task("Eat tree", "0", "30")]

# The seed tasks pass their numbers as strings. That is the exact
# mix the int conversion in __init__ has to survive on every run,
# because the menu builds its tasks with ints instead.

#print(tasks[1])


# The empty check at the top of this function, and the matching
# one in firstTask below, matter because the empty state is
# reachable in a normal session: complete every task, run
# REMOVE, and the list is empty. random.choice on an empty list
# raises, so I print and return instead.
def randomTask(tasks):
  if not tasks:
    print("\n There are no tasks to choose from. \n")
    return
  print("\n Random Task selected: \n")
  print(random.choice(tasks))


# This prints information about the random task aswell as the random task
#print(randomTask(tasks))


# I collect the day counts first and scan the tasks again for the
# match. A side effect of doing it in two passes: every task tied
# on the fewest days prints, not just the first one I find. With
# the seed tasks only "walk dog" shows, but two added tasks with
# the same day count would both print here.
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
  # I write the kept tasks back into the caller's list with this
  # slice assignment, and the slice is the part that has to be
  # right. Building new_list alone left the original list
  # unchanged, which is why an earlier version of REMOVE printed
  # a shorter list and then removed nothing. Giving the local name
  # a new list would fail the same way: the menu loop would keep
  # holding the old list, and the next PRINT would show the
  # removed tasks still there.
  tasks[:] = new_list
  print("\n List of tasks after removal: \n")
  for i in new_list:
    print(i)


#removeCompleted(tasks)

# The catch around this loop covers the whole menu body, not just
# the menu prompt. Closing the input (EOF, Ctrl-D) or pressing
# Ctrl-C at an ADD or COMPLETE sub-prompt therefore quits the
# whole program with the same Bye message instead of cancelling
# that one action or dying with a traceback. I accept that here
# because there is no saved state to protect. The list lives in
# memory only and is gone either way.
def main():
  while True:
    print("\n Welcome to the task management program. \n")
    print("1. ADD" + "\n" + "2. COMPLETE" + "\n" + "3. PRINT" + "\n" + "4. REMOVE" + "\n" + "5. RANDOM" + "\n" + "6. NEXT" + "\n" "7. QUIT")
    try:
      answer = input("\n What would you like to execute? \n")
      # I parse the number on its own, before any branch runs. Text,
      # an empty line, and 3.5 all land in the except below and go
      # back to the menu, instead of crashing the loop or falling
      # through into a branch they do not belong to.
      try:
        choice = int(answer)
      except ValueError:
        print("\n Please enter a number from 1 to 7. \n")
        continue
      if choice == 1:
        description = input("\n Please specify the description \n")
        time = input("\n please specify the time until completion \n")
        # I refuse a text day count here instead of storing it. A
        # string day count is what broke NEXT in an earlier version,
        # because as text "100" sorts ahead of "2".
        try:
          days = int(time)
        except ValueError:
          print("\n The time until completion must be a whole number of days. Task not added. \n")
          continue
        # A task with no name could never be picked out by COMPLETE,
        # which matches on the exact name, so I refuse a blank one
        # instead of storing a task nothing can reach.
        if not description.strip():
          print("\n The description cannot be blank. Task not added. \n")
          continue
        # A negative count names a due date in the past. Overdue is
        # a state a task reaches as days pass, not a state it starts
        # in, so I refuse it at entry and say why.
        if days < 0:
          print("\n The time until completion cannot be negative. Task not added. \n")
          continue
        # A new task always starts uncompleted. Done is a state a
        # task reaches through COMPLETE, not a state it can start in.
        tasks.append(task(description, 0, days))
        print(tasks[-1])
      elif choice == 2:
          # The match is exact and the loop below never breaks, so
          # two tasks with the same name both get marked completed.
          # The count drives the message after the loop: a name that
          # matched nothing now says so, where it used to print
          # nothing and a typo looked exactly like success.
          name = input("\n What is the name of your task (case sensitive) \n")
          matched = 0
          for i in tasks:
              if i.Task == name:
                  i.Completed_Uncompleted = 1
                  matched += 1
          if matched:
              print("\n Marked completed: " + name + " \n")
          else:
              print("\n No task named '" + name + "' found. Names are case sensitive; run PRINT to see the exact names. \n")
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
          return
      else:
          print("\n Please enter a number from 1 to 7. \n")
    except (EOFError, KeyboardInterrupt):
      print("\n Bye! Bye! \n")
      return


if __name__ == "__main__":
  main()
    


