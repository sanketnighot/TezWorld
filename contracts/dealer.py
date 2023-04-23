import smartpy as sp  # type: ignore

Address = sp.io.import_script_from_url("file:contracts/utils/address.py")
Errors = sp.io.import_script_from_url("file:contracts/utils/errors.py")


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
class Dealer(sp.Contract):
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
                ),
            ),
            game_status=_game_status,
            game_fees=_game_fees,
            minimum_players=sp.nat(2),
            maximum_players=sp.nat(8),
            game_instance=sp.none,
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
                    ),
                ),
                game_status=game_status_type,
                game_fees=sp.TMutez,
                minimum_players=sp.TNat,
                maximum_players=sp.TNat,
                game_instance=sp.TOption(
                    sp.TRecord(
                        current_player=sp.TNat,
                        current_game_action=game_action_type,
                        # deadline_for_action=sp.TTimestamp, 
                    )
                ),
            )
        )

    def is_stakeholder(self):
        """
        This function verifies if the sender is a stakeholder in the smart contract.
        """
        sp.verify(self.data.stakeholders.contains(sp.sender), Errors.NotStakeholder)

    def update_current_player(self):
        """
        This function updates the current player in a game instance.
        """
        sp.verify(self.data.game_instance != sp.none, Errors.InvalidGameInstance)
        current_game_instance = sp.local(
            "current_game_instance", self.data.game_instance.open_some()
        )
        current_player_id = sp.local(
            "current_player_id", current_game_instance.value.current_player
        )
        with sp.if_(current_player_id.value == self.data.total_players):
            current_game_instance.value.current_player = sp.nat(0)
        with sp.else_():
            current_game_instance.value.current_player = (
                current_player_id.value + sp.nat(1)
            )

    def move_player_position(self, player_id, dice_number):
        fst, snd = sp.match_pair(dice_number)
        with sp.if_(fst != snd):
            self.update_current_player()
            self.data.player_ledger[player_id].doubles_on_dice = sp.nat(0)
        with sp.else_():
            self.data.player_ledger[player_id].doubles_on_dice += sp.nat(1)
        self.data.player_ledger[player_id].current_position = (
            self.data.player_ledger[player_id].current_position + fst + snd
        ) % 40

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
        with sp.if_(new_game_status == sp.variant("on_going", sp.unit)):
            self.data.game_instance = sp.some(
                sp.record(
                    current_player=sp.nat(0),
                    current_game_action=sp.variant("dice_roll", sp.unit),
                )
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
        sp.verify_equal(
            player_id,
            self.data.game_instance.open_some().current_player,
            Errors.NotYourTurn,
        )
        player_address = sp.view(
            "get_player", self.data.players_contract, player_id, t=sp.TAddress
        ).open_some("Error: Unable to get player address")
        sp.verify(sp.sender == player_address, Errors.InvalidPlayerId)
        # TODO: Implement dice roll logic and remove dice_number parameter and its logic
        self.move_player_position(player_id, dice_number)
        current_game_instance = sp.local(
            "current_game_instance", self.data.game_instance.open_some()
        )
        current_game_instance.value.current_game_action = sp.variant(
            "dice_roll", sp.unit
        )
        self.data.game_instance = sp.some(current_game_instance.value)


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
