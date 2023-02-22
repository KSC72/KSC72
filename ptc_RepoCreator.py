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
 
except:
    logging.error("\n ERROR: Could not import module: ")
    logging.error(" Script execution terminated.")
    #fPTC_Util_Terminate()



################################################################
#     Definition of ext tools and file names                   #
################################################################
fDefSystemEditor    	= r"Notepad.exe"
fDefFileListFile        = r"filelist.txt"
fDefFileIncFile         = r"fileinc.txt"
fDefFileLogging         = r"ptc_fetch.log"
fDefProjViewQuery       = r"ptc_proj.log"
fDefLabelViewQuery      = r"ptc_label.log"

################################################################
# check and parse command line arguments                       #
################################################################
def fPTC_Util_check_command_line_parameter():
    
    parser = argparse.ArgumentParser(description="Creates a an automatic fetch of overall PTC projects and repositories report.")
    
    parser.add_argument("--project", required=True, help="The project of the report")
    parser.add_argument("--input",required=True,help="JSON file with PTC command configuration")
    parser.add_argument("--outputBase", required=True, help="The output folder Base.")

    global args
    args = parser.parse_args()
    args.input = args.input.replace("/", os.sep)
    args.output = os.path.abspath(args.output.replace("/", os.sep))

    return #end of def with no defined return
################################################################

################################################################
# initializeLogging                                            #
################################################################
def fPTC_Util_initLogging():
  # configure logger
  logging.Formatter(fmt='%(asctime)s.%(msecs)03d',datefmt='%Y-%m-%d,%H:%M:%S')

  logging.basicConfig(filename=fDefFileLogging,
                    format='%(asctime)s %(message)s',
                    filemode='a')
  
  logging.Formatter(fmt='%(asctime)s.%(msecs)03d',datefmt='%Y-%m-%d,%H:%M:%S')
 
  # Creating an object
  logger = logging.getLogger()

  # Setting the threshold of logger to DEBUG
  logger.setLevel(logging.DEBUG)

  return #end of def with no defined return
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

   arg_out = tmpAusgabe.decode('cp850').split('\n')
   
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
# generate list of projects in PTC
################################################################
def fPTC_Util_ViewProjects(arg_ProjectName, arg_Subprojects):
    
    # save current working dir
    tmpCurrentWorkDir = os.getcwd()
    
    logging.info("Generating Project View")
    
    tmp_PTC_Command  = "si projects --nodisplaySubs"
  
    arg_out = fPTC_Util_ExecuteCommand(tmp_PTC_Command,fDefProjViewQuery,"w")
    
    logging.info("si projects performed")
    
    # return to original workdir
    os.chdir(tmpCurrentWorkDir)

    return arg_out # returns lists with queried project
################################################################	



################################################################
# generate list of labels in PTC
################################################################
def fPTC_Util_ViewlabelsAll(arg_ProjectName, arg_Subprojects):
    
    # save current working dir
    tmpCurrentWorkDir = os.getcwd()
    
    logging.info("Generating Label View")
    
    # si viewprojecthistory --project=f:/MKS/MKS_db/EE0084_SOFTWARE/project.pj --rfilter=labeled --fields=labels
    tmp_PTC_Command  = "si viewprojecthistory --project="+ arg_ProjectName+ " --fields=revision,date,labels"
  
    arg_out = fPTC_Util_ExecuteCommand(tmp_PTC_Command,"","")
    
    logging.info("si viewlabels performed")
    
    # return to original workdir
    os.chdir(tmpCurrentWorkDir)

    return arg_out

################################################################
# generate list of labels in PTC
################################################################
def fPTC_Util_ViewlabelsAuthors(arg_ProjectName, arg_Subprojects):
    
    # save current working dir
    tmpCurrentWorkDir = os.getcwd()
    
    logging.info("Generating Label View")
    
    # si viewprojecthistory --project=f:/MKS/MKS_db/EE0084_SOFTWARE/project.pj --rfilter=labeled --fields=labels
    tmp_PTC_Command  = "si viewprojecthistory --project="+ arg_ProjectName+ " --fields=revision,date,author"
  
    arg_out = fPTC_Util_ExecuteCommand(tmp_PTC_Command,"","")
    
    logging.info("si viewlabels performed")
    
    # return to original workdir
    os.chdir(tmpCurrentWorkDir)

    return arg_out


################################################################
# generate list of labels in PTC
################################################################
def fPTC_Util_ViewlabelsDescr(arg_ProjectName, arg_Subprojects):
    
    # save current working dir
    tmpCurrentWorkDir = os.getcwd()
    
    logging.info("Generating Label View")
    
    # si viewprojecthistory --project=f:/MKS/MKS_db/EE0084_SOFTWARE/project.pj --rfilter=labeled --fields=labels
    tmp_PTC_Command  = "si viewprojecthistory --project="+ arg_ProjectName+ " --fields=revision,date,description"
  
    arg_out = fPTC_Util_ExecuteCommand(tmp_PTC_Command,"","")
    
    logging.info("si viewlabels performed")
    
    # return to original workdir
    os.chdir(tmpCurrentWorkDir)

    return arg_out


################################################################
# generate list of labels in PTC
################################################################
def fPTC_Util_Viewlabels(arg_ProjectName, arg_Subprojects):
    
    # save current working dir
    tmpCurrentWorkDir = os.getcwd()
    
    logging.info("Generating Label View")
    
    # si viewprojecthistory --project=f:/MKS/MKS_db/EE0084_SOFTWARE/project.pj --rfilter=labeled --fields=labels
    tmp_PTC_Command  = "si viewprojecthistory --project="+ arg_ProjectName+ " --rfilter=labeled --fields=labels"
  
    arg_out = fPTC_Util_ExecuteCommand(tmp_PTC_Command,fDefLabelViewQuery,"w")
    
    logging.info("si viewlabels performed")
    
    # return to original workdir
    os.chdir(tmpCurrentWorkDir)

    return arg_out
################################################################

################################################################
# get revision labels of revs in PTC
################################################################
def fPTC_Util_GetRevlabels(arg_ProjectName, arg_Subprojects):
    
    # save current working dir
    tmpCurrentWorkDir = os.getcwd()
    
    logging.info("Generating Label View")
    
    # si viewprojecthistory --project=f:/MKS/MKS_db/EE0084_SOFTWARE/project.pj --rfilter=labeled --fields=labels
    tmp_PTC_Command  = "si viewprojecthistory --project="+ arg_ProjectName+ " --fields=revision,labels"
  
    arg_out = fPTC_Util_ExecuteCommand(tmp_PTC_Command,fDefLabelViewQuery,"w")
    
    logging.info("si viewlabels performed")
    
    # return to original workdir
    os.chdir(tmpCurrentWorkDir)

    return arg_out
################################################################

################################################################
# get revision dates of revs in PTC
################################################################
def fPTC_Util_GetRevDates(arg_ProjectName, arg_Subprojects):
    
    # save current working dir
    tmpCurrentWorkDir = os.getcwd()
    
    logging.info("Generating Label View")
    
    # si viewprojecthistory --project=f:/MKS/MKS_db/EE0084_SOFTWARE/project.pj --rfilter=labeled --fields=labels
    tmp_PTC_Command  = "si viewprojecthistory --project="+ arg_ProjectName+ " --fields=revision,date"
  
    arg_out = fPTC_Util_ExecuteCommand(tmp_PTC_Command,fDefLabelViewQuery,"w")
    
    logging.info("si viewlabels performed")
    
    # return to original workdir
    os.chdir(tmpCurrentWorkDir)

    return arg_out
################################################################

################################################################
# get revision dates of revs in PTC
################################################################
def fPTC_Util_GetRevAuthors(arg_ProjectName, arg_Subprojects):
    
    # save current working dir
    tmpCurrentWorkDir = os.getcwd()
    
    logging.info("Generating Label View")
    
    # si viewprojecthistory --project=f:/MKS/MKS_db/EE0084_SOFTWARE/project.pj --rfilter=labeled --fields=labels
    tmp_PTC_Command  = "si viewprojecthistory --project="+ arg_ProjectName+ " --fields=revision,author"
  
    arg_out = fPTC_Util_ExecuteCommand(tmp_PTC_Command,fDefLabelViewQuery,"w")
    
    logging.info("si viewlabels performed")
    
    # return to original workdir
    os.chdir(tmpCurrentWorkDir)

    return arg_out
################################################################


################################################################
# get revision dates of revs in PTC
################################################################
def fPTC_Util_GetRevDescriptions(arg_ProjectName, arg_Subprojects):
    
    # save current working dir
    tmpCurrentWorkDir = os.getcwd()
    
    logging.info("Generating Label View")
    
    # si viewprojecthistory --project=f:/MKS/MKS_db/EE0084_SOFTWARE/project.pj --rfilter=labeled --fields=labels
    tmp_PTC_Command  = "si viewprojecthistory --project="+ arg_ProjectName+ " --fields=revision,description"
  
    arg_out = fPTC_Util_ExecuteCommand(tmp_PTC_Command,fDefLabelViewQuery,"w")
    
    logging.info("si viewlabels performed")
    
    # return to original workdir
    os.chdir(tmpCurrentWorkDir)

    return arg_out
################################################################

################################################################
# get dev paths in PTC
################################################################
def fPTC_Util_GetDevPaths(arg_ProjectName, arg_Subprojects):
    
    # save current working dir
    tmpCurrentWorkDir = os.getcwd()
    
    logging.info("Generating Devpaths Infos")
    
    # si viewprojecthistory --project=f:/MKS/MKS_db/EE0084_SOFTWARE/project.pj --rfilter=labeled --fields=labels
    tmp_PTC_Command  = "si projectinfo --devpaths --project="+ arg_ProjectName
  
    arg_out = fPTC_Util_ExecuteCommand(tmp_PTC_Command,fDefLabelViewQuery,"w")

    devPathString =[]
    devPathListRevName =[]

    linefound = 0
    for line in arg_out:
       if (line.find("Associated Issues:") != -1):
            #Development Path found
            linefound = 2
       if (linefound == 1):
            devPathString.append(line)
       if (line.find("Development Paths:") != -1):
            #Development Path found
            linefound = 1
    logging.info("si viewdevpaths performed")
    
    if (len(devPathString)) > 0:
        for devPathEntry in devPathString:
            tmpRevision = devPathEntry[devPathEntry.find("(")+1:(devPathEntry.find(")"))]
            tmpDevPathName = devPathEntry[:devPathEntry.find("(")-1]
            devPathListEntry = str(tmpRevision) + "\t" + str(tmpDevPathName).lstrip(" ")
            devPathListRevName.append(devPathListEntry)

    # return to original workdir
    os.chdir(tmpCurrentWorkDir)

    return devPathListRevName
################################################################

################################################################
# calculate Proj Metrics
################################################################
def fPTC_CalcNView_ProjMetrics(arg_ProjectName, arg_Subprojects,argRevision):
    
    # save current working dir
    tmpCurrentWorkDir = os.getcwd()
    
    logging.info("Generating Devpaths Infos")
    
    #si calculateprojectmetrics --project=f:/mks/mks_db/EE0000_TESTPRJ/project.pj --projectRevision=1.2.1.2 --recomputeall
    # tmp_PTC_Command  = "si calculateprojectmetrics --project="+arg_ProjectName+" --projectRevision="+argRevision+" --recomputeall"
  
    # arg_out = fPTC_Util_ExecuteCommand(tmp_PTC_Command,fDefLabelViewQuery,"w")

    #si viewprojectmetrics --project=f:/mks/mks_db/EE0000_TESTPRJ/project.pj --projectRevision=1.2.1.2 --fields=metric,value

    tmp_PTC_Command  = "si viewprojectmetrics --project="+arg_ProjectName+" --projectRevision="+argRevision+" --fields=metric,value"
    
    arg_out = fPTC_Util_ExecuteCommand(tmp_PTC_Command,fDefLabelViewQuery,"w")

    if len(arg_out) < 2:    #no real calculation performed -> trigger calculation
            #tmp_PTC_Command  = "si calculateprojectmetrics --project="+arg_ProjectName+" --projectRevision="+argRevision+" --recomputeall"
            tmp_PTC_Command  = "si calculateprojectmetrics --project="+arg_ProjectName+" --projectRevision="+argRevision
            print ("   ... recalculating metrics of "+arg_ProjectName+" with revision "+argRevision)
            arg_out = fPTC_Util_ExecuteCommand(tmp_PTC_Command,fDefLabelViewQuery,"w")
            # and view metrics results again
            tmp_PTC_Command  = "si viewprojectmetrics --project="+arg_ProjectName+" --projectRevision="+argRevision+" --fields=metric,value"
            arg_out = fPTC_Util_ExecuteCommand(tmp_PTC_Command,fDefLabelViewQuery,"w")

    os.chdir(tmpCurrentWorkDir)

    return arg_out
################################################################




################################################################
# generate sandbox based on label in PTC
################################################################
def fPTC_Util_GenSandbox(arg_ProjectName, arg_Subprojects):
    
    # save current working dir
    tmpCurrentWorkDir = os.getcwd()
    
    logging.info("Generating Sandbox View")
    
    # si viewprojecthistory --project=f:/MKS/MKS_db/EE0084_SOFTWARE/project.pj --rfilter=labeled --fields=labels
    ## tmp_PTC_Command  = "si viewprojecthistory --project="+ arg_ProjectName+ " --rfilter=labeled --fields=labels"
  
    ## si createsandbox -R --project=f:/MKS/MKS_DB/EE0084_SOFTWARE/project.pj  --projectRevision="EE0084_E92_FS_0210" .\EE0084_Software\EE0084_E92_FS_0210

    tmp_PTC_Command = r"si createsandbox -R --project=f:/MKS/MKS_DB/EE0084_SOFTWARE/project.pj  --projectRevision=\"EE0084_E92_FS_0210\" .\EE0084_Software\EE0084_E92_FS_0210"
    arg_out = fPTC_Util_ExecuteCommand(tmp_PTC_Command,fDefLabelViewQuery,"w")
    
    logging.info("si gen Sandbox performed")
    
    # return to original workdir
    os.chdir(tmpCurrentWorkDir)

    return arg_out
################################################################


#revisionDict ={
#
#'1.1': {'date':"",'author':"",'description':"",'labels':["label1"],'devpathstart':["devpath"]}
#}

revisionDict ={}



################################################################
# find Out Revision Label Description from overall revision status 
# and return stringList with lines of Label Description
################################################################
def fPTC_Util_PatchRevisionDictElement(argRevDescriptions):

    stringTest = []    
    for count in range (0,len(argRevDescriptions)):
        tmpRevDescr =  argRevDescriptions[count]                       
        x = re.findall("^[0123456789.]+\t", tmpRevDescr)
        if len(x)!=0:
            lineComplete = str('')
            partString = tmpRevDescr.replace(x[0],"")

            finish = False
            index = 0

            while (finish==False):

                    if ((count+index +1)< len(argRevDescriptions)):
                        nextLine = argRevDescriptions[count+1+index]
                    else:
                        finish = True
                        nextLine = ""

                    if len(re.findall("^[0123456789.]+\t", nextLine))==0:
                        partString = partString+"\n"+nextLine
                        index = index + 1
                    else:
                        finish = True

            lineComplete = str(x[0]) + str(partString)

            stringTest.append(lineComplete)

    return (stringTest)

################################################################
# read Out Repo List
################################################################
def fPTC_Util_ReadRepoList(argFile):
    
    filelist = open(argFile,'r')
    argOut = filelist.read()
    filelist.close()

    return argOut
################################################################

################################################################
# read Out Project List
################################################################
def fPTC_Util_updateBranchDescriptions(argRevDict):
    for RevEntry in argRevDict:
            tmpPointRevNumber = argRevDict[RevEntry]['rev']
            tmpShortRevNumber = argRevDict[RevEntry]['rev'].split('.')
            tmpBranchName = argRevDict[RevEntry]['branch name']
            tmpProjShort= argRevDict[RevEntry]['proj']

            higherBranchRevNumber = ""

            if len(tmpShortRevNumber)>2:
                
                for i in range (len(tmpShortRevNumber)-2):
                    if i != 0:
                        tmpPoint = '.'
                    else:
                        tmpPoint = ''
                    higherBranchRevNumber = higherBranchRevNumber + tmpPoint + tmpShortRevNumber[i]
                    
                tmpDevPathIndex = int(tmpShortRevNumber[len(tmpShortRevNumber)-2])-1
                tmpIndex=tmpProjShort+'_'+higherBranchRevNumber
                try:
                   argRevDict[RevEntry]['branch name']=argRevDict[tmpIndex]['devpathstart'][tmpDevPathIndex]
                except:
                   argRevDict[RevEntry]['branch name']="branch without name/devpath"



def fPTC_Util_updateCalculationScheme(argRevDict):
    for RevEntry in argRevDict:
            tmpNoOfFilesFolder = int(argRevDict[RevEntry].get('subs',0))+int(argRevDict[RevEntry].get('text',0))+int(argRevDict[RevEntry].get('binary',0))
            tmpNoOfBytes = int(argRevDict[RevEntry].get('characters',0))+int(argRevDict[RevEntry].get('bytes',0))
            fPTC_Util_UpdateRevisionDictElement(RevEntry,'NoOfFilesFolders',(tmpNoOfFilesFolder))
            fPTC_Util_UpdateRevisionDictElement(RevEntry,'NoOfBytes',(tmpNoOfBytes))


################################################################






################################################################
# calculate Proj Metrics
################################################################
def fPTC_Util_CheckpointProject(arg_ProjectName, arg_LabelText,arg_Description):

    logging.info("Generating Checkpoint Descriptions")

     ## si checkpoint --project=f:/mks/mks_db/pkit_mks/ED0047_TEST/project.pj --label="TERMINATION_CP_BEFORE_MKS_MIGRATION" --description="TERMINATION_CHECKPOINT. DO NOT FURTHER WORK ON THIS MASTER OR BRANCH" --"state=green" --forceConfirm=yes
    tmp_PTC_Command  = "si checkpoint --project=\""+arg_ProjectName+"\" --label=\""+arg_LabelText+"\" --description=\""+arg_Description+"\" --state=\"green\" --forceConfirm=yes" 
    
    arg_out = fPTC_Util_ExecuteCommand(tmp_PTC_Command,fDefLabelViewQuery,"w")


################################################################
# calculate Proj Metrics
################################################################
def fPTC_CalcNView_ProjMetrics(arg_ProjectName, arg_Subprojects,argRevision):
    
    # save current working dir
    tmpCurrentWorkDir = os.getcwd()
    
    logging.info("Generating Devpaths Infos")
    
    #si calculateprojectmetrics --project=f:/mks/mks_db/EE0000_TESTPRJ/project.pj --projectRevision=1.2.1.2 --recomputeall
    # tmp_PTC_Command  = "si calculateprojectmetrics --project="+arg_ProjectName+" --projectRevision="+argRevision+" --recomputeall"
  
    # arg_out = fPTC_Util_ExecuteCommand(tmp_PTC_Command,fDefLabelViewQuery,"w")

    #si viewprojectmetrics --project=f:/mks/mks_db/EE0000_TESTPRJ/project.pj --projectRevision=1.2.1.2 --fields=metric,value

    tmp_PTC_Command  = "si viewprojectmetrics --project="+arg_ProjectName+" --projectRevision="+argRevision+" --fields=metric,value"
    
    arg_out = fPTC_Util_ExecuteCommand(tmp_PTC_Command,fDefLabelViewQuery,"w")

    if len(arg_out) < 2:    #no real calculation performed -> trigger calculation
            #tmp_PTC_Command  = "si calculateprojectmetrics --project="+arg_ProjectName+" --projectRevision="+argRevision+" --recomputeall"
            tmp_PTC_Command  = "si calculateprojectmetrics --project="+arg_ProjectName+" --projectRevision="+argRevision
            print ("   ... recalculating metrics of "+arg_ProjectName+" with revision "+argRevision)
            arg_out = fPTC_Util_ExecuteCommand(tmp_PTC_Command,fDefLabelViewQuery,"w")
            # and view metrics results again
            tmp_PTC_Command  = "si viewprojectmetrics --project="+arg_ProjectName+" --projectRevision="+argRevision+" --fields=metric,value"
            arg_out = fPTC_Util_ExecuteCommand(tmp_PTC_Command,fDefLabelViewQuery,"w")

    os.chdir(tmpCurrentWorkDir)

    return arg_out
################################################################



################################################################
#  Generate Proj Revision List from Revision Dictionary
################################################################
def fPTC_Util_GenerateProjRevisionList(argRevDict,argFile):

    filelist = open(argFile,'w')

    for RevEntry in argRevDict:
            #f:/MKS/MKS_db/EE0084_SOFTWARE/project.pj
            tmpProj = r"f:/MKS/MKS_db/"+argRevDict[RevEntry]['proj']+r"/project.pj"
            tmpRev  = argRevDict[RevEntry]['rev']
            filelist.write(tmpProj+";"+tmpRev+'\n')
    
    filelist.close()            

def fPTC_Util_GenerateSandboxesAccordingRevLog(argRevLog,argRootPath):
        #first read RevLog
        filelist = open(argRevLog,'r')
        tmpReposRevList = filelist.read()
        filelist.close()

        tmpReposRevListLines = tmpReposRevList.split('\n')

        for tmpEntry in tmpReposRevListLines:
            tmpLine=tmpEntry.split(';')
            if (len(tmpLine) == 2):
                       tmpMKSProj=tmpLine[0]
                       tmpMKSProjShort=tmpMKSProj[tmpMKSProj.find(r"f:/MKS/MKS_DB/")+14:(tmpMKSProj.find(r"/project.pj"))]
                       tmpMKSRev=tmpLine[1]
                       ## si createsandbox -R --project=f:/MKS/MKS_DB/EE0084_SOFTWARE/project.pj  --projectRevision="EE0084_E92_FS_0210" .\EE0084_Software\EE0084_E92_FS_0210
                       tmp_PTC_Command = r"si createsandbox -R --project="+tmpMKSProj+" --projectRevision="+tmpMKSRev+" "+argRootPath+tmpMKSProjShort+'/'+tmpMKSRev
                       print ("Fetching MKS Project "+tmpMKSProj+" with revision: "+tmpMKSRev)
                       arg_out = fPTC_Util_ExecuteCommand(tmp_PTC_Command,fDefLabelViewQuery,"w")


def fPTC_Util_GetSandbox(argProj,argRev,argPath):

       ## si createsandbox -R --project=f:/MKS/MKS_DB/EE0084_SOFTWARE/project.pj  --projectRevision="EE0084_E92_FS_0210" .\EE0084_Software\EE0084_E92_FS_0210
       
       tmpCreationPath = argPath+"/"+argRev
       tmp_PTC_Command = r"si createsandbox -R --project="+argProj+" --projectRevision="+argRev+" "+tmpCreationPath
       print ("Fetching MKS Project "+argProj+" with revision: "+argRev)
       arg_out = fPTC_Util_ExecuteCommand(tmp_PTC_Command,fDefLabelViewQuery,"w")

       return (arg_out)



################################################################
# patch single Element in global Dictionary revisionDict
#  SearchToken like 1.2 is argRevDictToken
#  Key is argRevElementKey
#  new Value is argRevValue
################################################################
def fPTC_Util_UpdateRevisionDictElement(argRevDictToken, argRevElementkey,argRevValue):
    
    try:
        myTmpCopy = revisionDict[argRevDictToken].copy()

        #myTmpCopy[argRevElementkey]=argRevValue
        
        if argRevElementkey not in myTmpCopy.keys():
            myTmpCopy[argRevElementkey]=0

        if type(myTmpCopy[argRevElementkey]) is list:
            myTmpCopy[argRevElementkey].append(argRevValue)
        else:
            myTmpCopy[argRevElementkey]=argRevValue
    
        revisionDict[argRevDictToken].update(myTmpCopy)

        argOut = 0
    
    except:
        argOut = -1

    return argOut
################################################################


#globProj = "f:/MKS/MKS_DB/EE0084_SOFTWARE/project.pj"
#globProj = "f:/MKS/MKS_DB/EE0291_VW_MQB2020_SBA/project.pj"
globProj = "f:/MKS/MKS_DB/EE0000_TESTPRJ/project.pj"


#revisionDict ={
#    '1.1': {'date':"",'author':"",'description':"",'labels':["label1"],'devpathstart':["devpath"]}
#}


################################################################
# Function: main                                               #
# main                                                         #
################################################################
 
def main():
                       
 fPTC_Util_initLogging()


 tmpProjList = fPTC_Util_ReadRepoList("ptc_ProjRevLog.txt")

 tmpProjListSep = tmpProjList.split('\n')

 for tmpFetchEntry in tmpProjListSep:
     tmpFetchList = tmpFetchEntry.split(';')
     if len(tmpFetchList)==2:
        
        tmpProj = tmpFetchList[0]
        tmpRev  = tmpFetchList[1]
        tmpMKSProjShort=tmpProj[tmpProj.find(r"f:/MKS/MKS_DB/")+15:(tmpProj.find(r"/project.pj"))]
        tmpMKSProjShort=r"./"+tmpMKSProjShort.replace('/','_')
        tmpMKSProjLong= r"C:/UserData/MKSMigra/"+tmpMKSProjShort
        fPTC_Util_GetSandbox(tmpProj,tmpRev,tmpMKSProjLong)

 
 if False:
   for currentScanProj in tmpProjListSep:
               globProj = currentScanProj
               print ("Checkpointing "+currentScanProj+" ...")
               fPTC_Util_CheckpointProject(globProj,"TERMINATION_CP_BEFORE_MKS_MIGRATION","TERMINATION_CHECKPOINT. DO NOT FURTHER WORK ON THIS MASTER OR BRANCH")

 
 if False:
  for currentScanProj in tmpProjListSep:
               globProj = currentScanProj
               
               tmp_Labels = fPTC_Util_Viewlabels(globProj,"")
               tmpRevLabels = fPTC_Util_GetRevlabels(globProj,"")
               tmpRevDates = fPTC_Util_GetRevDates(globProj,"")
               tmpRevAuthors = fPTC_Util_GetRevAuthors(globProj,"")
               tmpRevDescriptions = fPTC_Util_GetRevDescriptions(globProj,"")
               tmpDevPaths = fPTC_Util_GetDevPaths(globProj,"")

               print ("Scanning MKS History of "+currentScanProj+" ...")
               ## todo über projectinfo die devpaths Infos abfragen tmpRevDevPathInfos = fPTC_Util_GetDevPathInfos("f:/MKS/MKS_DB/EE0084_SOFTWARE/project.pj","")
   
               
               currentDate=datetime.date.today()
               currentCalString = currentDate.strftime("%Y-%m-%d")

               tmpProjName = globProj[globProj.find(r"f:/MKS/MKS_DB/")+14:(globProj.find(r"/project.pj"))]

              

               for tmpLabel in tmpRevLabels:
                   tmpLabels=tmpLabel.split("\t")
                   if (len(tmpLabels) == 2):
                       tmpShortRev=tmpLabels[0]
                       tmpRev=tmpProjName+"_"+tmpLabels[0]
                       tmpLabNum=tmpLabels[1]
                       if len(tmpShortRev.split('.')) == 2:
                         tmpBranchName="master"
                       else:
                         tmpBranchName="branch"   
                       revisionDict.update( {tmpRev: {'proj':tmpProjName,'rev':tmpShortRev,'branch name':tmpBranchName,'date':"",'dateday':currentCalString,\
                        'author':"",'description':"",'labels':tmpLabNum,'devpathstart':[],'NoOfFilesFolders':0,'NoOfBytes':0}})
                        
                       tmpMetrics=fPTC_CalcNView_ProjMetrics(globProj,"",tmpShortRev)
                       for tmpMetric in tmpMetrics:
                           tmpMetricLine = tmpMetric.split("\t")
                           if (len(tmpMetricLine) == 2):
                               fPTC_Util_UpdateRevisionDictElement(tmpRev,tmpMetricLine[0],int(tmpMetricLine[1]))


               for tmpLabel in tmpRevDates:
                   tmpLabels=tmpLabel.split("\t")
                   if (len(tmpLabels) == 2):
                       tmpRev=tmpProjName+"_"+tmpLabels[0]
                       tmpLabNum=tmpLabels[1]
                       fPTC_Util_UpdateRevisionDictElement (tmpRev,'date',tmpLabNum)
                       updatedDate=datetime.datetime.strptime(tmpLabNum, '%d.%m.%Y %H:%M:%S')
                       updatedCalString = updatedDate.strftime("%Y-%m-%d")
                       #fPTC_Util_UpdateRevisionDictElement(tmpRev,'datetime',(updatedDate))
                       fPTC_Util_UpdateRevisionDictElement(tmpRev,'dateday',(updatedCalString))
                       
               for tmpLabel in tmpRevAuthors:
                   tmpLabels=tmpLabel.split("\t")
                   if (len(tmpLabels) == 2):
                       tmpRev=tmpProjName+"_"+tmpLabels[0]
                       tmpLabNum=tmpLabels[1]
                       fPTC_Util_UpdateRevisionDictElement (tmpRev,'author',tmpLabNum)
               
               tmpRevDescriptionsConverted = fPTC_Util_PatchRevisionDictElement(tmpRevDescriptions)

               for tmpLabel in tmpRevDescriptionsConverted:
                   tmpLabels=tmpLabel.split("\t")
                   if (len(tmpLabels) == 2):
                       tmpRev=tmpProjName+"_"+tmpLabels[0]
                       tmpLabNum=tmpLabels[1]
                       fPTC_Util_UpdateRevisionDictElement (tmpRev,'description',tmpLabNum)

               for tmpLabel in tmpDevPaths:
                   tmpLabels=tmpLabel.split("\t")
                   if (len(tmpLabels) == 2):
                       tmpRev=tmpProjName+"_"+tmpLabels[0]
                       tmpLabNum=tmpLabels[1]
                       fPTC_Util_UpdateRevisionDictElement (tmpRev,'devpathstart',tmpLabNum)

              # tmpSheetDataFrame = pandas.DataFrame(revisionDict).T  # transpose to look in Excel Format
              # tmpProjName=tmpProjName.replace('/','_')
              # tmpSheetDataFrame.to_csv(tmpProjName+".csv")
              # tmpSheetDataFrame.to_excel(tmpProjName+".xlsx")
              # fPTC_Util_GenerateProjRevisionList(revisionDict,tmpProjName+".txt")


# fPTC_Util_updateBranchDescriptions (revisionDict)
# fPTC_Util_updateCalculationScheme (revisionDict)


# tmpSheetDataFrame = pandas.DataFrame(revisionDict).T  # transpose to look in Excel Format
# tmpSheetDataFrame.to_csv("ptc_ProjRevSheet.csv")
# tmpSheetDataFrame.to_excel("ptc_ProjRevSheet.xlsx")

# fPTC_Util_GenerateProjRevisionList(revisionDict,"ptc_ProjRevLog.txt")

 #   fPTC_Util_GenerateSandboxesAccordingRevLog(r"ptc_ProjRevLog.txt",r"c:/userData/MKS_MigProj/")

 logging.info("Script is done!")
	
 sys.exit(0)
#################################################################	



################################################################
# Function: fPTC_Util_Terminate                                #
# In case of problems end script                               #
################################################################ 
def fPTC_Util_Terminate():
    
    logging.error("Script terminated: Unable to continue, terminating...")

    # exit program with return code for a fail
    sys.exit(1)
################################################################

    
################################################################
# call the main function after parsing all of this script      #
################################################################ 
if __name__=="__main__":
    main()
################################################################	
	
	
