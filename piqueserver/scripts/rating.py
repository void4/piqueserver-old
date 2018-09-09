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

@command('rating')
def rating(connection, value=None):
    if value is None:
        if connection not in connection.protocol.players:
            raise ValueError()
        player = connection
    else:
        player = get_player(connection.protocol, value)

    record = db.get(player.name)
    if record is None:
        return 'Player rating could not be determined.'

    return '%s rating is: %.2f' % (player.name, record.mu*100)


def apply_script(protocol, connection, config):
    return protocol, connection
