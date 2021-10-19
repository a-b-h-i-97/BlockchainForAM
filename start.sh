#! /bin/bash
geth --identity "mynode" init ./CustomGenisis.json --datadir ./testChain
geth --datadir ./testChain --networkid 98765