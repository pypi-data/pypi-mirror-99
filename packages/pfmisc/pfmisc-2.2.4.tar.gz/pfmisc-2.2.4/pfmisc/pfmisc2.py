import sys
import os
import json
import pudb

from pfmisc._colors import Colors
from pfmisc.debug import debug
from pfmisc.C_snode import *
from pfmisc.error import *


class someOtherClass2():
    """
    Some other class
    """

    def __init__(self, *args, **kwargs):
        """
        """

        self.dp             = debug(verbosity=0, level=-1, within = "someOtherClass2")

    def say(self, msg):
        print('\n* Now we are in a different class in this module...')
        print('* Note the different class and method in the debug output.')
        print('* calling: self.dp.qprint(msg):')
        self.dp.qprint(msg)

class pfmisc2():
    """
    Example of how to use the local misc dependencies
    """

    # An error declaration block
    _dictErr = {
        'someError1'   : {
            'action'        : 'trying to parse image file specified, ',
            'error'         : 'wrong format found. Must be [<index>:]<filename>',
            'exitCode'      : 1},
        'someError2': {
            'action'        : 'trying to read input <tagFileList>, ',
            'error'         : 'could not access/read file -- does it exist? Do you have permission?',
            'exitCode'      : 20
            }
        }

    def col2_print(self, str_left, str_right):
        print(Colors.WHITE +
              ('%*s' % (self.LC, str_left)), end='')
        print(Colors.LIGHT_BLUE +
              ('%*s' % (self.RC, str_right)) + Colors.NO_COLOUR)

    def __init__(self, *args, **kwargs):
        """

        Holder for constructor of class -- allows for explicit setting
        of member 'self' variables.

        :return:
        """
        self.LC             = 40
        self.RC             = 40
        self.args           = None
        self.str_desc       = 'pfmisc'
        self.str_name       = self.str_desc
        self.str_version    = ''

        self.dp             = debug(verbosity   = 1,
                                    within      = 'pfmisc2')

        self.dp2            = debug(verbosity   = 1,
                                    within      = 'pfmisc2',
                                    debugToFile = True,
                                    debugFile   = '/tmp/pfmisc2.txt')
    def demo(self, *args, **kwargs):
        """
        Simple run method
        """

        print('* calling: self.dp.qprint("Why hello there, world!"):')
        self.dp.qprint("Why hello there, world!")

        print('* calling: self.dp2.qprint("Why hello there, world! In a debugging file!"):')
        self.dp2.qprint("Why hello there, world! In a debugging file!")
        print('* Check on /tmp/pfmisc2.txt')

        other = someOtherClass2()
        other.say("And this is from a different class")

        print('* now with no syslog...')
        print('* calling: self.dp.qprint("Hello there, world w/o syslog!", syslog = False):')
        self.dp.qprint("Hello there, world w/o syslog!", syslog = False)

        print('\n* end and no end...')
        print('* calling: self.dp.qprint("This is the end... ", end=''):')
        print('* calling: self.dp.qprint("My only friend the end", syslog = False):')
        self.dp.qprint("This is the end... ", end='')
        self.dp.qprint("My only friend the end", syslog = False)

        for str_comms in ['status', 'error', 'tx', 'rx']:
            print('\n* calling: self.dp.qprint("This string is tagged with %s" % str_comms, ', end='')
            print("comms = '%s')" % str_comms)
            self.dp.qprint("This string is tagged with '%s'" % str_comms, comms = str_comms)

        print("Followed by an error...")
        fatal(
            self, 'someError2',
            header  = 'This is an unrecoverable error!',
            drawBox = True
        )

