#!/bin/sh

IFS=,
while read pkg; do
  pip install $pkg
done
