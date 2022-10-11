# -*- coding: utf-8 -*-

from dataclasses import dataclass

from recc_database.packet.group import Group
from recc_database.packet.group_member import GroupMember
from recc_database.packet.project import Project


@dataclass
class GroupJoinGroupMember(GroupMember, Group):
    pass


@dataclass
class ProjectJoinGroupMember(GroupMember, Project):
    pass
