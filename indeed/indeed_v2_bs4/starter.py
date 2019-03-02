"""
@author Archie_Paredes
@created Mar 1, 2018
@version 2.0
Indeed - Started program
"""
import os, sys, time, subprocess

jobtitle = input("Enter a job: ")
jobtitle = jobtitle.replace(" ", "_")


shell_command1 = "python indeed_linkLocTitl2.py".format(jobtitle)

os.system(shell_command1)

