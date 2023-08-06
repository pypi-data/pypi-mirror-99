[![CircleCI](https://circleci.com/gh/duckietown/duckietown-shell.svg?style=shield)](https://circleci.com/gh/duckietown/duckietown-shell) 
[![Docker Hub](https://img.shields.io/docker/pulls/duckietown/duckietown-shell.svg)](https://hub.docker.com/r/duckietown/duckietown-shell/)

# Duckietown Shell

*Duckietown Shell* is a pure Python, easily distributable (few dependencies) utility for Duckietown.

The idea is that most of the functionality is implemented as Docker containers, and `dt-shell` provides a nice interface for that, so that user should not type a very long `docker run` command line.

**Note: Duckietown Shell required Python 3.6 or higher.**
 
## Prerequisites

The duckietown shell has very minimal requirements. 
Please use the links provided and follow the instructions for your OS

1. [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git/)
2. [Git LFS](https://git-lfs.github.com/) (for building and working with the docs only)
2. [Docker](https://docs.docker.com/get-docker/)

## Installing the Duckietown Shell

### Installation on Ubuntu 18.xx or 20.xx

**Note**: This OS is officially supported

Install `pip3`

    $ sudo apt install -y python3-pip
    
Add yourself to the `docker` group:

    $ sudo adduser `whoami` docker

**Note**: you may need to *log in and out* to have the group change take effect.

Install the `duckietown-shell` Python package:

    $ pip3 install --no-cache-dir --user -U duckietown-shell


#### Testing the Installation

Typing 

    $ which dts
    
should output something like: `/home/![user]/.local/bin/dts`

If nothing is output you may need to add `/home/![user]/.local/bin` to your shell path. You can do so by adding the line:

    `export PATH=$PATH:/root/.local/bin`
    
into your `~/.bashrc` file (if you use bash, otherwise the corresponding shell initialization file).

### Installation on Ubuntu 16.xx

The duckietown shell requires python 3.6 or higher, which is not standard on ubuntu16.
A currently working workaround is to install homebrew, by following instructions [here](https://docs.brew.sh/Homebrew-on-Linux). 
Then, run :

    $ brew install python3
    $ python3.7 -m pip install --no-cache-dir --user -U duckietown-shell

Then, typing 

    $ which dts

should output : `/home/linuxbrew/.linuxbrew/bin/dts`

### OS X

[Install `pip3`](https://evansdianga.com/install-pip-osx/).
    
Add yourself to the `docker` group:

    $ sudo adduser `whoami` docker

Install the `duckietown-shell`:

**Note: Never use `sudo pip install` to install `duckietown-shell`.**

    $ pip3 install --no-cache-dir --user -U duckietown-shell

Note: you may need to *log in and out* to have the group change take effect.

By default Docker uses the OS X keychain to store credentials but this is not good.

Edit `~/.docker/config.json` and remove all references to a "osxkeychain".

Then run `docker login` again.

Then you should see an `auth` entry of the type:

    {
        "auths": {
            "https://index.docker.io/v1/": {
                "auth": "mXXXXXXXXXXXXXXXXXXXXXXXXXX"
            }
        },
    }


#### Testing the Installation

Typing 

    $ which dts
    
should output the path to the `dts` executable. This path can vary based on your python setup. 
If it is not found you may need to add something to your shell path. 

### Installation in other operating systems

To install the shell, use:

    $ pip3 install --no-cache-dir --user -U duckietown-shell

The shell itself does not require any other dependency beside standard cross-platform Python libraries.

**Note: Never use `sudo pip3 install` to install `duckietown-shell`.**

### Installation on Docker (experimental)

Assuming that Docker is already installed, place the following
in your `~/.bashrc` or other initialization file for a shell:

    alias dts='docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock  -w $PWD -v $PWD:$PWD -v ~/.dt-shell:/root/.dt-shell -v ~/.docker:/root/.docker duckietown/duckietown-shell:v3 dts'

Some functionality might not be available.



## Testing Duckietown shell

At this point, try to enter the Duckietown shell by typing the command

    $ dts

If you get an error, delete the subfolder `commands` in the folder `~/.dt-shell` 

    ~/.dt-shell$ rm -rf commands/

Then, try again

    $ dts

-----------------------

**You now have successfully installed the Duckietown Shell. If you know what you want to do with it go ahead. Below are some examples of things you can do with the Duckietown Shell** 

## Compile one of the "Duckumentation"

To compile one of the books (e.g. docs-duckumentation but there are many others):

    $ git clone https://github.com/duckietown/docs-duckumentation.git
    $ cd docs-duckumentation
    $ git submodule init
    $ git submodule update
    $ dts docs build

There is an incremental build system. To clean and run from scratch:

    $ dts docs clean
    $ dts docs build
  

## Authenticate a Duckietown Token

Run the command `dts tok set` to set the Duckietown authentication token:

    $ dts tok set  

Instructions will guide you and you will be prompted for the token.

If you already know the token, then you can use:

    $ dts tok set dt1-YOUR-TOKEN
    
### Verifying that a token is valid

To verify that a token is valid, you can use:

    $ dts tok verify dt1-TOKEN-TO-VERIFY
    
This exits with 0 if the token is valid, and writes on standard output the following json:

    {"uid": 3, "expiration": "2018-09-23"}
    
which means that the user is identified as uid 3 until the given expiration date.
 

-----------------------

## Duckiebot setup

### Command for flashing SD card

This command will install DuckieOS on the SD-card:

    $ dts init_sd_card

-----------------------

### Command for starting ROS GUIs

This command will start the ROS GUI container:

    $ dts start_gui_tools <DUCKIEBOT_NAME_GOES_HERE>

-----------------------

### Command for calibrating the Duckiebot

This command will run the Duckiebot calibration procedure:

    $ dts calibrate_duckiebot <DUCKIEBOT_NAME_GOES_HERE>

