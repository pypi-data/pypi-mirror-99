# AutoApiTestRunner
Automation Command Line Tool

## Installation
### Method-1: Using https://pypi.org/project/AutoApiTestRunner/1.0.0/

Installation Command:
* pip install AutoApiTestRunner==1.0.0

### Method-2: Using pip

Installation Command:
NOTE: you must have a working git over ssh configuration.

* ssh -T git@github.com
    * “Hi kshamashuttl! You've successfully authenticated, but GitHub does not provide shell access.”
* sudo -H python -m pip install --no-cache-dir "git+ssh://git@github.com/Shuttl-Tech/AutoApiTestRunner.git"

Validate the installation by running
- auto --help

## Configuration
you need to configure it before it can access Drone API.
You are going to need a Drone Token and Drone server URL.
Now head over to https://ci.shuttl.xyz/account, under *Example CLI Usage* section you will see the token and server URL.
Copy both of them and keep them safe.

You can start initialisation process by executing
* auto init

and provide the information on prompt.
* Drone token:your personal token (https://ci.shuttl.xyz/account)
* Drone host:https://ci.shuttl.xyz/
* Full name: Your Name
* Github org [Shuttl-Tech]:Shuttl-Tech


## Trigger API Sanity

* Command:auto runner
    * Repo name:Name of GH repo
    * Branch:Custom branch name