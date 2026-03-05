#!/bin/bash

PIPE=/tmp/demo_named_pipe

while true
do
    for img in test_images/*
    do
        echo "Writing to Pipe : $img"

        test -p "$PIPE" && echo "Writing  $img to named pipe : $PIPE"

        dd if="$img" of="$PIPE" status=progress 2>&1 | awk '{print "\t"$0}'

        sleep 2
    done

    echo "End..."
done