#!/usr/bin/env sh

input_file="$(git rev-parse --show-toplevel)/non_python_solutions/day1/data/2022-12-01-input.txt"

# PART 1: number of calories carried by elf with highest number of calories
awk '{ sum += $1 }; {if ($1 == "") { print sum; sum=0 }}; END { print sum }' $input_file | sort -rn | head -1

# PART 2: number of calories carried by three elves with highest number of calories
awk '{ sum += $1 }; {if ($1 == "") { print sum; sum=0 }}; END { print sum }' $input_file | sort -rn | head -3 | awk '{ sum += $1}; END { print sum }'
