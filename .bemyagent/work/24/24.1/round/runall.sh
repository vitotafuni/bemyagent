#!/bin/zsh
# env: BMA_SCRATCH, BMA_ACCOUNT. Runs all arms (or those given as args), 3 at a time.
P=$BMA_SCRATCH
arms=("$@"); [ $# -eq 0 ] && arms=($(cd $P; ls -d [hs]-*/ | tr -d /))
printf '%s\n' $arms | xargs -P 3 -I{} zsh ${0:h}/launch.sh {}
