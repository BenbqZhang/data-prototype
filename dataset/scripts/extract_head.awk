BEGIN {
    FS = "\t"
    OFS = ","
}

NR == 2 {
    sub(/address\t/, "address ")
    sub(/^\t+/, "")
    print $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $13, $14, $15
}
NR > 2 { exit }
