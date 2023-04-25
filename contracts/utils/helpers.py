import smartpy as sp  # type: ignore

Errors = sp.io.import_script_from_url("file:contracts/utils/errors.py")


class Helpers(sp.Contract):
    def __init__(self):
        pass

    def is_stakeholder(self):
        """
        This function verifies if the sender is a stakeholder in the smart contract.
        """
        sp.verify(self.data.stakeholders.contains(sp.sender), Errors.NotStakeholder)

    def is_player(self, player_id):
        sp.verify_equal(
            player_id,
            self.data.game_instance.open_some().current_player,
            Errors.NotYourTurn,
        )
        player_address = sp.view(
            "get_player", self.data.players_contract, player_id, t=sp.TAddress
        ).open_some("Error: Unable to get player address")
        sp.verify(sp.sender == player_address, Errors.InvalidPlayerId)

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
        with sp.if_(
            current_game_instance.value.current_game_action
            == sp.variant("await_player_action", sp.unit)
        ):
            with sp.if_(current_player_id.value == self.data.total_players):
                current_game_instance.value.current_player = sp.nat(0)
            with sp.else_():
                current_game_instance.value.current_player = (
                    current_player_id.value + sp.nat(1)
                )
        sp.trace(sp.some(current_game_instance.value))
        self.data.game_instance = sp.some(current_game_instance.value)

    def update_game_action(self, game_action):
        current_game_instance_ = sp.local(
            "current_game_instance_", self.data.game_instance.open_some()
        )
        with sp.if_(game_action == sp.variant("dice_roll", sp.unit)):
            current_game_instance_.value = sp.record(
                current_player=current_game_instance_.value.current_player,
                current_game_action=game_action,
                deadline_for_action=(sp.now).add_seconds(self.data.time_per_turn),
            )

        with sp.if_(game_action == sp.variant("await_player_action", sp.unit)):
            current_game_instance_.value = sp.record(
                current_player=current_game_instance_.value.current_player,
                current_game_action=game_action,
                deadline_for_action=(sp.now).add_seconds(self.data.time_per_turn),
            )
            self.update_current_player()
        self.data.game_instance = sp.some(current_game_instance_.value)

    def move_player_position(self, player_id, dice_number):
        fst, snd = sp.match_pair(dice_number)
        with sp.if_(fst != snd):
            self.data.player_ledger[player_id].doubles_on_dice = sp.nat(0)
        with sp.else_():
            self.data.player_ledger[player_id].doubles_on_dice += sp.nat(1)
        self.data.player_ledger[player_id].current_position = (
            self.data.player_ledger[player_id].current_position + fst + snd
        ) % 40
        return self.data.player_ledger[player_id].current_position
