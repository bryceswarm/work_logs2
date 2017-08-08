# Project 4 for Team Treehouse
#
#
#
#
# Author: Bryce Swarm
import os
from collections import OrderedDict

from tasks import Tasks, initialize


# clear the command screen
def clear_screen():
    """ Clears the command screen for next prompts to be displayed
        more efficiently."""
    os.system('cls' if os.name == 'nt' else 'clear')


def new_task(employee_name=None, task_name=None,
             time_elapsed=None, notes=None):
    """Report a new task"""
    if not employee_name:
        employee_name = _get_name()
    if not task_name:
        task_name = _get_task_name()
    if not time_elapsed:
        time_elapsed = _get_time_elapsed()
    if not notes:
        notes = _get_notes()
    Tasks.create(employee_name=employee_name,
                 task_name=task_name,
                 time_elapsed=time_elapsed,
                 notes=notes)
    input('Entry Added. Press any key to continue.')


def _get_name():
    return _prompt_user(prompt='What is your name?').strip()


def _get_time_elapsed():
    while True:
        try:
            time_elapsed = int(_prompt_user(
                prompt='How long (minutes) was spent on the task?').strip())
        except ValueError:
            print('That is not a valid amount of time')
            continue
        else:
            return str(time_elapsed)


def _get_task_name():
    return _prompt_user(prompt='What is the task?').strip()


def _get_notes():
    return _prompt_user(prompt='Any extra notes?').strip()


def _prompt_user(prompt):
    clear_screen()
    print(prompt)
    return input('> ')


def display_task(search_task=None, search_date=None,
                 search_time_spent=None, search_employee=None):
    """View reported tasks"""
    tasks = Tasks.select().order_by(Tasks.timestamp.desc())
    if search_task:
        tasks = tasks.where(Tasks.task_name.contains(search_task)
                            + Tasks.notes.contains(search_task))
    elif search_employee:
        tasks = tasks.where(Tasks.employee_name.contains(search_employee))
    elif search_date:
        tasks = tasks.where(Tasks.date == search_date)
    elif search_time_spent:
        tasks = tasks.where(Tasks.time_elapsed == search_time_spent)

    for task in tasks:
        timestamp = task.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        clear_screen()
        print(timestamp)
        print('=' * len(timestamp))
        print('Task: ' + task.task_name)
        print('Employee: ' + task.employee_name)
        print('Time to complete: ' + task.time_elapsed + ' minutes')
        print('Notes: ' + task.notes)
        print('=' * len(timestamp))
        print('1) Next entry')
        print('2) Delete entry')
        print('3) Return to main menu')
        next_action = input('> ').lower().strip()

        if next_action == '3':
            break
        elif next_action == '2':
            delete_task(task)


def menu_loop():
    """Prompt user with options"""
    menu_select = None
    while menu_select != 'q':
        print('Please make a selection.\n'
              "Enter 'Q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        menu_select = input('> ').lower().strip()
        if menu_select in menu:
            clear_screen()
            menu[menu_select]()


def search_menu_loop():
    """Search for a task record"""
    menu_select = None
    while menu_select != 'q':
        print('Please make a selection.\n'
              "Enter 'Q' to return to main menu.")
        for key, value in search_menu.items():
            print('{}) {}'.format(key, value.__doc__))
        menu_select = input('> ').lower().strip()
        if menu_select in search_menu:
            clear_screen()
            search_menu[menu_select]()


def delete_task(task):
    """Deletes current task"""
    if input('Are you sure? [Y/N]').lower() == 'y':
        task.delete_instance()
        clear_screen()
        input('Entry Deleted. Press any key to continue.')


def _exact_date():
    """Search by exact entry date"""
    clear_screen()
    display_task(search_date=input('Date (MM/DD/YY): '))


def _time_spent():
    """Search by time spent on task"""
    clear_screen()
    display_task(search_time_spent=
                 input('Please enter exact minutes spent: '))


def _task_term():
    """Search by task name or notes"""
    clear_screen()
    display_task(search_task=input('Enter term to search by: '))


def _employee():
    """Search by employee"""
    clear_screen()
    display_task(search_employee=input('Employee Name: '))


menu = OrderedDict([
        ('1', new_task),
        ('2', display_task),
        ('3', search_menu_loop),
])

search_menu = OrderedDict([
        ('1', _exact_date),
        ('2', _task_term),
        ('3', _employee),
        ('4', _time_spent),
])


if __name__ == '__main__':
    initialize()
    menu_loop()
