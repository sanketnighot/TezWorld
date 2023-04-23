
import { ContractAbstractionFromContractType, WalletContractAbstractionFromContractType } from './type-utils';
import { address, MMap, mutez, nat, unit } from './type-aliases';

export type Storage = {
    game_fees: mutez;
    game_status: (
        { NotStarted: unit }
        | { not_started: unit }
    );
    player_ledger: MMap<nat, {
        address: address;
        current_position: nat;
        player_status: (
            { active: unit }
            | { inactive: nat }
        );
    }>;
    players_contract: address;
    properties_and_utilities_contract: address;
    stakeholders: Array<address>;
    tezcredits_contract: address;
    total_players: nat;
};

type Methods = {
    default: () => Promise<void>;
};

type MethodsObject = {
    default: () => Promise<void>;
};

type contractTypes = { methods: Methods, methodsObject: MethodsObject, storage: Storage, code: { __type: 'DealerCode', protocol: string, code: object[] } };
export type DealerContractType = ContractAbstractionFromContractType<contractTypes>;
export type DealerWalletType = WalletContractAbstractionFromContractType<contractTypes>;
