
Name
====

**trackmsg.py** -  Track messages on postfix log, delivery status and other informations. 

Usage
=====

usage: trackmsg.py [-h] [-s SERVER] [-f SENDER] [-t RECIPIENT] [-r RELAY_HOST]
                   [-l LOGFILE]

 ./trackmsg.py -l maillog -f '.*gmail.com' 
+------------+--------+------------------------------+----------------------------+------------------+----------------+--------------------------+
| Message ID | Status |             From             |             To             |   Relay Server   | Sender Server  |     Extended Status      |
+------------+--------+------------------------------+----------------------------+------------------+----------------+--------------------------+
| 6F6C7C07DE |  sent  | lxxxxxxxxxxxxxxxxxxx@gmai... | gfleuryxxxxxxxx@xxxxxxx.br | exchangefront_xx | localhost[127. | (250 2.6.0 <CAHT2ZQukW7b |
|            |        |                              |                            | xxxxxxxx.xxx[10. |     0.0.1]     | 4ku9nkb0TcW2YV+OMxWkpqLW |
|            |        |                              |                            |   xxx.x.xx]:25   |                | 23ONUgm-NxmnHVA@mail.gma |
|            |        |                              |                            |                  |                | il.com> Queued mail for  |
|            |        |                              |                            |                  |                |        delivery)         |
+------------+--------+------------------------------+----------------------------+------------------+----------------+--------------------------+


You can use regex on any arguments. 

License
=======

This software is distributed under the terms of the FSF Lesser Gnu Public License (see [lgpl.txt](lgpl.txt)).
