import smartpy as sp  # type: ignore

FA12 = sp.io.import_script_from_url("https://smartpy.io/templates/FA1.2.py")
Address = sp.io.import_script_from_url("file:contracts/utils/address.py")


class TezCredits(FA12.FA12):
    pass


token_metadata = {"name": "TzCredits", "symbol": "TZC", "decimals": "6"}

sp.add_compilation_target(
    "Compiled_TezCredits_Contract",
    TezCredits(
        Address.admin,  # Update the admin Addressess before deployement to the chain.
        config=FA12.FA12_config(support_upgradable_metadata=True),
        token_metadata=token_metadata,
        contract_metadata={
            "": "ipfs://bafkreicysfopd2fnmytjgsagdk555mh6d2npfqrbtlbxfj7srwzayd2maq"
        },
    ),
    storage=None,
)
