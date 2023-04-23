
import { ContractAbstractionFromContractType, WalletContractAbstractionFromContractType } from './type-utils';
import { address, BigMap, bytes, contract, MMap, nat } from './type-aliases';

export type Storage = {
    administrator: address;
    balances: BigMap<address, {
        approvals: MMap<address, nat>;
        balance: nat;
    }>;
    metadata: BigMap<string, bytes>;
    paused: boolean;
    token_metadata: BigMap<nat, {
        token_id: nat;
        token_info: MMap<string, bytes>;
    }>;
    totalSupply: nat;
};

type Methods = {
    approve: (
        spender: address,
        value: nat,
    ) => Promise<void>;
    burn: (
        address: address,
        value: nat,
    ) => Promise<void>;
    getAdministrator: (
        _0: contract,
    ) => Promise<void>;
    getAllowance: (
        owner: address,
        spender: address,
        _2: contract,
    ) => Promise<void>;
    getBalance: (
        _0: address,
        _1: contract,
    ) => Promise<void>;
    getTotalSupply: (
        _0: contract,
    ) => Promise<void>;
    mint: (
        address: address,
        value: nat,
    ) => Promise<void>;
    setAdministrator: (param: address) => Promise<void>;
    setPause: (param: boolean) => Promise<void>;
    transfer: (
        from: address,
        to: address,
        value: nat,
    ) => Promise<void>;
    update_metadata: (
        key: string,
        value: bytes,
    ) => Promise<void>;
};

type MethodsObject = {
    approve: (params: {
        spender: address,
        value: nat,
    }) => Promise<void>;
    burn: (params: {
        address: address,
        value: nat,
    }) => Promise<void>;
    getAdministrator: (params: {
        0: contract,
    }) => Promise<void>;
    getAllowance: (params: {
        owner: address,
        spender: address,
        2: contract,
    }) => Promise<void>;
    getBalance: (params: {
        0: address,
        1: contract,
    }) => Promise<void>;
    getTotalSupply: (params: {
        0: contract,
    }) => Promise<void>;
    mint: (params: {
        address: address,
        value: nat,
    }) => Promise<void>;
    setAdministrator: (param: address) => Promise<void>;
    setPause: (param: boolean) => Promise<void>;
    transfer: (params: {
        from: address,
        to: address,
        value: nat,
    }) => Promise<void>;
    update_metadata: (params: {
        key: string,
        value: bytes,
    }) => Promise<void>;
};

type contractTypes = { methods: Methods, methodsObject: MethodsObject, storage: Storage, code: { __type: 'TezcreditsCode', protocol: string, code: object[] } };
export type TezcreditsContractType = ContractAbstractionFromContractType<contractTypes>;
export type TezcreditsWalletType = WalletContractAbstractionFromContractType<contractTypes>;
