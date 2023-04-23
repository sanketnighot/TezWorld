
export const DealerCode: { __type: 'DealerCode', protocol: string, code: object[] } = {
    __type: 'DealerCode',
    protocol: 'PsDELPH1Kxsxt8f9eWbxQeRxkjfbxoqM52jvs5Y5fBxWWh4ifpo',
    code: JSON.parse(`[{"prim":"parameter","args":[{"prim":"unit","annots":["%register"]}]},{"prim":"storage","args":[{"prim":"pair","args":[{"prim":"pair","args":[{"prim":"pair","args":[{"prim":"mutez","annots":["%game_fees"]},{"prim":"or","annots":["%game_status"],"args":[{"prim":"unit","annots":["%NotStarted"]},{"prim":"unit","annots":["%not_started"]}]}]},{"prim":"pair","args":[{"prim":"map","annots":["%player_ledger"],"args":[{"prim":"nat"},{"prim":"pair","args":[{"prim":"address","annots":["%address"]},{"prim":"pair","args":[{"prim":"nat","annots":["%current_position"]},{"prim":"or","annots":["%player_status"],"args":[{"prim":"unit","annots":["%active"]},{"prim":"nat","annots":["%inactive"]}]}]}]}]},{"prim":"address","annots":["%players_contract"]}]}]},{"prim":"pair","args":[{"prim":"pair","args":[{"prim":"address","annots":["%properties_and_utilities_contract"]},{"prim":"set","annots":["%stakeholders"],"args":[{"prim":"address"}]}]},{"prim":"pair","args":[{"prim":"address","annots":["%tezcredits_contract"]},{"prim":"nat","annots":["%total_players"]}]}]}]}]},{"prim":"code","args":[[{"prim":"CDR"},{"prim":"DUP"},{"prim":"CAR"},{"prim":"CAR"},{"prim":"CAR"},{"prim":"AMOUNT"},{"prim":"COMPARE"},{"prim":"EQ"},{"prim":"IF","args":[[],[{"prim":"PUSH","args":[{"prim":"string"},{"string":"TzWorld: Insufficient_Amount"}]},{"prim":"FAILWITH"}]]},{"prim":"DUP"},{"prim":"CAR"},{"prim":"CAR"},{"prim":"CDR"},{"prim":"PUSH","args":[{"prim":"or","args":[{"prim":"unit"},{"prim":"unit"}]},{"prim":"Right","args":[{"prim":"Unit"}]}]},{"prim":"COMPARE"},{"prim":"EQ"},{"prim":"IF","args":[[],[{"prim":"PUSH","args":[{"prim":"string"},{"string":"TzWorld: Game_Already_Started"}]},{"prim":"FAILWITH"}]]},{"prim":"DUP"},[[{"prim":"DUP"},{"prim":"CAR"},{"prim":"DIP","args":[[{"prim":"CDR"}]]}]],[[{"prim":"DUP"},{"prim":"CAR"},{"prim":"DIP","args":[[{"prim":"CDR"}]]}]],{"prim":"SWAP"},[[{"prim":"DUP"},{"prim":"CAR"},{"prim":"DIP","args":[[{"prim":"CDR"}]]}]],{"prim":"PUSH","args":[{"prim":"or","args":[{"prim":"unit"},{"prim":"nat"}]},{"prim":"Left","args":[{"prim":"Unit"}]}]},{"prim":"PUSH","args":[{"prim":"nat"},{"int":"0"}]},{"prim":"SENDER"},{"prim":"PAIR","args":[{"int":"3"}]},{"prim":"SOME"},{"prim":"DIG","args":[{"int":"5"}]},{"prim":"GET","args":[{"int":"6"}]},{"prim":"UPDATE"},{"prim":"PAIR"},{"prim":"SWAP"},{"prim":"PAIR"},{"prim":"PAIR"},{"prim":"NIL","args":[{"prim":"operation"}]},{"prim":"PAIR"}]]}]`)
};
