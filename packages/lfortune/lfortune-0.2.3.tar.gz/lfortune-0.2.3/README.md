# Fortune

![Python application](https://github.com/lbacik/fortune/workflows/Python%20application/badge.svg)
[![codecov](https://codecov.io/gh/lbacik/fortune/branch/master/graph/badge.svg?token=W8LPOUVRSX)](https://codecov.io/gh/lbacik/fortune)

Program allows to play with fortunes files in a very similar way to the original "fortune" app 
(https://en.wikipedia.org/wiki/Fortune_(Unix)); however, a few new features are planned!

I have used "l" as a prefix for the console program version as the "fortune" name is already taken on PyPI.

## Installation

### PyPI

https://pypi.org/project/lfortune/

For python3:

    pip install lfortune
    
or (when the python2 is also installed):

    pip3 install lfortune

You will need to separately install the fortunes file(s) and appropriately configure the app (see below) - to point 
where it can find these file(s).

### Docker image

https://hub.docker.com/r/lbacik/fortune

There is set an automated build on dockerhub for the project's master branch. This build includes the debian's fortunes 
package (stable release).

    docker run --rm lbacik/fortune 

### Build the docker image locally

    git clone git@github.com:lbacik/fortune.git
    git checkout BRANCH
    docker build -t fortune:local . 

## Usage
 
### docker

If you are using docker image - it already contains the fortune package, however, there is still a few packages/sets 
which you can add/try - check the `apt search fortune` ;).

To get to bash prompt in docker image say:

    docker run --rm -ti --entrypoint=/bin/bash lbacik/fortune

### macOS

You can install the original fortune's data files with `brew` (of course it also contains the "fortune" program):

    brew install fortune 

Next see the "configuration" section (below).

### other 

You can just clone the fortune data files from any of its repositories, 
e.g: [debian salsa repos](https://salsa.debian.org/search?utf8=✓&search=fortune&group_id=&project_id=&snippets=false&repository_ref=&nav_source=navbar) 

## help

To get help:

**1. when using docker image:**

    docker run --rm lbacik/fortune --help
    
**2. when installed locally:**

    $ lfortune --help         
    usage: lfortune [-h] [-p [PATH]] [-c [CONFIG]] [--copy-config [COPY_CONFIG]] [--show-config] [--show-fortunes] 
                    [db ...]
    
    positional arguments:
      db                    fortunes db(s) - file(s)/directory(ies) (without root_path), optionally prepended with a
                            percentage chance of a hit, e.g: lfortune 50% computers art 40% tao (in this example art
                            will have 10%)
    
    optional arguments:
      -h, --help            show this help message and exit
      -p [PATH], --path [PATH]
                            file/directory to get random fortune from (overrides the root_path, it can be also set as
                            FORTUNES environment variable)
      -c [CONFIG], --config [CONFIG]
                            config file to use
      --copy-config [COPY_CONFIG]
                            copy config file. You can provide the dest, the default is ~/.config/lfortune/config.ini
      --show-config         show settings and exit
      --show-fortunes       show fortunes (only the first positional argument is used)
    
    2020 Łukasz Bacik <mail@luka.sh> https://github.com/lbacik/fortune

## Configuration

The `lfortune` app (installed locally) will have to know where it can find the fortunes data files. 
This information can be pass to the app on various ways:

**1. by the** `-p` **argument** 

Let assume we are using macOS, and you have installed the fortune files by the `brew` command (`brew install fortune`).
You can check where they had been copied by:

    $ brew list fortune
    /usr/local/Cellar/fortune/9708/bin/fortune
    /usr/local/Cellar/fortune/9708/bin/strfile
    /usr/local/Cellar/fortune/9708/bin/unstr
    /usr/local/Cellar/fortune/9708/share/games/ (70 files)
    /usr/local/Cellar/fortune/9708/share/man/ (3 files)

    $ ls /usr/local/Cellar/fortune/9708/share/games/                                   
    fortunes
    
    $ ls /usr/local/Cellar/fortune/9708/share/games/fortunes  
    ... a lot of files...
     
 So, the fortune's data files can be found at `/usr/local/Cellar/fortune/9708/share/games/fortunes`, 
 in such a case you can get the random fortune by: 
 
    $ lfortune -p /usr/local/Cellar/fortune/9708/share/games/fortunes       
 
**2. by the environment variable**
 
 The env variable which the fortune app is looking for is `FORTUNES`:
 
    $ export FORTUNES=/usr/local/Cellar/fortune/9708/share/games/fortunes
    $ lfortune
    
**3. by the config file**
 
 To copy the config file to your home directory you can use:
 
    $ lfortune --copy-config
    
Then the file is available at `~/.config/lfortune/config.ini` - you can set the fortune's data dir by setting 
the `root` parameter.    
 
## Examples

`lfortune` can be always replaced by the `docker run --rm lbacik/fortune`


    $ lfortune --show-config                                             
    ConfigValues(root_path=/usr/local/Cellar/fortune/9708/share/games/fortunes)

---

    $ lfortune --show-fortunes 
    PATH: /usr/local/Cellar/fortune/9708/share/games/fortunes
    computers
    riddles
    men-women
    literature
    love
    magic
    linuxcookie
    ...    

---

    $ lfortune --show-fortunes computers | tail
    %
    Your mode of life will be changed to ASCII.
    %
    Your mode of life will be changed to EBCDIC.
    %
    Your password is pitifully obvious.
    %
    Your program is sick!  Shoot it and put it out of its memory.
    %

---

Random generation from all the files in the `root` directory (and its subdirectories, what probably should be fixed):
    
    $ lfortune

---
    
Random generation from the file:

    $ lfortune magic
    "The first rule of magic is simple.  Don't waste your time waving your
    hands and hoping when a rock or a club will do."
                    -- McCloctnik the Lucid

---

Setting the percentage probability (linuxcookie will have had assigned the probability of 60%):

    $ lfortune 20% computers 20% magic linuxcookie
    "I once witnessed a long-winded, month-long flamewar over the use of
    mice vs. trackballs...It was very silly."
    (By Matt Welsh)
