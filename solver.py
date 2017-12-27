#!/usr/bin/env python

from elements import Elem as E


_match_rules = set([
    (E.fire, E.fire),
    (E.water, E.water),
    (E.air, E.air),
    (E.earth, E.earth),
    (E.salt, E.salt),
    (E.salt, E.fire),
    (E.salt, E.water),
    (E.salt, E.air),
    (E.salt, E.earth),
    (E.mors, E.vitae),
    (E.quicksilver, E.lead),
    (E.quicksilver, E.tin),
    (E.quicksilver, E.iron),
    (E.quicksilver, E.copper),
    (E.quicksilver, E.silver),
    (E.quicksilver, E.gold)
])

match_rules = set()
for r1, r2 in _match_rules:
    match_rules.add((r1, r2))
    match_rules.add((r2, r1))
# single gold is a rule too
