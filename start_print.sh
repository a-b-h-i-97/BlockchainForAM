#! /bin/bash
geth --identity "PrintNode" init ./CustomGenisis.json --datadir ./PrintNode
geth --datadir ./PrintNode --networkid 98765 --port 30305