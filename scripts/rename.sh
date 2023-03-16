#!/bin/bash

# counter=1

# for filename in ../classicGuide/xhtml/*; do
#     mv -i $filename "../classicGuide/xhtml/$counter.xhtml"
#     counter=$((counter + 1))
# done


counter=1

for filename in ../2015Guide/xhtml/*; do
    mv -i $filename "../2015Guide/xhtml/$counter.xhtml"
    counter=$((counter + 1))
done
