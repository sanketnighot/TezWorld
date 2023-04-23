def make(msg):
    return f"TzWorld: {msg}"


NotAdmin = make("Sender_Not_Admin")

NotStakeholder = make("Sender_Not_Stakeholder")

GameAlreadyStarted = make("Game_Already_Started")

InsufficientAmount = make("Insufficient_Amount")

InvalidShortAmount = make("Insufficient_Short_Amount")

InvalidCollateralAmount = make("Insufficient_Collateral_Amount")

NotInitialized = make("Contract_Not_Initialized")

AlreadyInitialized = make("Contract_Already_Initialized")

Paused = make("Contract_Paused")

InvalidVault = make("Invalid_Vault")

VaultExist = make("Vault_Already_Exist")

UnAuthorizedUser = make("UnAuthorized_User")

MaxPlayers = make("Maximum_Players_Reached")

NotMinimumPlayers = make("Not_Enough_Players")

InvalidGameInstance = make("Invalid_Game_Instance")

NotYourTurn = make("Not_Your_Turn")

InvalidPlayerId = make("Invalid_Player_Id")
