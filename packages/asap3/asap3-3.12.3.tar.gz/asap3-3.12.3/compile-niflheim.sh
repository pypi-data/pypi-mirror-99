#!/bin/bash

# Compiling ASAP for Niflheim.
#
# This script assumes that you are already on Nifhleim and in the ASAP 
# directory. 

NIFHOSTS="slid.fysik.dtu.dk thul.fysik.dtu.dk fjorm.fysik.dtu.dk svol.fysik.dtu.dk"
NIFEXTRA="sylg.fysik.dtu.dk"
OK=n
for H in $NIFHOSTS $NIFEXTRA; do
    if [[ "$H" == `hostname` ]]; then
	OK=y
    fi
done
if [[ $OK == n ]]; then
    echo "Apparently not on a Niflheim compile node."
    echo "This script should be executed on one of these machines:"
    echo "   $NIFHOSTS"
    echo "but this is `hostname`"
    exit 1
fi

# if ( icpc -V 2> /dev/null ); then
#     true
# else
#     echo "ERROR: Intel compilers not available."
#     echo "Please add"
#     echo "    module load intel-compilers"
#     echo "to your .bashrc file."
#     exit 1
# fi

# Now loop over all machines and compile.  Note that `pwd` is executed
# when the command is parsed, i.e. on this machine!

if [[ -n "$VIRTUAL_ENV" ]] ; then
    echo "Virtual environment detected: $VIRTUAL_ENV"
    CMD="source \"$VIRTUAL_ENV\"/bin/activate && cd `pwd` && make depend-maybe && make -j16 all"
else
    CMD="cd `pwd` && make depend-maybe && make -j16 all"
fi
echo "Compilation command: $CMD"

for H in $NIFHOSTS; do
    echo
    echo "**** Compiling on $H ****"
    echo
    ssh $H "$CMD"
    if [[ $? -ne 0 ]]; then
	echo 
	echo '!!!!!!!  COMPILATION FAILED  !!!!!!!!'
	exit 1
    fi
done

for tch in intel foss; do
    if [[ ! -L "Nifl7_ivybridge_$tch" ]]; then
	ln -s Nifl7_sandybridge_$tch Nifl7_ivybridge_$tch
    fi
done
