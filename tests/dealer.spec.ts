
import { TezosToolkit } from '@taquito/taquito';
import { char2Bytes } from '@taquito/utils';
import { tas } from './types/type-aliases';
import { InMemorySigner, importKey } from '@taquito/signer';
import { DealerContractType as ContractType } from './types/dealer.types';
import { DealerCode as ContractCode } from './types/dealer.code';

jest.setTimeout(20000)

describe('dealer', () => {
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
                        game_fees: tas.mutez('42'),
                        game_status: (
                            { NotStarted: tas.unit() }
                            | { not_started: tas.unit() }
                        ),
                        player_ledger: tas.map([{ 
                            key: tas.nat('42'), 
                            value: {
                            address: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                            current_position: tas.nat('42'),
                            player_status: (
                                { active: tas.unit() }
                                | { inactive: tas.nat('42') }
                            ),
                        },
                        }]),
                        players_contract: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        properties_and_utilities_contract: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        stakeholders: [tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456')],
                        tezcredits_contract: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        total_players: tas.nat('42'),
                    },
            });
            const newContractResult = await newContractOrigination.contract();
            const newContractAddress = newContractResult.address;
            contract = await Tezos.contract.at<ContractType>(newContractAddress);
            
    });


    it('should call register', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const registerRequest = await contract.methodsObject.register().send();
        await registerRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });
});
