BEGIN {
    FS = "\t"
    OFS = ","
}
NR == 2 {
    sub(/address\t/, "address ")
}
NR >= 2 && NR <= 5002 { # omit first line (startTime)
    sub(/^\t+/, "")
    print $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $13, $14, $15
}
