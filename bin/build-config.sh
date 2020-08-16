#!/bin/bash

CONFIG=$(envsubst < ./config_template.json | jq .)
echo $CONFIG
export CONFIG
