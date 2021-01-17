# Gear Optimizer

Gear optimizer for i-rpg.net online game written in Python

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

There are no additional packages needed, only pure Python

### Running

```
python optimizer.py
```

## Equipment csv file

`guild_eq.csv` is a file with all avaliable equipment that a player has access to.  
An example file is attached to this repo. Please use it to keep correct csv format. 

## Distribution

In order to build the project and distribute it as and executable you need `Pyinstaller`:

```
pip install pyinstaller
```

Then to create executable run:

```
pyinstaller optimizer.py
```

That's it! You will find en executable file and all additional files in `dist/optimizer`  
Please attach also `guild_eq.csv` file to the files