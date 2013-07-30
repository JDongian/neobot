Neobot
======

Automated neopets income generation!

Currently the only thing that works is Linux.Freebies.harvest, but it works well and should be cross
platform! Just run harvest.py, a frontend-ish for DailyFreebies.py.

I've scrapped any progress in Windows in favor of Linux development. Windows work using pywin32 will
continue when I have a few flash games in Linux working. Should be soon.


Have fun with this!


##Dependanices
In order of importance:
* python2.7
* python-requests
* python-bs4
* python-dogtail
* python-imaging (PIL)


##Instructions

To run the freebie collector, navigate to neobot/Linux/Freebies and run harvest.py. Records of the pages as you collected the freebie are located in neobet/Lunix/Freebies/dump/.

###Windows
Make sure to have python2.7, python-requests, and python-bs4 installed before continuing.
As of now, you can clone the repo and navigate to neobot/Linux/Freebies and run:

$ python harvest.py

and run the freebie collector!

###Mac OS
Make sure to have run:

$ brew install python-requests

$ brew install python-bs4

before continuing.
As of now, you can clone the repo and navigate to neobot/Linux/Freebies and run:

$ python harvest.py

and run the freebie collector!

###Linux
$ apt-get install python-requests python-bs4

$ git clone git@github.com:JDong820/neobot.git neobot/

$ cd neobot/Linux/Freebies

$ python harvest.py

##Finished Features

In order of completion:

* Avatar collector
* Potato counter **NEW!**
* Faerie crossword solver (uses tdn)
* Daily puzzle (uses tdn)
* Coltzan
* Tombola
* Anchor management (Krawken)
* Toy Box
* Blue Grundo Plushie
* Fruit machine
* Bank interest
* Apple Bobbing
* Obsidan quarry
* Underground Fishing
* Free Jelly
* Free Omelette
* Rich Slorg
* Geripikatu Tomb
* Lunar puzzle

##Upcoming Features

Expect (some of!) these within the coming week!

* Deamon auto-scheduler
* Better frontend **<**
* Kacheek Seek **<**
* Marrow Guessing

And if I get mouse control and screen capture working, this is the priority list of flash games, most of which I have existing logic code for.
* Fashion Fever
* Punchbag bob
* Coconut Shy
* Tug-o-War
* Ice Cream Machine
* The Buzzer Game
* Meepit vs Feepit
* Attack of the Revenge

##Known Bugs/Issues
* Logging in isn't registered correctly in DailyFreebies.py, and should be handled better in general.
* Console feedback is missing from harvest.py
* There's probably a bug somewhere in every file if you look hard enough...
