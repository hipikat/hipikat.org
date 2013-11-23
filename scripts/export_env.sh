#!/bin/bash

### Read files in [project]/var/env/ to environment variables.
project_dir=`cat $VIRTUAL_ENV/.project`
envfile_dir=$project_dir/var/env
for file in $envfile_dir/*
do
    file_name=${file##*/}
    export $file_name=`cat $file`
done
