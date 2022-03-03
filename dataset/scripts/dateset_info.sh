#!/usr/bin/env bash

collectdates="20210102 20210108 20210111 20210112"
header="sensor number,filename,file size,line number,start time,end time"
root_dir=$1
output_dir=$2

for cdates in $collectdates; do
    clct_num_dirs=$root_dir"/"$cdates"/*"
    for numdir in $clct_num_dirs; do
        numinfofile=$(echo $numdir | awk 'BEGIN{FS="/"}{printf("%s-%s",$(NF-1), $NF)}')".csv"
        numinfofile=$output_dir$numinfofile
        echo $header > $numinfofile

        locdirs=$numdir"/*"
        locdirs=$(echo $locdirs | awk 'BEGIN{RS=" "; ORS=" "}/loc/{print}')
        for locd in $locdirs; do
            if [ -z "$(ls -A $locd)" ]; then
                continue
            fi
            sub_loc=$locd"/*.txt"
            sensor_num=$(echo $locd | awk 'BEGIN{FS="/"}{print $NF}')
            file_name=$(echo $sub_loc | awk 'BEGIN{FS="/"}{print $NF}')
            file_size=$(du -h $sub_loc | awk '{print $1}')
            line_number=$(wc -l $sub_loc | awk '{print $1}')
            start_time=$(head -n 3 $sub_loc | awk 'BEGIN{FS="\t"}NR==3{sub(/^\t+/, ""); print $2}')
            end_time=$(tail -n 1 $sub_loc | awk 'BEGIN{FS="\t"}{sub(/^\t+/, ""); print $2}')
            echo $sensor_num,$file_name,$file_size,$line_number,$start_time,$end_time >> $numinfofile
        done
    done
done
