import smartpy as sp  # type: ignore

Address = sp.io.import_script_from_url("file:contracts/utils/address.py")
Errors = sp.io.import_script_from_url("file:contracts/utils/errors.py")
GameActions = sp.io.import_script_from_url("file:contracts/utils/game_actions.py")
Helpers = sp.io.import_script_from_url("file:contracts/utils/helpers.py")
spaces = sp.io.import_script_from_url("file:contracts/utils/board_spaces.py").Spaces

game_status_type = sp.TVariant(
    not_started=sp.TUnit,
    on_going=sp.TUnit,
    ended=sp.TUnit,
).layout(("not_started", ("on_going", "ended")))

player_status_type = sp.TVariant(
    active=sp.TUnit, inactive=sp.TNat, bankrupt=sp.TUnit
).layout(("active", ("inactive", "bankrupt")))

game_action_type = sp.TVariant(dice_roll=sp.TUnit, await_player_action=sp.TUnit).layout(
    ("dice_roll", "await_player_action")
)


# ~ Dealer Contract ~
class Dealer(GameActions.GameActions, Helpers.Helpers):
    def __init__(
        self,
        _stakeholders,
        _tezcredits_contract,
        _properties_and_utilities_contract,
        _players_contract,
        _game_status,
        _game_fees,
    ):
        self.init(
            stakeholders=_stakeholders,
            tezcredits_contract=_tezcredits_contract,
            properties_and_utilities_contract=_properties_and_utilities_contract,
            players_contract=_players_contract,
            total_players=sp.nat(0),
            player_ledger=sp.map(
                tkey=sp.TNat,
                tvalue=sp.TRecord(
                    current_position=sp.TNat,
                    player_status=player_status_type,
                    doubles_on_dice=sp.TNat,
                    current_game_action=game_action_type,
                ),
            ),
            current_player=sp.nat(0),
            game_status=_game_status,
            game_fees=_game_fees,
            minimum_players=sp.nat(2),
            maximum_players=sp.nat(8),
            time_per_turn=sp.int(60),
        )
        self.init_type(
            sp.TRecord(
                stakeholders=sp.TSet(sp.TAddress),
                tezcredits_contract=sp.TAddress,
                properties_and_utilities_contract=sp.TAddress,
                players_contract=sp.TAddress,
                total_players=sp.TNat,
                player_ledger=sp.TMap(
                    sp.TNat,
                    sp.TRecord(
                        current_position=sp.TNat,
                        player_status=player_status_type,
                        doubles_on_dice=sp.TNat,
                        current_game_action=game_action_type,
                    ),
                ),
                current_player=sp.TNat,
                game_status=game_status_type,
                game_fees=sp.TMutez,
                minimum_players=sp.TNat,
                maximum_players=sp.TNat,
                time_per_turn=sp.TInt,
            )
        )
        GameActions.GameActions.__init__(self)
        Helpers.Helpers.__init__(self)

    @sp.entry_point
    def update_game_status(self, new_game_status):
        """
        This function updates the game status and performs some checks based on the new status.

        :param new_game_status: new_game_status is a parameter that represents the updated status of a
        game. The `new_game_status` parameter is of type `sp.TVariant`
        """
        sp.set_type(new_game_status, game_status_type)
        self.is_stakeholder()
        with sp.if_(self.data.game_status == sp.variant("ended", sp.unit)):
            sp.failwith("Game has ended")
        with sp.if_(self.data.game_status == sp.variant("not_started", sp.unit)):
            sp.verify(
                self.data.total_players >= self.data.minimum_players,
                Errors.NotMinimumPlayers,
            )
        self.data.game_status = new_game_status
        sp.emit(sp.record(new_game_status=new_game_status, tag="GAME_STATUS_UPDATED"))

    @sp.entry_point
    def update_player_status(self, new_player_status, player_id):
        """
        This function updates the player status in the player ledger and emits an event with the updated
        status and player ID.

        :param new_player_status: The new status to be assigned to a player
        :param player_id: player_id is a natural number that represents the player card id of a player that he holds. It is of type `sp.TNat`, which is a type of natural number used in SmartPy.
        """
        sp.set_type(new_player_status, player_status_type)
        sp.set_type(player_id, sp.TNat)
        self.is_stakeholder()
        self.data.player_ledger[player_id].player_status = new_player_status
        sp.emit(
            sp.record(player=player_id, status=new_player_status),
            tag="PLAYER_STATUS_UPDATED",
        )

    @sp.entry_point
    def register(self, metadata):
        """
        The function registers a player by minting a player card and tezcredits, adding the player to
        the ledger, and emitting an event.

        :param metadata: The metadata parameter is a map (dictionary) of string keys and bytes values
        that contains additional information about the player being registered. This information can be
        used to customize the player's card or provide additional context about the player
        """
        sp.set_type(metadata, sp.TMap(sp.TString, sp.TBytes))
        sp.verify_equal(sp.amount, self.data.game_fees, Errors.InsufficientAmount)
        sp.verify_equal(
            self.data.game_status,
            sp.variant("not_started", sp.unit),
            Errors.GameAlreadyStarted,
        )
        sp.verify(
            self.data.total_players < self.data.maximum_players, Errors.MaxPlayers
        )

        # Mint player card
        mint_player_contract_params = sp.contract(
            sp.TList(
                sp.TRecord(
                    metadata=sp.TMap(sp.TString, sp.TBytes), to_=sp.TAddress
                ).layout(("to_", "metadata")),
            ),
            self.data.players_contract,
            entry_point="mint",
        ).open_some("Error: Unable to mint player card")
        mint_player_data = [sp.record(metadata=metadata, to_=sp.sender)]
        sp.transfer(mint_player_data, sp.mutez(0), mint_player_contract_params)

        # Mint tezcredits
        mint_tzcredits_contract_params = sp.contract(
            sp.TRecord(address=sp.TAddress, value=sp.TNat).layout(("address", "value")),
            self.data.tezcredits_contract,
            entry_point="mint",
        ).open_some("Error: Unable to mint tezcredits")
        mint_tzcredits_data = sp.set_type_expr(
            sp.record(address=sp.sender, value=sp.utils.mutez_to_nat(sp.amount)),
            sp.TRecord(address=sp.TAddress, value=sp.TNat).layout(("address", "value")),
        )
        sp.transfer(mint_tzcredits_data, sp.mutez(0), mint_tzcredits_contract_params)

        # Add Player to ledger
        self.data.player_ledger[self.data.total_players] = sp.record(
            current_position=sp.nat(0),
            player_status=sp.variant("active", sp.unit),
            doubles_on_dice=sp.nat(0),
            current_game_action=sp.variant("dice_roll", sp.unit),
        )
        self.data.total_players += sp.nat(1)

        # Emit event
        sp.emit(
            sp.record(address=sp.sender, player_id=self.data.total_players),
            tag="PlayerRegistered",
        )

    @sp.entry_point
    def roll_dice(self, player_id, dice_number):
        sp.set_type(player_id, sp.TNat)
        sp.set_type(dice_number, sp.TPair(sp.TNat, sp.TNat))
        self.is_player(player_id)
        self.is_current_player(player_id)
        sp.verify(
            self.data.player_ledger[player_id].current_game_action
            == sp.variant("dice_roll", sp.unit),
            Errors.InvalidAction,
        )
        # TODO: Implement dice roll logic and remove dice_number parameter and its logic
        self.move_player_position(player_id, dice_number)
        self.data.player_ledger[player_id].current_game_action = sp.variant(
            "await_player_action", sp.unit
        )

    @sp.entry_point
    def take_action(self, player_id, action):
        # TODO: Check if action aligns with the players position
        self.is_player(player_id)
        self.is_current_player(player_id)

        sp.verify(
            self.data.player_ledger[player_id].current_game_action
            == sp.variant("await_player_action", sp.unit),
            Errors.InvalidAction,
        )
        sp.set_type(action, GameActions.player_action_type)
        with sp.if_(action.is_variant("land_on_owned_property")):
            sp.verify(
                spaces[
                    self.data.player_ledger[player_id].current_position
                ].related_action.contains(
                    sp.variant("land_on_owned_property", sp.unit)
                ),
                Errors.InvalidAction,
            )
            self.land_on_owned_property(action)
        with sp.if_(action.is_variant("land_on_unowned_property")):
            sp.verify(
                spaces[
                    self.data.player_ledger[player_id].current_position
                ].related_action.contains(
                    sp.variant("land_on_unowned_property", sp.unit)
                ),
                Errors.InvalidAction,
            )
            self.land_on_unowned_property(
                action, self.data.player_ledger[player_id].current_position
            )
        with sp.if_(action.is_variant("land_on_go")):
            sp.verify(
                spaces[
                    self.data.player_ledger[player_id].current_position
                ].related_action.contains(sp.variant("land_on_go", sp.unit)),
                Errors.InvalidAction,
            )
            self.land_on_go(action)
        with sp.if_(action.is_variant("land_on_go_to_jail")):
            sp.verify(
                spaces[
                    self.data.player_ledger[player_id].current_position
                ].related_action.contains(sp.variant("land_on_go_to_jail", sp.unit)),
                Errors.InvalidAction,
            )
            self.land_on_go_to_jail(action)
        with sp.if_(action.is_variant("land_on_tax_space")):
            sp.verify(
                spaces[
                    self.data.player_ledger[player_id].current_position
                ].related_action.contains(sp.variant("land_on_tax_space", sp.unit)),
                Errors.InvalidAction,
            )
            self.land_on_tax_space(action)
        with sp.if_(action.is_variant("land_on_chance")):
            sp.verify(
                spaces[
                    self.data.player_ledger[player_id].current_position
                ].related_action.contains(sp.variant("land_on_chance", sp.unit)),
                Errors.InvalidAction,
            )
            self.land_on_chance(action)
        with sp.if_(action.is_variant("land_on_community_chest")):
            sp.verify(
                spaces[
                    self.data.player_ledger[player_id].current_position
                ].related_action.contains(
                    sp.variant("land_on_community_chest", sp.unit)
                ),
                Errors.InvalidAction,
            )
            self.land_on_community_chest(action)
        with sp.if_(action.is_variant("land_on_free_parking")):
            sp.verify(
                spaces[
                    self.data.player_ledger[player_id].current_position
                ].related_action.contains(sp.variant("land_on_free_parking", sp.unit)),
                Errors.InvalidAction,
            )
            self.land_on_free_parking(action)
        self.data.player_ledger[player_id].current_game_action = sp.variant(
            "await_player_action", sp.unit
        )
        self.data.player_ledger[player_id].current_game_action = sp.variant(
            "dice_roll", sp.unit
        )
        self.update_current_player()


sp.add_compilation_target(
    "Compiled_Dealer_Contract",
    Dealer(
        _stakeholders=sp.set([Address.admin]),
        _tezcredits_contract=sp.address("KT1tezcreditscontract"),
        _properties_and_utilities_contract=sp.address(
            "KT1propertiesandutilitiescontract"
        ),
        _players_contract=sp.address("KT1playerscontract"),
        _game_status=sp.variant("not_started", sp.unit),
        _game_fees=sp.tez(100),
    ),
    storage=None,
)
