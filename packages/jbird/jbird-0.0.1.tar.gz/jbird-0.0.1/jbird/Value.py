import os
from .Jbird import Jbird


class Value(Jbird):

    # name and full path to the keys file
    file = '__values.dat'

    # set variables, create directory and files
    def __init__(self):
        self._prepare()

        # create keys file if not exists
        if not os.path.isfile(os.path.join(self.path, self.file)):
            open(os.path.join(self.path, self.file), 'w').close()

    # return pos in bytes (!)
    def pos(self, pos: int) -> bytes:
        return int(pos).to_bytes(5, 'big')

    # return len in bytes (!)
    def vol(self, vol: int) -> bytes:
        return int(vol).to_bytes(5, 'big')

    def v(self):
        print('value')
        self.j()
