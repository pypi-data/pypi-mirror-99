import binascii
import os

from jadi import service

from .terminal import Terminal


@service
class TerminalManager():
    """
    Manager class for all opened terminals
    """

    def __init__(self, context):
        self.context = context
        self.terminals = {}

    def __getitem__(self, _id):
        return self.terminals[_id]

    def __contains__(self, _id):
        return _id in self.terminals

    def list(self):
        """
        List all opened terminals.

        :return: List of terminal ids
        :rtype: list of hex
        """

        return [{
            'id': _id,
            'command': self[_id].command,
        } for _id in self.terminals]

    def create(self, **kwargs):
        """
        Open a new virtual terminal and register it.

        :return: Id of the new terminal
        :rtype: hex
        """

        _id = binascii.hexlify(os.urandom(32)).decode('utf-8')
        t = Terminal(self, _id, **kwargs)
        self.terminals[_id] = t
        return _id

    def kill(self, _id):
        """
        Sent a kill signal to Terminal object and remove it from opened terminals.

        :param _id: Id of the terminal
        :type _id: hex
        """

        self.terminals[_id].kill()
        self.remove(_id)

    def remove(self, _id):
        """
        Remove specified terminal from terminals dict.

        :param _id: Id of the terminal
        :type _id: hex
        """

        self.terminals.pop(_id)
