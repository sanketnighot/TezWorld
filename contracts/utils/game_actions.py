import smartpy as sp  # type: ignore

player_action_type = sp.TVariant(
    land_on_owned_property=sp.TUnit,
    land_on_unowned_property=sp.TBool,
    land_on_go=sp.TUnit,
    land_on_go_to_jail=sp.TUnit,
    land_on_tax_space=sp.TUnit,
    land_on_chance=sp.TUnit,
    land_on_community_chest=sp.TUnit,
    land_on_free_parking=sp.TUnit,
)

metadata = sp.pack(
    "ipfs://bafyreibwl5hhjgrat5l7cmjlv6ppwghm6ijygpz2xor2r6incfcxnl7y3e/metadata.json"
)


class GameActions(sp.Contract):
    def __init__(self):
        pass

    def land_on_unowned_property(self, action, token_id):
        action_data = sp.local(
            "action_data", action.open_variant("land_on_unowned_property")
        )
        with sp.if_(action_data.value == sp.bool(True)):
            property_data_type = sp.contract(
                sp.TRecord(
                    metadata=sp.TMap(sp.TString, sp.TBytes),
                    to=sp.TAddress,
                    token_id=sp.TNat,
                ),
                self.data.properties_and_utilities_contract,
                entry_point="mint",
            ).open_some()

            property_data = sp.record(
                metadata={"": metadata}, to=sp.sender, token_id=token_id
            )

            sp.transfer(property_data, sp.mutez(0), property_data_type)
            sp.emit(sp.record(property_id=token_id), tag="PropertyBought")
        with sp.if_(action_data.value == sp.bool(False)):
            sp.emit(sp.record(property_id=token_id), tag="PropertyAddedToAuction")

    def land_on_owned_property(self, action):
        sp.emit(sp.record(data=action), tag="land_on_owned_property")

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
