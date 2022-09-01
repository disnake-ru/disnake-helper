from enum import IntEnum


class Color(IntEnum):
    GRAY = 0x2F3136
    GREEN = 0x00FF00
    RED = 0xFF0000


class LogChannel(IntEnum):
    MESSSAGE_LOG = 994234860292022392
    MOD_LOG = 983347204884414514
    ON_MEMBER_JOIN = 994235079800913930
    BRANCH = 1008411379507662919


class Roles(IntEnum):
    UPDATE_DISNAKE = 983441082039820329
    UPDATE_SERVER = 983441129276063834
    DISNAKE_POLLS = 1008439902280630272
    GUIDES = 991387100639404172
    MODER = 983133009144324250
    HELPER = 983286061222473728
