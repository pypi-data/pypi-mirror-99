# 🤖 Qubot

An autonomous exploratory testing library for Python.

### About

Qubot was created out of inspiration to create a fully autonomous testing bot to mimic a real-life
QA-tester.

See [the Qubot paper](docs/qubot_paper.pdf) to learn more about the design decisions and the Q-learning approach behind
this repository. Moreover, see [experiments.ipynb](experiments.ipynb) for the experiment
mentioned in paper.

Hours of painstaking work have been put into this project thus far, and we hope this
library finds actual use in the field of autonomous software testing.

### Getting Started

To get started with Qubot, simply download the library into your project's repository from PyPi:
```
pip install qubot
```

#### Run Programmatically

You can specify each aspect of your test programmatically, and run it all within the same code file.
```
from qubot import Qubot, QubotConfigTerminalInfo, QubotConfigModelParameters, QubotDriverParameters, QubotPresetRewardFunc

qb = Qubot(
    url_to_test="https://upmed-starmen.web.app/",
    terminal_info_testing=QubotConfigTerminalInfo(
        terminal_ids=[],
        terminal_classes=["SignIn_login_hcp__qYuvP"],
        terminal_contains_text=[],
    ),
    terminal_info_training=QubotConfigTerminalInfo(
        terminal_ids=[],
        terminal_classes=[],
        terminal_contains_text=["Log in as a Healthcare Provider"],
    ),
    driver_params=QubotDriverParameters(
        use_cache=True,
        max_urls=10,
    ),
    model_params=QubotConfigModelParameters(
        alpha=0.5,
        gamma=0.6,
        epsilon=1,
        decay=0.01,
        train_episodes=1000,
        test_episodes=100,
        step_limit=100,
    ),
    reward_func=QubotPresetRewardFunc.ENCOURAGE_EXPLORATION,
    input_values={
        "color": "#000000",
        "date": "2021-01-01",
        "datetime-local": "2021-01-01T01:00",
        "email": "johndoe@gmail.com",
        "month": "2021-01",
        "number": "1",
        "password": "p@ssw0rd",
        "search": "query",
        "tel": "123-456-7890",
        "text": "text",
        "time":  "00:00:00.00",
        "url": "https://www.google.com/",
        "week": "2021-W01"
    }
)
qb.run()
print(qb.get_stats())
```

#### Run Programmatically via a Configuration File

Shorten the Qubot setup code by adding a Qubot configuration `JSON` file in the same directory, as follows:

##### qu_config.json
```
{
	"url": "https://upmed-starmen.web.app/",
	"terminal_info": {
		"training": {
            "ids": [],
            "classes": [
                "SignIn_login_hcp__qYuvP"
            ],
            "contains_text": []
		},
		"testing": {
            "ids": [],
            "classes": [],
            "contains_text": [
                "Log in as a Healthcare Provider"
            ]
		}
	},
	"driver_parameters": {
	    "use_cache": false,
	    "max_urls": 1
	},
	"model_parameters": {
		"alpha": 0.5,
		"gamma": 0.6,
		"epsilon": 1,
		"decay": 0.01,
		"train_episodes": 1000,
		"test_episodes": 100,
		"step_limit": 100
	},
	"reward_func": 3,
	"input_values": {
		"color": "#000000",
        "date": "2021-01-01",
        "datetime-local": "2021-01-01T01:00",
        "email": "johndoe@gmail.com",
        "month": "2021-01",
        "number": "1",
        "password": "p@ssw0rd",
        "search": "query",
        "tel": "123-456-7890",
        "text": "text",
        "time":  "00:00:00.00",
        "url": "https://www.google.com/",
        "week": "2021-W01"
	}
}
```

Then, run the following code to set up and execute the Qubot tests.

##### main.py
```
from qubot import Qubot

qb = Qubot.from_file('./qu_config.json')
qb.run()
print(qb.get_stats())
```

#### Run in Command-Line via a Configuration File

To install Qubot for your command line, 

### Authors

<b>Anthony Krivonos</b> <br/>
[Portfolio](https://anthonykrivonos.com) | [GitHub](https://github.com/anthonykrivonos)

<b>Kenneth Chuen</b> <br/>
[Portfolio](https://anthonykrivonos.com) | [GitHub](https://github.com/kenkenchuen)

Created for the [COMSE6156 - Topics in Software Engineering](https://www.coursicle.com/columbia/courses/COMS/E6156/) course at Columbia University
in Spring 2021.
