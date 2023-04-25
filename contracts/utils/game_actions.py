import smartpy as sp  # type: ignore

player_action_type = sp.TVariant(
    land_on_owned_property=sp.TUnit,
    land_on_unowned_property=sp.TUnit,
    land_on_go=sp.TUnit,
    land_on_go_to_jail=sp.TUnit,
    land_on_tax_space=sp.TUnit,
    land_on_chance=sp.TUnit,
    land_on_community_chest=sp.TUnit,
    land_on_free_parking=sp.TUnit,
)


class GameActions(sp.Contract):
    def __init__(self):
        pass
    def land_on_owned_property(self, action):
        sp.emit(sp.record(data=action), tag="land_on_owned_property")

    def land_on_unowned_property(self, action):
        sp.emit(sp.record(data=action), tag="land_on_unowned_property")

    def land_on_go(self, action):
        sp.emit(sp.record(data=action), tag="land_on_go")

    def land_on_go_to_jail(self, action):
        sp.emit(sp.record(data=action), tag="land_on_go_to_jail")

    def land_on_tax_space(self, action):
        sp.emit(sp.record(data=action), tag="land_on_tax_space")

    def land_on_chance(self, action):
        sp.emit(sp.record(data=action), tag="land_on_chance")

    def land_on_community_chest(self, action):
        sp.emit(sp.record(data=action), tag="land_on_community_chest")

    def land_on_free_parking(self, action):
        sp.emit(sp.record(data=action), tag="land_on_free_parking")
    