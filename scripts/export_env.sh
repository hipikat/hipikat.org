#!/bin/bash

### Read files in [project]/var/env/ to environment variables.
project_dir=`cat $VIRTUAL_ENV/.project`
envfile_dir=$project_dir/var/env
for file in $envfile_dir/*
do
    file_name=${file##*/}
    export DJANGO_$file_name=`cat $file`
done


### Local settings
export DJANGO_SETTINGS_CLASS=Development