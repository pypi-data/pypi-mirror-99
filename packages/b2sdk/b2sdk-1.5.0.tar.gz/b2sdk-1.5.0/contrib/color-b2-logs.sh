#!/bin/bash -eu
awk -F '\t' '{print $1 " " $4 " " $5 " " $6}' | colorex --green=DEBUG \
    --bgreen=INFO \
    --bred=ERROR \
    --byellow=WARNING \
    --bmagenta='calling [\w\.]+' \
    --bblue='INFO // =+  [0-9\.]+   =+ \\' \
    --bblue='INFO // =+  [0-9\.]+   =+ \\' \
    --bblue='starting command .* with arguments:' \
    --bblue='starting command .* \(arguments hidden\)' \
    --red=Traceback \
    --green='\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,\d\d\d' \
    --cyan='b2\.sync'
