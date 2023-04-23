
import { TezosToolkit } from '@taquito/taquito';
import { char2Bytes } from '@taquito/utils';
import { tas } from './types/type-aliases';
import { InMemorySigner, importKey } from '@taquito/signer';
import { BoardContractType as ContractType } from './types/board.types';
import { BoardCode as ContractCode } from './types/board.code';

jest.setTimeout(20000)

describe('board', () => {
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
                        board_spaces: tas.bigMap([{ 
                            key: tas.nat('42'), 
                            value: {
                            category: 'VALUE',
                            name: 'VALUE',
                        },
                        }]),
                        dealer_contract: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        players_contract: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        properties_and_utilities_contract: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        tezcredits_contract: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                    },
            });
            const newContractResult = await newContractOrigination.contract();
            const newContractAddress = newContractResult.address;
            contract = await Tezos.contract.at<ContractType>(newContractAddress);
            
    });

});
