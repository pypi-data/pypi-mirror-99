# -*- coding: windows-1250 -*-

from time import sleep


class TeamMember:

    def __init__(self, name, support_message, is_sick=False):
        self.name = name
        self.support_message = support_message
        self.is_sick = is_sick

    def get_support_message(self):
        return f'---- {self.name} ----\n{self.support_message}'


def support_generator(team_members: list):
    """
    Generator that yields good thoughts and support from given team_members until sickness disappear.

    Parameters
    ----------
    team_members: One or more TeamMember objects that will be used inside of the generator.
    -------
    """

    while True:
        for team_member in team_members:
            sleep(5)
            yield team_member.get_support_message()