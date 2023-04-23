import smartpy as sp  # type: ignore

FA2 = sp.io.import_script_from_url("file:contracts/utils/fa2.py")
Address = sp.io.import_script_from_url("file:contracts/utils/address.py")


class Players(
    FA2.Admin, FA2.MintNft, FA2.Fa2Nft, FA2.BurnNft, FA2.OnchainviewBalanceOf
):
    def __init__(self, admin, **kwargs):
        FA2.Fa2Nft.__init__(self, **kwargs)
        FA2.Admin.__init__(self, admin)
    
    @sp.onchain_view()
    def get_player(self, player_id):
        sp.set_type(player_id, sp.TNat)
        player_address = self.data.ledger[player_id]
        sp.result(player_address)

sp.add_compilation_target(
    "Compiled_Players_Contract",
    Players(
        admin=Address.admin,
        metadata=sp.utils.metadata_of_url(
            "ipfs://QmW8jPMdBmFvsSEoLWPPhaozN6jGQFxxkwuMLtVFqEy6Fb"
        ),
    ),
    storage=None,
)
