#!/bin/bash
ifconfig eth0 | grep inet | awk -F: '{print $2}'| awk '{print $1}'
# для alpine linux
