import smartpy as sp  # type: ignore

FA2 = sp.io.import_script_from_url("file:contracts/utils/fa2.py")
Address = sp.io.import_script_from_url("file:contracts/utils/address.py")


class Assets(FA2.Admin, FA2.MintNft, FA2.Fa2Nft, FA2.BurnNft, FA2.OnchainviewBalanceOf):
    def __init__(self, admin, **kwargs):
        FA2.Fa2Nft.__init__(self, **kwargs)
        FA2.Admin.__init__(self, admin)

    @sp.entry_point
    def mint(self, metadata, to, token_id):
        sp.set_type(metadata, sp.TMap(sp.TString, sp.TBytes))
        sp.set_type(to, sp.TAddress)
        sp.set_type(token_id, sp.TNat)
        sp.verify(sp.sender == self.data.administrator, "FA2_NOT_ADMIN")
        self.data.token_metadata[token_id] = sp.record(
            token_id=token_id, token_info=metadata
        )
        self.data.ledger[token_id] = to

    @sp.onchain_view()
    def get_property_owner(self, property_id):
        sp.set_type(property_id, sp.TNat)
        property_owner = self.data.ledger[property_id]
        sp.result(property_owner)


sp.add_compilation_target(
    "Compiled_Assets_Contract",
    Assets(
        admin=Address.admin,
        metadata=sp.utils.metadata_of_url(
            "ipfs://QmW8jPMdBmFvsSEoLWPPhaozN6jGQFxxkwuMLtVFqEy6Fb"
        ),
    ),
    storage=None,
)
