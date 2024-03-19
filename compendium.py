# Author: Tommy Nguyen
# GitHub: TommyTegra
# Description: A command-line interface (CLI) that allows the user to
#       get compendium entries from the two Legend of Zelda games:
#       Breath of the Wild, and Tears of the Kingdom.

import requests
import typer
from InquirerPy import inquirer
import pyfiglet
import zmq
from PIL import Image
from io import BytesIO

# ZeroMQ object
obj = zmq.Context()
socket = obj.socket(zmq.REQ)

# Connect to Microservice server
socket.connect("tcp://localhost:5555")


def home():
    """
    Home page which allows for game version selection.
    """
    title_art = pyfiglet.figlet_format("ZELDA", font="stop")
    subtitle_art = pyfiglet.figlet_format("Compendium", font="stforek")
    print('-------------------------------------------------'
          '-------------------------------------------------')
    print(title_art)
    print(subtitle_art)
    print('--------------------------------------------------'
          '--------------------------------------------------')
    print('Welcome! This program allows you to find compendium '
          'entries in either Breath of the Wild, or Tears of Kingdom.\n')
    print('Please use arrow keys to navigate.')
    game_choice = inquirer.select(
        message='Select a game version (enter to confirm):',
        choices=[
            'Breath of the Wild (BOTW)',
            'Tears of the Kingdom (TOTK)',
            'Exit (closes program)'
        ],
    ).execute()
    game_ver = None
    if game_choice == 'Breath of the Wild (BOTW)':
        game_ver = (1, 'BOTW')
    elif game_choice == 'Tears of the Kingdom (TOTK)':
        game_ver = (2, 'TOTK')
    else:
        quit()

    print(f'You have selected: {game_choice}.')
    print(f'({game_ver[1]}) The beginning of prompts will indicate this.')
    task_selection(game_ver)


def task_selection(game_ver):
    """
    Task selection page. Allows the user to select which service to
    execute.
    """
    print('--------------------------------------------------'
          '--------------------------------------------------')
    task_choice = inquirer.select(
        message=f'({game_ver[1]}) Please select a service: ',
        choices=[
            'ID Lookup (requires exact number)\n        -Enter an ID number to get entry',
            'Name Lookup (requires exact full name)\n        -Enter name to get entry',
            'Explore Categories (browse manually)\n        '
            '-Lists names of all entries within a selected category',
            'Get random compendium entry',
            'Back (to home page)',
            'Exit (closes program)'
        ],
    ).execute()
    if task_choice == 'ID Lookup (requires exact number)\n        -Enter an ID number to get entry':
        id_lookup(game_ver)
    elif task_choice == 'Name Lookup (requires exact full name)\n        -Enter name to get entry':
        name_lookup(game_ver)
    elif task_choice == 'Explore Categories (browse manually)\n        ' \
                        '-Lists names of all entries within a selected category':
        explore_cat(game_ver)
    elif task_choice == 'Get random compendium entry':
        random_entry(game_ver)
    elif task_choice == 'Back (to home page)':
        home()
    else:
        quit()


def id_lookup(game_ver):
    """
    ID Lookup page. Prompts the user to enter the ID number
    of the entry for lookup.
    """
    print('--------------------------------------------------'
          '--------------------------------------------------')
    print(f'({game_ver[1]}) ID Lookup: ')
    print('You may use Ctrl + Z for alternate choices.\n')
    id_num = inquirer.number(
        message='Please enter an ID number: ',
        default=None,
        mandatory=False
    ).execute()
    results = requests.get(f'https://botw-compendium.herokuapp.com/api/v3/compendium/entry/{id_num}?game={game_ver[0]}')
    entry = results.json()
    if not entry["data"]:
        id_num = None
    if id_num is not None:
        result(game_ver, id_num)
    alt_choice = inquirer.select(
        message='Invalid input or input cancelled.',
        choices=[
            'Retry ID input',
            'Try name input',
            'Manually search (go to explore)',
            'Back (to task selection)',
            'Start over (to home page)',
            'Exit (close program)'
        ],
    ).execute()
    if alt_choice == 'Retry ID input':
        id_lookup(game_ver)
    elif alt_choice == 'Try name input':
        name_lookup(game_ver)
    elif alt_choice == 'Manually search (go to explore)':
        explore_cat(game_ver)
    elif alt_choice == 'Back (to task selection)':
        task_selection(game_ver)
    elif alt_choice == 'Start over (to home page)':
        home()
    else:
        quit()


def name_lookup(game_ver):
    """
    Name lookup page. Prompts the user for a string which is the name
    of the potential entry. Will return entry on valid input, give
    alternate choices otherwise.
    """
    print('--------------------------------------------------'
          '--------------------------------------------------')
    print(f'({game_ver[1]}) Name Lookup: ')
    print('You may use Ctrl + Z for alternate choices.\n')
    id_num = inquirer.text(
        message='Please enter an ID number: ',
        default="",
        mandatory=False
    ).execute()
    results = requests.get(f'https://botw-compendium.herokuapp.com/api/v3/compendium/entry/{id_num}?game={game_ver[0]}')
    entry = results.json()
    if not entry["data"]:
        id_num = ""
    if id_num != "":
        result(game_ver, id_num)
    alt_choice = inquirer.select(
        message='Invalid input or input cancelled.',
        choices=[
            'Retry name input',
            'Try ID input',
            'Manually search (go to explore)',
            'Back (to task selection)',
            'Start over (to home page)',
            'Exit (close program)'
        ],
    ).execute()
    if alt_choice == "Retry name input":
        name_lookup(game_ver)
    if alt_choice == 'Try ID input':
        id_lookup(game_ver)
    elif alt_choice == 'Manually search (go to explore)':
        explore_cat(game_ver)
    elif alt_choice == 'Back (to task selection)':
        task_selection(game_ver)
    elif alt_choice == 'Start over (to home page)':
        home()
    else:
        quit()



def explore_cat(game_ver):
    """
    Explore categories page. Allows users to select a category which will list
    all the entries within that category.
    """
    print('--------------------------------------------------'
          '--------------------------------------------------')
    print(f'({game_ver[1]}) Explore: \n'
          f'This will list the names of all entries within the category.\n')
    cat_choice = inquirer.select(
        message='Please select a category: ',
        choices=[
            'Creatures',
            'Equipment',
            'Materials',
            'Monsters',
            'Treasure',
            'Cancel (go to task selection)'
        ],
    ).execute()
    if cat_choice == 'Cancel (go to task selection)':
        task_selection(game_ver)
    print(f'{cat_choice}: ')
    name = cat_choice.lower()
    category = requests.get(f'https://botw-compendium.herokuapp.com/api/v3/compendium/category/{name}?game={game_ver[0]}')
    entry = category.json()
    data = entry['data']
    entry_list = []
    for item in data:
        entry_list.append((item['id'], item['name']))
    entry_list.sort()
    for entity in entry_list:
        print(f'ID: {entity[0]}, Name: {entity[1]}')
    print('Finished.')
    finish_choice = inquirer.select(
        message='Would you like to: ',
        choices=[
            'Explore again (go back)',
            'Choose another service (go to task selection)',
            'Start over (go to home)',
            'Exit (close program)'
        ],
    ).execute()
    if finish_choice == 'Explore again (go back)':
        explore_cat(game_ver)
    elif finish_choice == 'Choose another service (go to task selection)':
        task_selection(game_ver)
    elif finish_choice == 'Start over (go to home)':
        home()
    else:
        quit()


def random_entry(game_ver):
    """
    Gets a random entry from the compendium. Call microservice for
    random ID number.
    """
    print('--------------------------------------------------'
          '--------------------------------------------------')
    ms_msg = str(game_ver).encode()
    socket.send(ms_msg)
    receive = socket.recv()
    rand_id = receive.decode()
    confirm_choice = inquirer.select(
        message='This will give you a random entry.\n Confirm?',
        choices=[
            "Yes",
            "No (to task selection)",
            "Start over (to home page)",
            "Exit (close program)"
        ],
    ).execute()
    if confirm_choice == "Yes":
        result(game_ver, rand_id)
    elif confirm_choice == "No (to task selection)":
        task_selection(game_ver)
    elif confirm_choice == "Start over (to home page)":
        home()
    else:
        quit()


def result(game_ver, id_num):
    """
    Results page. Prints the ID number, name, and the description.
    """
    print('--------------------------------------------------'
          '--------------------------------------------------')
    results = requests.get(f'https://botw-compendium.herokuapp.com/api/v3/compendium/entry/{id_num}?game={game_ver[0]}')
    entry = results.json()
    data = entry['data']
    print(f'({game_ver[1]}) Results: \n'
          f'ID number: {data["id"]} \n'
          f'Name: {data["name"]} \n'
          f'Description: {data["description"]}\n')

    if game_ver[0] == 1:
        image_choice = inquirer.select(
            message='Do you want the image?',
            choices=[
                'I want the image.',
                'I do not want the image.'
            ],
        ).execute()
        if image_choice == 'I want the image.':
            confirm = inquirer.confirm(
                message="Are you sure? It will open the image in a new window."
            ).execute()
            if confirm:
                get_image(id_num)

    whole_entry(game_ver, data)


def whole_entry(game_ver, data):
    """
    Inquires about getting the entire entry information.
    """

    all_choice = inquirer.select(
        message='Do you want the whole available entry?',
        choices=[
            "I want the whole entry.",
            "I do not."
        ],
    ).execute()
    if all_choice == "I want the whole entry.":
        confirm = inquirer.confirm(
            message="Are you sure? It will printed with its original formatting"
                    "and with all of its available details."
        ).execute()
        if confirm:
            print(data)
    alt_choice = inquirer.select(
        message='Would you like to: ',
        choices=[
            'Choose another service (to task selection)',
            'Start over (to home page)',
            'Exit (close program)'
        ],
    ).execute()
    if alt_choice == 'Choose another service (to task selection)':
        task_selection(game_ver)
    elif alt_choice == 'Start over (to home page)':
        home()
    else:
        quit()


def get_image(id_num):
    """
    Inquires about obtain entry image.
    """
    response = requests.get(f'https://botw-compendium.herokuapp.com/api/v3/compendium/entry/{id_num}/image')
    # Open the image using PIL
    image = Image.open(BytesIO(response.content))

    # Display the image
    image.show()
    return


if __name__ == '__main__':
    typer.run(home)


