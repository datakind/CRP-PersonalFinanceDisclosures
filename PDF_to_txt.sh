#!/bin/bash

# This converts pdfs to txt files and should be run from the folder containing 
# the pdf files to convert to txt

for f in *.pdf
do
    v2=${f::-4}
    pdftoppm $f $v2 -png

    for t in ${v2}-*
    do
        v3=${t::-4}
        tesseract $t $v3
    done

    for c in ${v3}-*
    do
        final="${v2}.txt"
        cat $c >> $final
    done

done
     
