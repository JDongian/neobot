Neobot
======

Automated neopets income generation!

Currently the only thing that works is Freebies.harvest, but it works well and should be cross
platform!

I've scrapped any progress in Windows in favor of Linux development. I will work again on Windows using pywin32 when I have a few flash games in Linux working.


Have fun with this!


####Dependanices
In order of importance:
* python2.7
* python-requests
* python-bs4
* python-dogtail
* python-imaging (PIL)


####Instructions

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
You don't need instructions!

####Upcoming Features

Expect (some of!) these within the coming week!
 
* Fashion fever autoplay
* Coconut shy autoplay
* Farie crossword autoplay
* Deamon auto-scheduler

