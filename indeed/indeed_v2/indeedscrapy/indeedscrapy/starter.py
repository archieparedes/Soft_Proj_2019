"""
@author Archie_Paredes
@created Mar 1, 2018
@version 2.0
Indeed - Started program
"""
import os, sys, time, subprocess

jobtitle = input("Enter a job: ")
jobtitle = jobtitle.replace(" ", "_")


shell_command1 = "scrapy crawl indeedLinks -a job={} -a domain=system -o t1.csv -t csv".format(jobtitle)


os.system(shell_command1)

