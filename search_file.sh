#/bin/bash

for f in `find . -name "*.py"` ; do
    find1=`cat $f | grep "a"`
    find2=`cat $f | grep "settings"`
    if [[ ! -z $find1 ]] && [[ ! -z  $find2 ]] ; then 
        echo $find2
	echo $f
    fi
done
