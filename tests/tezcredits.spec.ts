
import { TezosToolkit } from '@taquito/taquito';
import { char2Bytes } from '@taquito/utils';
import { tas } from './types/type-aliases';
import { InMemorySigner, importKey } from '@taquito/signer';
import { TezcreditsContractType as ContractType } from './types/tezcredits.types';
import { TezcreditsCode as ContractCode } from './types/tezcredits.code';

jest.setTimeout(20000)

describe('tezcredits', () => {
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
                        balances: tas.bigMap([{ 
                            key: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'), 
                            value: {
                            approvals: tas.map([{ 
                                key: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'), 
                                value: tas.nat('42'),
                            }]),
                            balance: tas.nat('42'),
                        },
                        }]),
                        metadata: tas.bigMap({ 
                            'VALUE': tas.bytes(char2Bytes('DATA')),
                        }),
                        paused: true,
                        token_metadata: tas.bigMap([{ 
                            key: tas.nat('42'), 
                            value: {
                            token_id: tas.nat('42'),
                            token_info: tas.map({ 
                                'VALUE': tas.bytes(char2Bytes('DATA')),
                            }),
                        },
                        }]),
                        totalSupply: tas.nat('42'),
                    },
            });
            const newContractResult = await newContractOrigination.contract();
            const newContractAddress = newContractResult.address;
            contract = await Tezos.contract.at<ContractType>(newContractAddress);
            
    });


    it('should call approve', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const approveRequest = await contract.methodsObject.approve({
                spender: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                value: tas.nat('42'),
            }).send();
        await approveRequest.confirmation(3);
        
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
        
        const burnRequest = await contract.methodsObject.burn({
                address: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                value: tas.nat('42'),
            }).send();
        await burnRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call getAdministrator', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const getAdministratorRequest = await contract.methodsObject.getAdministrator({
                0: tas.contract('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
            }).send();
        await getAdministratorRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call getAllowance', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const getAllowanceRequest = await contract.methodsObject.getAllowance({
                owner: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                spender: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                2: tas.contract('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
            }).send();
        await getAllowanceRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call getBalance', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const getBalanceRequest = await contract.methodsObject.getBalance({
                0: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                1: tas.contract('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
            }).send();
        await getBalanceRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call getTotalSupply', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const getTotalSupplyRequest = await contract.methodsObject.getTotalSupply({
                0: tas.contract('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
            }).send();
        await getTotalSupplyRequest.confirmation(3);
        
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
        
        const mintRequest = await contract.methodsObject.mint({
                address: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                value: tas.nat('42'),
            }).send();
        await mintRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call setAdministrator', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const setAdministratorRequest = await contract.methodsObject.setAdministrator(tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456')).send();
        await setAdministratorRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call setPause', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const setPauseRequest = await contract.methodsObject.setPause(true).send();
        await setPauseRequest.confirmation(3);
        
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
        
        const transferRequest = await contract.methodsObject.transfer({
                from: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                to: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                value: tas.nat('42'),
            }).send();
        await transferRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call update_metadata', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const update_metadataRequest = await contract.methodsObject.update_metadata({
                key: 'VALUE',
                value: tas.bytes(char2Bytes('DATA')),
            }).send();
        await update_metadataRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });
});
