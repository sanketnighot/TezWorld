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

    def is_current_player(self, player_id):
        sp.verify_equal(player_id, self.data.current_player, Errors.NotYourTurn)

    def is_player(self, player_id):
        sp.verify_equal(
            player_id,
            self.data.current_player,
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
        with sp.if_(
            self.data.player_ledger[self.data.current_player].doubles_on_dice == 0
        ):
            with sp.if_(self.data.current_player == abs(self.data.total_players - 1)):
                self.data.current_player = sp.nat(0)
            with sp.else_():
                self.data.current_player += sp.nat(1)

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
