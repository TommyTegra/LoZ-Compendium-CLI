# LoZ-Compendium-CLI
The Legend of Zelda BOTW &amp; TOTK Compendium CLI

The CLI allows users to find compendium entries from either the Breath of the Wild version, or the Tears of the Kingdom version.

## Operating System
This works and have been developed on Windows 11.

## Required Libraries
InquirePy, PyFiglet, Requests, Typer, Pillow, and ZeroMQ is required as stated in the requirements.txt.

Given that the requirements.txt file is in the current directory, use the 
terminal (or similar) to install all needed dependencies/packages:
```
pip install -r requirements.txt
```

## Required Files
In addition to the required libraries, the repository should be downloaded in 
its entirety to ensure proper functionality. It is much simpler as well.

## Directions/Usage
### Setup
Ensure that Python is installed along with the required libraries, as stated 
above. There are various ways to go about installing the libraries so perform
the installations as you see fit, just ensure that all mentioned are covered 
in the requirements.txt file. Furthermore, ensure that all files in the 
repository are downloaded and in a local directory.

Note: Multiple terminals will be used. Developed on Windows.

### Starting Up the Microservice
To begin, open a terminal in the directory. 

Start the microservice server on this terminal. This can be achieved by:
```commandline
python microservice_server.py
```
In this terminal, the functionality for the random entry lookup is performed.

### Starting Up the Hyrule Compendium CLI
On a different terminal:
```commandline
python compendium.py
```
Note: The application is a Command-Line Interface (CLI) so all further interaction 
will be done through the terminal.

### Using the Application
Instructions for the CLI is provided within the CLI. The CLI is designed to be very 
straightforward, where the program will take the user step-by-step with clear and 
simple instructions. Follow the prompts inside the program to carry out the functions.

### Closing the Application.
The application can be terminated by a KeyboardInterrupt, Ctrl + C or Ctrl + 
Break. The user can also select the "Exit (closes program)" throughout the program.
