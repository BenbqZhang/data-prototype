BEGIN {
    FS = "\t"
    OFS = ","
}

NR == 2 {
    sub(/address\t/, "address ")
}

NR >= 2 { # omit first line (startTime)
    sub(/^\t+/, "")
    print $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $13, $14, $15
}

NR >= 3 && $2 > "2021-01-02 15:05:00.000" {
    exit
}
