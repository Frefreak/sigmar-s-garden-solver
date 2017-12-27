#!/usr/bin/env python

from enum import Enum, auto

class Elem(Enum):
    salt = '#ac9b74'
    fire = '#a42c0b'
    air = '#a9d6f1'
    water = '#77a09b'
    earth = '#325035'
    quicksilver = '#9ca4aa'
    lead = '#a2a2bc'
    tin = '#4f4935'
    iron = '#5b4b47'
    copper = '#dcb38a'
    silver = '#385457'
    gold = '#d89f31'
    mors = '#9d7a88'
    vitae = '#424132'

    def __init__(self, color):
        self.color = color
