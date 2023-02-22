# -*- coding: UTF-8 -*-
################################################################################## 
## \file ptc_fetch.py
## PROJECT      = ED0106
## SW-PROJECT   = $ProjectName: $
## MODULE       = PTC Project Log
## DEVICE       = N/A \n
## VERSION      = $Revision: 1.1 $
## LABEL        = $Name:  $
## FIRST DATE   = 17.01.2023
## FIRST AUTHOR = schwarz
## LAST CHANGE  = $Date: $
## LAST AUTHOR  = $Author: schwarz $
##
## Environment: Python 3.x \n
## Assembler  : N/A \n
## C-Compiler : N/A \n
## Linker     : N/A \n
##
## Manufacturer:
##  LEMFOERDER ELECTRONIC
##  VON DEM BUSSCHE-MUENCH-STR. 12
##  D-32339 ESPELKAMP/GERMANY
##
## Description:   Analyse,generateReports and Migrate PTC/Windchill RVS/PTC projects and repositories
##
## Notes: - Consider to have Windchill RVS/PTC 11.x/PTC2009 correctly installed 
##        - by intent scripting API does not query for user credentials, be logged in parallel GUI session
##
##################################################################################
## REVISION LOG */
## Changes:
## $Log: ptc_fetch.py  $
##
################################################################


try:
   import os
   import re
   import logging  # logger Py lib
   import subprocess # pipelining subprocess
   import sys
   import argparse # parsing arguments wise
   import datetime
   import pandas
   from subprocess import call
 
except:
    logging.error("\n ERROR: Could not import module: ")
    logging.error(" Script execution terminated.")
    #fPTC_Util_Terminate()


from subprocess import call




#################################################################
#   This function executes a custom external file(command,script,CLI,switch,...) 
#   with os.popen. in case filename is passed as param, content is copied 
#   to given file    
#################################################################        
def fPTC_Util_CliCommand(arg_command,  arg_filename, arg_appendmode):
    
   try:    
     dir = r"./"
     cmdline = ""
     #rc = call(cmdline, cwd=dir) # run `cmdline` in `dir`
     rc = call("echo Hallo" + cmdline, cwd=dir, shell=True)
     rc = call("type hallo.txt" + cmdline, cwd=dir+"tempo", shell=True)


   except:
    logging.error("Command "+arg_command+" could not be executed via popen() ")
    arg_out = ["Error"]
    return arg_out #returns with error Info

   #arg_out = rc.decode('utf-8').split('\n')
   arg_out ="OK"
   
##   for i in range(len(arg_out)):
##        arg_out[i]=arg_out[i].replace("\n","") 
        
   
   if(arg_filename != ""):
        if (arg_appendmode == True):
            tmpFileHandle = open(arg_filename,'a')
        else:
            tmpFileHandle = open(arg_filename,'w')
        for tmpLine in arg_out:            
            tmpFileHandle.write(tmpLine+"\n")
        tmpFileHandle.close()
    
    # depreciated approach of piping subprocesses calls 
    # test = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # Read output from process call (err is empty)
    # out,err = test.communicate()
    
   return arg_out #returns list with output from executed command to pipe
################################################################


#################################################################
#   This function executes a custom external file(command,script,CLI,switch,...) 
#   with os.popen. in case filename is passed as param, content is copied 
#   to given file    
#################################################################        
def fPTC_Util_ExecuteCommand(arg_command,  arg_filename, arg_appendmode):
    
   try:    
       output= subprocess.run(arg_command,capture_output=True)
       tmpAusgabe = output.stdout

       #p = sub.Popedfsdfn(command, stdout=sub.PIPE, stderr=sub.PIPE, stdin=sub.PIPE, encoding="utf-8", universal_newlines=True)

   except:
    logging.error("Command "+arg_command+" could not be executed via popen() ")
    arg_out = ["Error"]
    return arg_out #returns with error Info

   arg_out = tmpAusgabe.decode('utf-8').split('\n')
   
##   for i in range(len(arg_out)):
##        arg_out[i]=arg_out[i].replace("\n","") 
        
   
   if(arg_filename != ""):
        if (arg_appendmode == True):
            tmpFileHandle = open(arg_filename,'a')
        else:
            tmpFileHandle = open(arg_filename,'w')
        for tmpLine in arg_out:            
            tmpFileHandle.write(tmpLine+"\n")
        tmpFileHandle.close()
    
    # depreciated approach of piping subprocesses calls 
    # test = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # Read output from process call (err is empty)
    # out,err = test.communicate()
    
   return arg_out #returns list with output from executed command to pipe
################################################################


################################################################
# Function: main                                               #
# main                                                         #
################################################################
 
def main():
  print("Hallo")    
  tmpOut=fPTC_Util_CliCommand(r"cmd.exe","tmp.txt",True)                   
  print(tmpOut)



################################################################
# call the main function after parsing all of this script      #
################################################################ 
if __name__=="__main__":
    main()
################################################################	
	
	
