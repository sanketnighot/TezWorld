import smartpy as sp  # type: ignore

spaces = sp.io.import_script_from_url("file:contracts/utils/board_spaces.py").Spaces


class Board(sp.Contract):
    def __init__(
        self,
        _dealer_contract,
        _tezcredits_contract,
        _properties_and_utilities_contract,
        _players_contract,
    ):
        self.init(
            board_spaces=spaces,
            dealer_contract=_dealer_contract,
            tezcredits_contract=_tezcredits_contract,
            properties_and_utilities_contract=_properties_and_utilities_contract,
            players_contract=_players_contract,
        )


sp.add_compilation_target(
    "Compiled_Board_Contract",
    Board(
        _dealer_contract=sp.address("KT1dealercontract"),
        _tezcredits_contract=sp.address("KT1tezcreditscontract"),
        _properties_and_utilities_contract=sp.address(
            "KT1propertiesandutilitiescontract"
        ),
        _players_contract=sp.address("KT1playerscontract"),
    ),
    storage=None,
)
