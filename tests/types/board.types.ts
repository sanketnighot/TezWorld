
import { ContractAbstractionFromContractType, WalletContractAbstractionFromContractType } from './type-utils';
import { address, BigMap, nat } from './type-aliases';

export type Storage = {
    board_spaces: BigMap<nat, {
        category: string;
        name: string;
    }>;
    dealer_contract: address;
    players_contract: address;
    properties_and_utilities_contract: address;
    tezcredits_contract: address;
};

type Methods = {
    
};

type MethodsObject = {
    
};

type contractTypes = { methods: Methods, methodsObject: MethodsObject, storage: Storage, code: { __type: 'BoardCode', protocol: string, code: object[] } };
export type BoardContractType = ContractAbstractionFromContractType<contractTypes>;
export type BoardWalletType = WalletContractAbstractionFromContractType<contractTypes>;
