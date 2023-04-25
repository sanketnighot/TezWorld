import smartpy as sp  # type: ignore

GameActions = sp.io.import_script_from_url("file:contracts/utils/game_actions.py")

Categories = {
    "go": "go",
    "property_a": "property_a",
    "community_chest": "community_chest",
    "tax": "tax",
    "utility": "utility",
    "property_b": "property_b",
    "chance": "chance",
    "property_c": "property_c",
    "utility": "utility",
    "property_d": "property_d",
    "free_parking": "free_parking",
    "property_e": "property_e",
    "property_f": "property_f",
    "go_to_jail": "go_to_jail",
    "property_g": "property_g",
    "property_h": "property_h",
    "jail": "jail",
}

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


Spaces = sp.big_map(
    l={
        0: sp.record(
            name="go",
            category=Categories["go"],
            related_action=sp.set([sp.variant("land_on_go", sp.unit)]),
        ),
        1: sp.record(
            name="Mediterranean Avenue",
            category=Categories["property_a"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        2: sp.record(
            name="Community Chest",
            category=Categories["community_chest"],
            related_action=sp.set([sp.variant("land_on_community_chest", sp.unit)]),
        ),
        3: sp.record(
            name="Baltic Avenue",
            category=Categories["property_a"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        4: sp.record(
            name="Income tax",
            category=Categories["tax"],
            related_action=sp.set([sp.variant("land_on_tax_space", sp.unit)]),
        ),
        5: sp.record(
            name="Reading Railroad",
            category=Categories["utility"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        6: sp.record(
            name="Oriental Avenue",
            category=Categories["property_b"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        7: sp.record(
            name="chance",
            category=Categories["chance"],
            related_action=sp.set([sp.variant("land_on_chance", sp.unit)]),
        ),
        8: sp.record(
            name="Vermont Avenue",
            category=Categories["property_b"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        9: sp.record(
            name="Connecticut Avenue",
            category=Categories["property_b"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        10: sp.record(
            name="jail",
            category=Categories["jail"],
            related_action=sp.set([sp.variant("land_on_go", sp.unit)]),
        ),
        11: sp.record(
            name="St. Charles Place",
            category=Categories["property_c"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        12: sp.record(
            name="Electric Company",
            category=Categories["utility"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        13: sp.record(
            name="States Avenue",
            category=Categories["property_c"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        14: sp.record(
            name="Virginia Avenue",
            category=Categories["property_c"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        15: sp.record(
            name="Pennsylvania utility",
            category=Categories["utility"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        16: sp.record(
            name="St. James Place",
            category=Categories["property_d"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        17: sp.record(
            name="Community Chest",
            category=Categories["community_chest"],
            related_action=sp.set([sp.variant("land_on_community_chest", sp.unit)]),
        ),
        18: sp.record(
            name="Tennessee Avenue",
            category=Categories["property_d"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        19: sp.record(
            name="New York Avenue",
            category=Categories["property_d"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        20: sp.record(
            name="Free Parking",
            category=Categories["free_parking"],
            related_action=sp.set([sp.variant("land_on_free_parking", sp.unit)]),
        ),
        21: sp.record(
            name="Kentucky Avenue",
            category=Categories["property_e"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        22: sp.record(
            name="chance",
            category=Categories["chance"],
            related_action=sp.set([sp.variant("land_on_chance", sp.unit)]),
        ),
        23: sp.record(
            name="Indiana Avenue",
            category=Categories["property_e"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        24: sp.record(
            name="Illinois Avenue",
            category=Categories["property_e"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        25: sp.record(
            name="B. & O. utility",
            category=Categories["utility"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        26: sp.record(
            name="Atlantic Avenue",
            category=Categories["property_f"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        27: sp.record(
            name="Ventnor Avenue",
            category=Categories["property_f"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        28: sp.record(
            name="Water Works",
            category=Categories["utility"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        29: sp.record(
            name="Marvin Gardens",
            category=Categories["property_f"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        30: sp.record(
            name="go To jail",
            category=Categories["go_to_jail"],
            related_action=sp.set([sp.variant("land_on_go_to_jail", sp.unit)]),
        ),
        31: sp.record(
            name="Pacific Avenue",
            category=Categories["property_g"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        32: sp.record(
            name="North Carolina Avenue",
            category=Categories["property_g"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        33: sp.record(
            name="Community Chest",
            category=Categories["community_chest"],
            related_action=sp.set([sp.variant("land_on_community_chest", sp.unit)]),
        ),
        34: sp.record(
            name="Pennsylvania Avenue",
            category=Categories["property_g"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        35: sp.record(
            name="Short Line",
            category=Categories["utility"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        36: sp.record(
            name="chance",
            category=Categories["chance"],
            related_action=sp.set([sp.variant("land_on_chance", sp.unit)]),
        ),
        37: sp.record(
            name="Park Place",
            category=Categories["property_h"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
        38: sp.record(
            name="Luxury tax",
            category=Categories["tax"],
            related_action=sp.set([sp.variant("land_on_tax_space", sp.unit)]),
        ),
        39: sp.record(
            name="Boardwalk",
            category=Categories["property_h"],
            related_action=sp.set([
                sp.variant("land_on_unowned_property", sp.unit),
                sp.variant("land_on_owned_property", sp.unit),
            ]),
        ),
    },
    tkey=sp.TNat,
    tvalue=sp.TRecord(
        name=sp.TString,
        category=sp.TString,
        related_action=sp.TSet(player_action_type),
    ),
)
