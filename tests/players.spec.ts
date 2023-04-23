
import { TezosToolkit } from '@taquito/taquito';
import { char2Bytes } from '@taquito/utils';
import { tas } from './types/type-aliases';
import { InMemorySigner, importKey } from '@taquito/signer';
import { PlayersContractType as ContractType } from './types/players.types';
import { PlayersCode as ContractCode } from './types/players.code';

jest.setTimeout(20000)

describe('players', () => {
	const config = require('../.taq/config.json')
    const Tezos = new TezosToolkit(config.sandbox.local.rpcUrl);
	const key = config.sandbox.local.accounts.bob.secretKey.replace('unencrypted:', '')
	Tezos.setProvider({
		signer: new InMemorySigner(key),
	  });
    let contract: ContractType = undefined as unknown as ContractType;
    beforeAll(async () => {
        
            const newContractOrigination = await Tezos.contract.originate<ContractType>({
                code: ContractCode.code,
                storage: {
                        administrator: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        ledger: tas.bigMap([{ 
                            key: tas.nat('42'), 
                            value: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        }]),
                        metadata: tas.bigMap({ 
                            'VALUE': tas.bytes(char2Bytes('DATA')),
                        }),
                        next_token_id: tas.nat('42'),
                        operators: tas.bigMap([{ 
                            key: {
                            owner: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                            operator: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                            token_id: tas.nat('42'),
                        }, 
                            value: tas.unit(),
                        }]),
                        token_metadata: tas.bigMap([{ 
                            key: tas.nat('42'), 
                            value: {
                            token_id: tas.nat('42'),
                            token_info: tas.map({ 
                                'VALUE': tas.bytes(char2Bytes('DATA')),
                            }),
                        },
                        }]),
                    },
            });
            const newContractResult = await newContractOrigination.contract();
            const newContractAddress = newContractResult.address;
            contract = await Tezos.contract.at<ContractType>(newContractAddress);
            
    });


    it('should call balance_of', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const balance_ofRequest = await contract.methodsObject.balance_of({
                requests: [{
                    owner: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                    token_id: tas.nat('42'),
                }],
                callback: tas.contract('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
            }).send();
        await balance_ofRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call burn', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const burnRequest = await contract.methodsObject.burn([{
                    from_: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                    token_id: tas.nat('42'),
                    amount: tas.nat('42'),
                }]).send();
        await burnRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call mint', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const mintRequest = await contract.methodsObject.mint([{
                    to_: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                    metadata: tas.map({ 
                        'VALUE': tas.bytes(char2Bytes('DATA')),
                    }),
                }]).send();
        await mintRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call set_administrator', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const set_administratorRequest = await contract.methodsObject.set_administrator(tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456')).send();
        await set_administratorRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call transfer', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const transferRequest = await contract.methodsObject.transfer([{
                    from_: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                    txs: [{
                        to_: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        token_id: tas.nat('42'),
                        amount: tas.nat('42'),
                    }],
                }]).send();
        await transferRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call add_operator', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const add_operatorRequest = await contract.methodsObject.add_operator({
                owner: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                operator: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                token_id: tas.nat('42'),
            }).send();
        await add_operatorRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call remove_operator', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const remove_operatorRequest = await contract.methodsObject.remove_operator({
                owner: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                operator: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                token_id: tas.nat('42'),
            }).send();
        await remove_operatorRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });
});
