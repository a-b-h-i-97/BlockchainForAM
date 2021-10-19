#! /bin/bash
geth --identity "DesignNode" init ./CustomGenisis.json --datadir ./DesignNode
geth --datadir ./DesignNode --networkid 98765 --port 30304