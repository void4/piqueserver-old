"""
Gets a player's location info using a geoip database.

.. note::
  This script depends on `pygeoip` package and `piqueserver --update-geoip` needs to be executed after installing the package.

Commands
^^^^^^^^
* ``/from <player>`` get player's trueskill rating

.. codeauthor:: ?
"""

import os
from piqueserver.commands import command, get_player
from piqueserver.config import config

import shelve
import trueskill

db = shelve.open("shelve.db")

header = "Bottom 1%: 560 | 10%: 1430 | 20%: 1800 | 33%: 2130\nAverage: 2500\nTop 33%: 2870 | 20%: 3200 | 10%: 3560 | 1%: 4430\n"

@command('rating')
def rating(connection, value=None):
    db.sync()
    if value is None:
        if connection not in connection.protocol.players:
            raise ValueError()
        player = connection.name
    else:
        player = value

    record = db.get(player)
    if record is None:
        return 'Player rating could not be determined.'

    listing = "%s's rating is: %.2f" % (player, record.mu*100)
    return listing + "\n\n" + header

@command("top10")
def top10(connection):
    db.sync()
    sortedscores = sorted(list(db.items()), key=lambda x:x[1].mu, reverse=True)
    listing = "\n".join(["%.2f\t%.2f\t%s" % (v.mu*100,v.sigma*100,k) for k,v in sortedscores[:10]])
    return listing

def apply_script(protocol, connection, config):
    return protocol, connection
