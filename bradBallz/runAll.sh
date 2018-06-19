#!/bin/sh
#script to runn everthing along with helpful metadata
python getNamesToCkeckAgainst.py
time scrapy crawl brooksbaseball && du -h bothOut.csv

