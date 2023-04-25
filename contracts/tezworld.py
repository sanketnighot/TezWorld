import smartpy as sp  # type: ignore

FA12 = sp.io.import_script_from_url("https://smartpy.io/templates/FA1.2.py")
Address = sp.io.import_script_from_url("file:contracts/utils/address.py")
players_contract = sp.io.import_script_from_url("file:contracts/players.py")
dealer_contract = sp.io.import_script_from_url("file:contracts/dealer.py")
tezcredits_contract = sp.io.import_script_from_url("file:contracts/tezcredits.py")
board_contract = sp.io.import_script_from_url("file:contracts/board.py")
assets_contract = sp.io.import_script_from_url("file:contracts/assets.py")

if __name__ == "__main__":

    @sp.add_test("PlayersContract")
    def test():
        sc = sp.test_scenario()
        sc.h1("TezWorld: Players Contract (NFT Contract)")
        sc.table_of_contents()

        players = players_contract.Players(
            admin=Address.admin,
            metadata=sp.utils.metadata_of_url(
                "ipfs://QmW8jPMdBmFvsSEoLWPPhaozN6jGQFxxkwuMLtVFqEy6Fb"
            ),
        )
        sc += players

        sc.h1("Mint Player Cards")
        metadata = sp.pack(
            "ipfs://bafyreibwl5hhjgrat5l7cmjlv6ppwghm6ijygpz2xor2r6incfcxnl7y3e/metadata.json"
        )
        sc += players.mint([sp.record(to_=Address.admin, metadata={"": metadata})]).run(
            sender=Address.admin
        )

        sc.h1("Burn Player Cards")
        sc += players.burn([sp.record(amount=1, from_=Address.admin, token_id=0)]).run(
            sender=Address.admin
        )

    @sp.add_test("DealerContract")
    def test():
        sc = sp.test_scenario()
        sc.h1("TezWorld: Dealer Contract (Main Contract)")
        sc.table_of_contents()

        dealer = dealer_contract.Dealer(
            _stakeholders=sp.set([Address.admin]),
            _tezcredits_contract=sp.address("KT1tezcreditscontract"),
            _properties_and_utilities_contract=sp.address(
                "KT1propertiesandutilitiescontract"
            ),
            _players_contract=sp.address("KT1playerscontract"),
            _game_status=sp.variant("not_started", sp.unit),
            _game_fees=sp.tez(100),
        )
        sc += dealer

    @sp.add_test("TezCreditsContract")
    def test():
        sc = sp.test_scenario()
        sc.h1("TezWorld: TezCredits Contract (FA1.2 Contract)")
        sc.table_of_contents()

        token_metadata = {"name": "TzCredits", "symbol": "TZC", "decimals": "6"}
        tzc = tezcredits_contract.TezCredits(
            Address.admin,  # Update the admin Addressess before deployement to the chain.
            config=FA12.FA12_config(support_upgradable_metadata=True),
            token_metadata=token_metadata,
            contract_metadata={
                "": "ipfs://bafkreicysfopd2fnmytjgsagdk555mh6d2npfqrbtlbxfj7srwzayd2maq"
            },
        )
        sc += tzc

    @sp.add_test("BoardContract")
    def test():
        sc = sp.test_scenario()
        sc.h1("TezWorld: Board Contract (Game Board Contract)")

        sc.table_of_contents()
        board = board_contract.Board(
            _dealer_contract=sp.address("KT1dealercontract"),
            _tezcredits_contract=sp.address("KT1tezcreditscontract"),
            _properties_and_utilities_contract=sp.address(
                "KT1propertiesandutilitiescontract"
            ),
            _players_contract=sp.address("KT1playerscontract"),
        )
        sc += board

    @sp.add_test("TezosWorld")
    def test():
        sc = sp.test_scenario()
        sc.h1("TezWorld: All Contracts tested together")
        sc.table_of_contents()

        players = players_contract.Players(
            admin=Address.admin,
            metadata=sp.utils.metadata_of_url(
                "ipfs://QmW8jPMdBmFvsSEoLWPPhaozN6jGQFxxkwuMLtVFqEy6Fb"
            ),
        )
        sc.register(players)

        token_metadata = {"name": "TzCredits", "symbol": "TZC", "decimals": "6"}
        tzc = tezcredits_contract.TezCredits(
            Address.admin,  # Update the admin Addressess before deployement to the chain.
            config=FA12.FA12_config(support_upgradable_metadata=True),
            token_metadata=token_metadata,
            contract_metadata={
                "": "ipfs://bafkreicysfopd2fnmytjgsagdk555mh6d2npfqrbtlbxfj7srwzayd2maq"
            },
        )
        sc.register(tzc)

        dealer = dealer_contract.Dealer(
            _stakeholders=sp.set([Address.admin]),
            _tezcredits_contract=tzc.address,
            _properties_and_utilities_contract=sp.address(
                "KT1propertiesandutilitiescontract"
            ),
            _players_contract=players.address,
            _game_status=sp.variant("not_started", sp.unit),
            _game_fees=sp.tez(1500),
        )
        sc.register(dealer)

        board = board_contract.Board(
            _dealer_contract=dealer.address,
            _tezcredits_contract=tzc.address,
            _properties_and_utilities_contract=sp.address(
                "KT1propertiesandutilitiescontract"
            ),
            _players_contract=players.address,
        )
        sc.register(board)

        sc.h1("Initial Storage of all Contracts")

        sc.h2("Players Contract")
        sc.show(
            sp.record(contract_address=players.address, initial_storage=players.data)
        )

        sc.h2("Dealer Contract")
        sc.show(sp.record(contract_address=dealer.address, initial_storage=dealer.data))

        sc.h2("TezCredits Contract")
        sc.show(sp.record(contract_address=tzc.address, initial_storage=tzc.data))

        sc.h2("Board Contract")
        sc.show(sp.record(contract_address=board.address, initial_storage=board.data))

        sc += players.set_administrator(dealer.address).run(
            sender=Address.admin, show=False
        )
        sc += tzc.setAdministrator(dealer.address).run(sender=Address.admin, show=False)

        sc.h1("Register Player")
        metadata = sp.pack(
            "ipfs://bafyreibwl5hhjgrat5l7cmjlv6ppwghm6ijygpz2xor2r6incfcxnl7y3e/metadata.json"
        )
        sc.h2("Player 1")
        sc += dealer.register(sp.map({"": metadata})).run(
            sender=Address.alice, amount=sp.tez(1500)
        )

        sc.h2("Player 2")
        sc += dealer.register(sp.map({"": metadata})).run(
            sender=Address.bob, amount=sp.tez(1500)
        )

        sc.h1("Admin Starts the game")
        sc += dealer.update_game_status(sp.variant("on_going", sp.unit)).run(
            sender=Address.admin
        )

        sc.h1("Player 3 Tries to register after the game has started")
        sc += dealer.register(sp.map({"": metadata})).run(
            sender=Address.elon, amount=sp.tez(1500), valid=False
        )

        sc.h1("Player 1 rolls the dice")
        sc += dealer.roll_dice(
            player_id=sp.nat(0), dice_number=sp.pair(sp.nat(4), sp.nat(1))
        ).run(sender=Address.alice)

        sc.h1("Player 1 takes action")
        sc += dealer.take_action(
            player_id=sp.nat(0), action=sp.variant("land_on_unowned_property", sp.unit)
        ).run(sender=Address.alice)
