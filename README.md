![Intro scenery: the pencil ticking the last box on the planner page while the red cover comes down over the finished list, the highlighted row above the tick and looping pencil scribbles standing in for the entries](intro-banner.png)


# Task-Manager

![Wordmark banner: an open paper planner on a wooden desk, its left page ruled with rows of empty checkbox squares and looping pencil scribbles for entries, one row swept with yellow highlighter as the next due, the red spiral binding at the centre and a faint calendar grid on the right page](banner.png)

<p align="center"><img src="logo.png" alt="Task-Manager logo: a white spiral planner page seen from above, a column of empty pencil checkbox squares down the left margin with the first box ticked and the red spiral binding along the left edge" width="200"></p>

![Animated scene](scene.svg)

# Task-Manager

A minimal interactive task manager in Python, in a single file, using only
the standard library. Tasks live in an in-memory list for the duration of
the session; nothing is saved to disk, so the list resets when you quit.

## Run

```bash
python3 task-manager.py
```

The program starts with two built-in example tasks (`walk dog`, due in
2 days and marked completed, and `Eat tree`, due in 30 days and not
completed) and then shows a menu:

```text
1. ADD       add a task, with a description and whole days until it is due
2. COMPLETE  mark a task completed by its exact, case-sensitive name
3. PRINT     list all tasks with their status and days remaining
4. REMOVE    remove every completed task from the list
5. RANDOM    print one task chosen at random
6. NEXT      print the task with the fewest days remaining
7. QUIT      exit
```

![Separator](sep-heavy.svg)

## Behaviour verified by testing

- The menu accepts only a whole number from 1 to 7. Anything else (text,
  an empty line, `3.5`, 0, 99, -1) prints
  `Please enter a number from 1 to 7.` and shows the menu again, with no
  traceback.
- Closing the input (EOF, for example Ctrl-D) or pressing Ctrl-C at
  the menu or at any sub-prompt prints `Bye! Bye!` and exits with
  status 0, with no traceback.
- ADD rejects a non-numeric days value, a negative days value, and a
  blank description, each with an explanation, and does not add the
  task. After a successful add, the new task is printed in the same
  readable format PRINT uses.
- COMPLETE reports what it did: `Marked completed: <name>` when the
  name matched (every task with that exact name is marked), and a
  `No task named ... found` message when it matched nothing, so a
  typo no longer looks like success.
- REMOVE really removes: completed tasks are gone from a following PRINT,
  and only uncompleted tasks remain. The list is printed before and after
  the removal.
- NEXT compares days as numbers, so a task due in 2 days is chosen ahead
  of one due in 100 days.
- RANDOM prints just the chosen task (no stray `None` line).
- NEXT and RANDOM on an empty list (reachable after completing and
  removing every task) print a short no-tasks message instead of crashing.
- Days and completion status are stored as integers throughout. The
  `task` class methods behave accordingly: `task_due()` reports a task
  with 0 or fewer days as due, and `day_passed()` reduces the days
  remaining by one.

![Separator](sep-light.svg)

## Tests

```bash
python3 -m unittest
```

19 tests: the `task` class on its own (string fields stored as ints,
due checks, `day_passed`, removal mutating the caller's list) and
scripted menu runs (add, complete, remove, next, quit, bad input,
EOF, and a simulated Ctrl-C).

![Separator](sep-heavy.svg)

## Files

- `task-manager.py` - the whole program, including the `task` class and
  the menu loop
- `test_task_manager.py` - the test suite
- `LICENSE` - GNU General Public License v3

![Separator](sep-heavy.svg)

> **Landing list:** Every session opens with walk dog, due in 2 days and already completed, and Eat tree, due in 30 days and not completed. Quitting erases the list, because nothing is saved to disk.
