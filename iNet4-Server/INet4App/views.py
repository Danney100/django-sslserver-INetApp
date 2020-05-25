# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.db import connections
from django.http import HttpResponse
import json
import os



def Login(request):
     return render(request, 'Authenticate.html')


def HomePage(request):
    if request.method == 'POST':
        author_id = request.POST['author_id']
        password = request.POST['password']
        location = request.POST['location']
        JobsResult = []
        secretaryR = []

        User_name = "Author"
        WTs = "all"
        Depts = "all"
        Exc = "all"
        Dates = "all"
        LoggedInAs = ""
        Status = "InQueue"
        # System Settings - Defaults
        sys_sub = "Subject"
        sys_wt = "Worktype"
        sys_dept = "Department"
        sys_typ = "Typist"


        if author_id == "":
            return render(request, "login-Unknown.html")

        if password == "":
            return render(request, "login-MustPassword.html")


        if location == "":
            location = "0"

        returnstring = login_valid(author_id, password, location)

# -----------Testing --------------------------
        #WTs = returnString

        # if returnString == "[]":
        #     return render(request, "login-Unknown.html")

        if (returnstring == "none" or returnstring == "[]"):
            #if that = "none" then there are no typists.
            # This was in one routine... but I was having so much trouble I split them in two.
            # Now chech for a valid author

            if password == "":
                return render(request, "login-MustPassword.html")

            returnString1 = login_Author(author_id, password, location)
            validUser = False
            User_name = "Author"
            User_type = "author"

#-----------Testing --------------------------
            #WTs = returnString1


            if returnString1 == "[]":
                return render(request, "login-Unknown.html")

            if returnString1 == "none":
                return render(request, "login-unknown.html")
            else:   #This is an author, get his name... that's about it
                validUser = True
                # typistData = json.loads(returnString1)
                # User_name = typistData["namelast"]

        else:   #This is a Typist Load Typist data from json
            User_name = "Typist"
            User_type = "typist"
            validUser = True
            Exc = author_id
            #
            # typistData = json.loads(returnstring)
            #
            # User_name = typistData["NameLast"]
            # WTs = typistData["WTLock"]
            # Depts = typistData["DeptLock"]
            # Title = typistData["Title"]
            # Exc = author_id

            # soloMode = typistData["Title"]
            # SoloAuthorData  = typistData["Title"]
            # SoloTypistData = typistData["Title"]

            if WTs == "":
                WTs = "all"
            if Depts == "":
                Depts = "all"
            #Exc = "all"



#-------Just for testing#----------------------------------------------------------------------------------------------
        #User_name = "Author"
        #User_type = "author"
        #User_type = "typist"
        #WTs = returnString
        #Exc = "901"
        #validUser = True


        if validUser:
            with connections['VS_FileMgmt'].cursor() as cursor:
                if User_type == "typist":
                    # SQLString = "select AuthorNameLast, JobNumber, Subject, Worktype, Secretary, AuthorNameLast, Department, DateDictation, TimeDictation, DateTranscription,TimeTranscription, Length, Location, SystemID, substr(FileName,25) as subFname, FileStatus, Priority, AuthorUserId, TransNameLast, Marked, DragonTranscribedText from FilesActive WHERE Location = '" + location +"' AND FileStatus IN('e','s')"
                    SQLString = "select AuthorNameLast, JobNumber, Subject, Worktype, Secretary, AuthorNameLast, Department, DateDictation, TimeDictation, DateTranscription,TimeTranscription, Length, Location, SystemID, substr(FileName,25) as subFname, FileStatus, Priority, AuthorUserId, TransNameLast, Marked, DragonTranscribedText from FilesActive WHERE Location = '" + location +"' AND FileStatus IN('e','s','t') "
                    SQLString = SQLString + " AND Secretary = '" + Exc + "'"
                    SQLString = SQLString + " Order By JobNumber Desc"

                    # if WTs != "all":
                    #     SQLString = SQLString + " AND WorkType IN('" + WTs + "') "
                    #
                    # if Depts != "all":
                    #     SQLString = SQLString + " AND Department IN('" + Depts + "') "

                else:
                    SQLString = "select AuthorNameLast, JobNumber, Subject, Worktype, Secretary, AuthorNameLast, Department, DateDictation, TimeDictation, DateTranscription,TimeTranscription, Length, Location, SystemID, substr(FileName,25) as subFname, FileStatus, Priority, AuthorUserId, TransNameLast, Marked, DragonTranscribedText from FilesActive WHERE Location = '" + location +"' AND AuthorUserId = " + author_id

                cursor.execute(SQLString)
                Cola = [col[0] for col in cursor.description]
                JobsResult = [
                    dict(zip(Cola, row))
                    for row in cursor.fetchall()
                ]

            with connections['VS_SystemMgmt'].cursor() as cursor:
                cursor.execute("select UserID, NameLast from Transcriptionists WHERE Location = '" + location + "'")
                columns = [col[0] for col in cursor.description]
                secretaryR = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]

        return render(request, "HomePage.html",
                      {
                          "rows": JobsResult,
                          "author_id": author_id,
                          "SelectExeclusiveList": secretaryR,
                          "WTs": WTs,
                          "Exc": Exc,
                          "Depts": Depts,
                          "Dates": Dates,
                          "User_name": User_name,
                          "User_type": User_type,
                          "Status": Status,
                          "location": location,

                          "sys_sub": sys_sub,
                          "sys_wt": sys_wt,
                          "sys_dept": sys_dept,
                          "sys_typ": sys_typ

                      })

# def HomePage(request):
#     if request.method == 'POST':
#         author_id = request.POST['author_id']
#         password = request.POST['password']
#         location = request.POST['location']
#         JobsResult = []
#         secretaryR = []
#
#         if location == "":
#             location = "0"
#
#         returnString = login_valid(author_id, password, location)
#
#         validUser = True
#         # if returnString == "none":
#         #     validUser = False
#         #     return render(request, "login-Unknown.html")
#
#         validUser = True
#         if validUser:
#             # " And Worktype='2'"
#             with connections['VS_FileMgmt'].cursor() as cursor:
#                 cursor.execute("select AuthorNameLast, JobNumber, Subject, Worktype, Secretary, AuthorNameLast, Department, DateDictation, TimeDictation, DateTranscription,TimeTranscription, Length, Location, SystemID, substr(FileName,25) as subFname, FileStatus, Priority, AuthorUserId, TransNameLast, Marked, DragonTranscribedText from FilesActive WHERE AuthorUserId = " + author_id)
#                 #cursor.execute("select AuthorNameLast, JobNumber, Subject, Worktype, Secretary, AuthorNameLast, Department, DateDictation, TimeDictation, DateTranscription,TimeTranscription, Length, Location, SystemID, substr(FileName,25) as subFname, FileStatus, Priority, AuthorUserId, TransNameLast, Marked, DragonTranscribedText from FilesActive")
#                 Cola = [col[0] for col in cursor.description]
#                 JobsResult = [
#                     dict(zip(Cola, row))
#                     for row in cursor.fetchall()
#                 ]
#
#             with connections['VS_SystemMgmt'].cursor() as cursor:
#                 cursor.execute("select UserID, NameLast from Transcriptionists WHERE Location = '" + location + "'")
#                 columns = [col[0] for col in cursor.description]
#                 secretaryR = [
#                     dict(zip(columns, row))
#                     for row in cursor.fetchall()
#                 ]
#
#
#         return render(request, "HomePage.html",
#                       {
#                           "rows": JobsResult,
#                           "author_id": author_id,
#                           "SelectExeclusiveList": secretaryR,
#                           "WTs": ""
#                       })


def ReturnJob(request):
    if request.method == 'POST':
        Jnom = request.POST['jnom']
        AuID = request.POST['AuID']
        AutherInput = request.POST['AutherInput']
        WorktypeInput = request.POST['WorktypeInput']
        DeptInput = request.POST['DeptInput']
        SelectedStatus = request.POST['SelectedStatus']
        SelectedExclusive = request.POST['SelectedExclusive']
        filter_dic = {
            "AuthInput": AutherInput,
            "WT": WorktypeInput,
            "Dept": DeptInput,
            "SelectedSt": SelectedStatus,
            "SelectedEx": SelectedExclusive,
            "AuID": AuID
        }
        str_execution = "Update FilesActive set FileStatus = 'e' where JobNumber = " + Jnom
        return HttpResponse(refreshTable(str_execution, filter_dic))


def SavingJob(request):
    if request.method == 'POST':
        Jnom = request.POST['jnom']
        AuID = request.POST['AuID']
        AutherInput = request.POST['AutherInput']
        WorktypeInput = request.POST['WorktypeInput']
        DeptInput = request.POST['DeptInput']
        SelectedStatus = request.POST['SelectedStatus']
        SelectedExclusive = request.POST['SelectedExclusive']
        Audioduration = request.POST['Audioduration']
        filter_dic = {
            "AuthInput": AutherInput,
            "WT": WorktypeInput,
            "Dept": DeptInput,
            "SelectedSt": SelectedStatus,
            "SelectedEx": SelectedExclusive,
            "AuID": AuID
        }
        str_execution = "Update FilesActive set FileStatus = 's', SavedOffset = " + Audioduration +" where JobNumber = " + Jnom
        return HttpResponse(refreshTable(str_execution, filter_dic))




    #JobCompleted = request.POST['JobCompleted']

def SignJobout(request):
    if request.method == 'POST':
        SJID = request.POST['SJID']
        AuID = request.POST['AuID']
        AutherInput = request.POST['AutherInput']
        WorktypeInput = request.POST['WorktypeInput']
        DeptInput = request.POST['DeptInput']
        SelectedStatus = request.POST['SelectedStatus']
        SelectedExclusive = request.POST['SelectedExclusive']
        JStatus = request.POST['JStatus']
        Location = request.POST['Location']
        FSOName = request.POST['FSOName']
        filter_dic = {
            "AuthInput": AutherInput,
            "WT": WorktypeInput,
            "Dept": DeptInput,
            "SelectedSt": SelectedStatus,
            "SelectedEx": SelectedExclusive,
            "AuID": AuID
        }

        signOutResult = db_Signout(SJID,"Typist",AuID,FSOName,JStatus,Location)

        if signOutResult == 0:
            #the job is already taken by another
            x = refreshTable("NoUpdate", filter_dic)

            offsetAudio = '[{"SavedOffset":"File_Already_Taken"}]'
            returnVals = [offsetAudio, x]
            return HttpResponse(returnVals)

        # Or we have the job...
        #Already Done. str_execution = "Update FilesActive set FileStatus = 't' where JobNumber=" + SJID

        if JStatus == "Saved":
            str_exec2 = "Select SavedOffset from FilesActive where JobNumber=" + SJID
            with connections['VS_FileMgmt'].cursor() as cursor:
                cursor.execute(str_exec2)
                columns = [col[0] for col in cursor.description]
                offsetAudio = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
            offsetAudio = json.dumps(offsetAudio)
        else:
            offsetAudio = '[{"SavedOffset":"0"}]'

        x = refreshTable("NoUpdate", filter_dic)
        # x = refreshTable(str_execution, filter_dic)

        returnVals = [offsetAudio, x]
        return HttpResponse(returnVals)




def CompleteJob(request):
    if request.method == 'POST':
        Jnom = request.POST['jnom']
        AuID = request.POST['AuID']
        AutherInput = request.POST['AutherInput']
        WorktypeInput = request.POST['WorktypeInput']
        DeptInput = request.POST['DeptInput']
        SelectedStatus = request.POST['SelectedStatus']
        SelectedExclusive = request.POST['SelectedExclusive']
        filter_dic = {
            "AuthInput": AutherInput,
            "WT": WorktypeInput,
            "Dept": DeptInput,
            "SelectedSt": SelectedStatus,
            "SelectedEx": SelectedExclusive,
            "AuID": AuID
        }
        str_execution = "Update FilesActive set FileStatus = 'c' where JobNumber = " + Jnom
        return HttpResponse(refreshTable(str_execution, filter_dic))


# def login_valid(Id, password, location):
#     return True

# def login_valid(user_id, password, location):
#     returnString = "none"
#     LocationIn = " AND (Location = '" + location + "' OR Location LIKE '%," + location + "' OR Location LIKE '" + location + ",%' OR Location LIKE '%," + location + ",%')"
#     #SQLString = "Select Userid, NameLast, Title, ExclusiveFlag, Categoryflag, SpecificFlag, FifoFlag, SavedFlag, AuthorIdFlag, WorktypeFlag, DepartmentFlag, SubjectFlag, DocumentNumberFlag, NameFirst, CategoryAccessibleCategories, ReviewModeFlag, WTLock, DeptLock, iNetMark, iNetExport, DocumentNumberExcAsgIgnore, SoloMode, SoloTransData, SoloAuthorData, PasswordRequired, eMailNotification, email, NameMid, NavAllowAddAuthors, NavAllowAddTypists, NavAllowAddCategory, NavChannels, NavKeymaps, NavSystem, DragonVocab, AuthorIDExcAsgIgnore, WorktypeExcAsgIgnore, SubjectExcAsgIgnore, DepartmentExcAsgIgnore, DocumentNumbersToSkip FROM Transcriptionists WHERE UserID = '" + user_id + "' " & LocationIn
#     SQLString = "Select Title, WTLock, DeptLock, SoloMode, SoloTransData, SoloAuthorData, Categoryflag, CategoryAccessibleCategories, iNetMark, iNetExport, DragonVocab FROM Transcriptionists WHERE UserID = '" + user_id + "' AND NameFirst = '" + password + "' " + LocationIn
#     with connections['VS_SystemMgmt'].cursor() as cursor:
#         cursor.execute(SQLString)
#         # columns = [col[0] for col in cursor.description]
#         # results = [
#         #     dict(zip(columns, row))
#         #     for row in cursor.fetchall()
#         # ]
#
#         result_set = cursor.fetchone()
#         if result_set is None:
#             returnString = "none"
#         else:
#             for row in result_set:
#                 #print "%s, %s, %s, %s, %s" % (row["SoloMode"], row["SoloTransData"], row["SoloAuthorData"], row["WTLock"], row["DeptLock"])
#                 returnString = "Typist" #"%s, %s, %s, %s" % (row["SoloTransData"], row["SoloAuthorData"], row["WTLock"], row["DeptLock"])
#
#         #PrivateDb and 2Factor
#         # pass result back to post to page
#
#        #If there are values... return the dict via passBackDict?
#     return returnString


# def job_Available(jobNum, status, location):
#     returnString = "none"
#     LocationIn = " AND (Location = '" + location + "' OR Location LIKE '%," + location + "' OR Location LIKE '" + location + ",%' OR Location LIKE '%," + location + ",%')"
#     SQLString = "Select Title, UserID, NameLast FROM Authors WHERE UserID = '" + user_id + "'  AND (NameFirst = '" + password + "'  or NameFirst IS NULL) " + LocationIn
#
#     # Title, NameLast, DragonVocab
#     with connections['VS_SystemMgmt'].cursor() as cursor:
#         cursor.execute(SQLString)
#         columns = [col[0] for col in cursor.description]
#         results = [
#             dict(zip(columns, row))
#             for row in cursor.fetchall()
#         ]
#
#         if results is None:
#             return "none"
#         else:
#             return json.dumps(results)
#             # return "Typist"



def login_Author(user_id, password, location):
    returnString = "none"
    LocationIn = " AND (Location = '" + location + "' OR Location LIKE '%," + location + "' OR Location LIKE '" + location + ",%' OR Location LIKE '%," + location + ",%')"
    SQLString = "Select Title, UserID, NameLast FROM Authors WHERE UserID = '" + user_id + "'  AND (NameFirst = '" + password + "'  or NameFirst IS NULL) " + LocationIn

    # Title, NameLast, DragonVocab
    with connections['VS_SystemMgmt'].cursor() as cursor:
        cursor.execute(SQLString)
        columns = [col[0] for col in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        if results is None:
            return "none"
        else:
            return json.dumps(results)
            # return "Typist"


def login_valid(user_id, password, location):
    returnString = "none"
    LocationIn = " AND (Location = '" + location + "' OR Location LIKE '%," + location + "' OR Location LIKE '" + location + ",%' OR Location LIKE '%," + location + ",%')"
    #SQLString = "Select Userid, NameLast, Title, ExclusiveFlag, Categoryflag, SpecificFlag, FifoFlag, SavedFlag, AuthorIdFlag, WorktypeFlag, DepartmentFlag, SubjectFlag, DocumentNumberFlag, NameFirst, CategoryAccessibleCategories, ReviewModeFlag, WTLock, DeptLock, iNetMark, iNetExport, DocumentNumberExcAsgIgnore, SoloMode, SoloTransData, SoloAuthorData, PasswordRequired, eMailNotification, email, NameMid, NavAllowAddAuthors, NavAllowAddTypists, NavAllowAddCategory, NavChannels, NavKeymaps, NavSystem, DragonVocab, AuthorIDExcAsgIgnore, WorktypeExcAsgIgnore, SubjectExcAsgIgnore, DepartmentExcAsgIgnore, DocumentNumbersToSkip FROM Transcriptionists WHERE UserID = '" + user_id + "' " & LocationIn
    SQLString = "Select Title, WTLock, DeptLock, SoloMode, SoloTransData, SoloAuthorData, Categoryflag, CategoryAccessibleCategories, iNetMark, iNetExport, DragonVocab FROM Transcriptionists WHERE UserID = '" + user_id + "' AND (NameFirst = '" + password + "'  or NameFirst IS NULL) " + LocationIn
    with connections['VS_SystemMgmt'].cursor() as cursor:
        cursor.execute(SQLString)
        columns = [col[0] for col in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        if results is None:
            return "none"
            # returnString = "none"
        # elseif results == "[]":
        #     return "none"
        else:
            return json.dumps(results)
            #return "Typist"


def ListjobAjax(request):
    if request.method == 'POST':
        AutherInput = request.POST['AutherInput']
        WorktypeInput = request.POST['WorktypeInput']
        DeptInput = request.POST['DeptInput']
        SelectedStatus = request.POST['SelectedStatus']
        SelectedExclusive = request.POST['SelectedExclusive']
        author_id = request.POST['AuthID']

        location = "0"
        # if User_type == "typist":
        if (int(author_id) > 900 and int(author_id) < 990):
            SQLString = "select AuthorNameLast, JobNumber, Subject, Worktype, Secretary, AuthorNameLast, Department, DateDictation, TimeDictation, DateTranscription,TimeTranscription, Length, Location, SystemID, substr(FileName,25) as subFname, FileStatus, Priority, AuthorUserId, TransNameLast, Marked, DragonTranscribedText from FilesActive WHERE Location = '" + location + "'"
        else:
            SQLString = "select AuthorNameLast, JobNumber, Subject, Worktype, Secretary, AuthorNameLast, Department, DateDictation, TimeDictation, DateTranscription,TimeTranscription, Length, Location, SystemID, substr(FileName,25) as subFname, FileStatus, Priority, AuthorUserId, TransNameLast, Marked, DragonTranscribedText from FilesActive WHERE Location = '" + location + "' AND AuthorUserId = " + author_id

        str_execution = SQLString
        # str_execution = "select AuthorNameLast, JobNumber, Subject, Worktype, Secretary, AuthorNameLast, Department, DateDictation, TimeDictation, DateTranscription,TimeTranscription, Length, Location, SystemID, substr(FileName,25) as subFname , FileStatus, Priority, AuthorUserId, TransNameLast, Marked, DragonTranscribedText from FilesActive WHERE AuthorUserId = " + author_id
        if AutherInput:
            str_execution += " AND AuthorNameLast LIKE '" + AutherInput + "%'"
        if WorktypeInput:
            str_execution += " AND Worktype LIKE '" + WorktypeInput + "%'"
        if DeptInput:
            str_execution += " AND Department LIKE '" + DeptInput + "%'"
        if SelectedStatus:
            str_execution += " AND FileStatus LIKE '" + SelectedStatus + "%'"
        if SelectedExclusive:
            str_execution += " AND Secretary LIKE '" + SelectedExclusive + "%'"

        with connections['VS_FileMgmt'].cursor() as cursor:
            # cursor.execute(str_execution)
            # results = cursor.fetchall()
            cursor.execute(str_execution)
            columns = [col[0] for col in cursor.description]
            results = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
            x = json.dumps(results)
            return HttpResponse(x)


def refreshTable(update_exec, *args):
    AutherInput = args[0]['AuthInput']
    WorktypeInput = args[0]['WT']
    DeptInput = args[0]['Dept']
    SelectedStatus = args[0]['SelectedSt']
    SelectedExclusive = args[0]['SelectedEx']
    AuID = args[0]['AuID']
    #str_exec = "select AuthorNameLast, JobNumber, Subject, Worktype, Secretary, AuthorNameLast, Department, DateDictation, TimeDictation, DateTranscription,TimeTranscription, Length, Location, SystemID, substr(FileName,25) as subFname, FileStatus, Priority, AuthorUserId, TransNameLast, Marked, DragonTranscribedText from FilesActive WHERE AuthorUserId = " + AuID

    location = "0"
    # if User_type == "typist":
    if (int(AuID) > 900 and int(AuID) < 990):
        str_exec = "select AuthorNameLast, JobNumber, Subject, Worktype, Secretary, AuthorNameLast, Department, DateDictation, TimeDictation, DateTranscription,TimeTranscription, Length, Location, SystemID, substr(FileName,25) as subFname, FileStatus, Priority, AuthorUserId, TransNameLast, Marked, DragonTranscribedText from FilesActive WHERE Location = '" + location + "'"
    else:
        str_exec = "select AuthorNameLast, JobNumber, Subject, Worktype, Secretary, AuthorNameLast, Department, DateDictation, TimeDictation, DateTranscription,TimeTranscription, Length, Location, SystemID, substr(FileName,25) as subFname, FileStatus, Priority, AuthorUserId, TransNameLast, Marked, DragonTranscribedText from FilesActive WHERE Location = '" + location + "' AND AuthorUserId = " + AuID

    if AutherInput:
        str_exec += " AND AuthorNameLast LIKE '" + AutherInput + "%'"
    if WorktypeInput:
        str_exec += " AND Worktype LIKE '" + WorktypeInput + "%'"
    if DeptInput:
        str_exec += " AND Department LIKE '" + DeptInput + "%'"
    if SelectedStatus:
        str_exec += " AND FileStatus LIKE '" + SelectedStatus + "%'"
    if SelectedExclusive:
        str_exec += " AND Secretary LIKE '" + SelectedExclusive + "%'"
    with connections['VS_FileMgmt'].cursor() as cursor:
        if update_exec != "NoUpdate":
            cursor.execute(update_exec)
        cursor.execute(str_exec)

        columns = [col[0] for col in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
        x = json.dumps(results)
        return x

def db_Signout(SJID,UserName,AuID,fileName,FStatus,Location):
    # SJID = request.POST['SJID']
    # AuID = request.POST['AuID']
    # UserName = request.POST['UserName']
    # FStatus = request.POST['FStatus']

    if FStatus == "InQueue":
        FStatus = "e"
    if FStatus == "InTrans":
        FStatus = "t"
    if FStatus == "Completed":
        FStatus = "c"
    if FStatus == "Saved":
        FStatus = "s"

    ReturnableFilenameOnly = fileName
    FilenameOnly_SignedOut = fileName

    from datetime import datetime

    now = datetime.now()  # current date and time
    trans_date = now.strftime("%m/%d/%Y")
    trans_time = now.strftime("%H:%M:%S")
    trans_date_time = now.strftime("%m %d %Y %H %M %S")

    # TransDateTimeString = DateToEpoch(Now)
    # Now Reconstruct the FileName
    newfilename = ReturnableFilenameOnly

    # where is the org filename info
    LensPosition = newfilename.find("_")
    newfilename = newfilename[:LensPosition] + UserName + " " + AuID + " " + trans_date_time + ".t" + newfilename[-2:]

    # Job_Not_Available = false

    # SQLString = "Update FilesActive set FileStatus = 't', TransNameLast ='" + UserName + "', TransID ='" + AuID + "',  filename = '" + newfilename + "', TimeTranscription = '" + trans_time + "', DateTranscription = '" + trans_date + "'  where JobNumber=" + SJID + " AND FileStatus = '" + FStatus + "'"
    # if FStatus == "c": SQLString = "Update FilesActive set FileStatus = 't', filename = '" + newfilename + "'  where JobNumber=" + SJID + " AND FileStatus = '" + FStatus + "'"

    str_execution = "Update FilesActive set FileStatus = 't', TransNameLast ='" + UserName + "', TransUserID ='" + AuID + "', TimeTranscription = '" + trans_time + "', DateTranscription = '" + trans_date + "'  where JobNumber=" + SJID + " AND FileStatus = '" + FStatus + "' AND FileName LIKE '%" + fileName + "'"
    if FStatus == "c":
        str_execution = "Update FilesActive set FileStatus = 't', filename = '" + newfilename + "'  where JobNumber=" + SJID + " AND FileStatus = '" + FStatus + "' AND FileName LIKE '%" + fileName + "'"
    if FStatus == "s":
        str_execution = "Update FilesActive set FileStatus = 't', TransNameLast ='" + UserName + "', TransUserID ='" + AuID + "', TimeTranscription = '" + trans_time + "', DateTranscription = '" + trans_date + "'  where JobNumber=" + SJID + " AND FileStatus = '" + FStatus + "' AND FileName LIKE '%" + fileName + "' AND TransUserID ='" + AuID + "'"

    # str_execution = SQLString
    # str_execution with filename not yet implemented --for testing--but I didn't test it
    # str_execution = "Update FilesActive set FileStatus = 't', TransNameLast ='" + UserName + "', TransID ='" + AuID + "', TimeTranscription = '" + trans_time + "', DateTranscription = '" + trans_date + "'  where JobNumber=" + SJID + " AND FileStatus = '" + FStatus + "'"
    with connections['VS_FileMgmt'].cursor() as cursor:
        cursor.execute(str_execution)
        results = cursor.rowcount
        # # return HttpResponse('')
        # columns = [col[0] for col in cursor.description]
        # results = [
        #     dict(zip(columns, row))
        #     for row in cursor.fetchall()
        # ]

    return results;


#import os
# def SignJoboutNew(request):
#     if request.method == 'POST':
#         SJID = request.POST['SJID']
#         AuID = request.POST['AuID']
#
#         ReturnableFilenameOnly = request.POST['FileSignedOut']
#         FilenameOnly_SignedOut = request.POST['FileSignedOut']
#         UserName = request.POST['UserName']
#         FStatus = request.POST['FStatus']
#
#         from datetime import datetime
#
#         now = datetime.now()  # current date and time
#         trans_date = now.strftime("%m/%d/%Y")
#         trans_time = now.strftime("%H:%M:%S")
#         trans_date_time = now.strftime("%m %d %Y %H %M %S")
#
#         #TransDateTimeString = DateToEpoch(Now)
#         # Now Reconstruct the FileName
#         newfilename = ReturnableFilenameOnly
#
#         #where is the org filename info
#         LensPosition = newfilename.find("_")
#         newfilename = newfilename[:LensPosition] + UserName + " " + AuID + " " + trans_date_time + ".t" + newfilename[-2:]
#
#         Job_Not_Available = false
#
#         SQLString = "Update FilesActive set FileStatus = 't', TransNameLast ='" + UserName + "', TransID ='" + AuID + "',  filename = '" + newfilename + "', TimeTranscription = '" + trans_time + "', DateTranscription = '" + trans_date + "'  where JobNumber=" + SJID + " AND FileStatus = '" + FStatus + "'"
#         if FStatus == "c": SQLString = "Update FilesActive set FileStatus = 't', filename = '" + newfilename + "'  where JobNumber=" + SJID + " AND FileStatus = '" + FStatus + "'"
#
#         str_execution = SQLString
#         #str_execution with filename not yet implemented --for testing--but I didn't test it
#         #str_execution = "Update FilesActive set FileStatus = 't', TransNameLast ='" + UserName + "', TransID ='" + AuID + "', TimeTranscription = '" + trans_time + "', DateTranscription = '" + trans_date + "'  where JobNumber=" + SJID + " AND FileStatus = '" + FStatus + "'"
#         with connections['VS_FileMgmt'].cursor() as cursor:
#             cursor.execute(str_execution)
#             # return HttpResponse('')
#             columns = [col[0] for col in cursor.description]
#             results = [
#                 dict(zip(columns, row))
#                 for row in cursor.fetchall()
#             ]
#
#             if ZERO rows: #Not your job--cause it's gone
#                 Job_Not_Available = true
#             else:
#                 #we have this job
#                 #it's yours but... is the filename correct?
#
#                 # check if job REALLY exists():
#                 jobPresent = true
#                 try:
#                     fso = open(ServerRootPath + "//Files//" + FileNameOnlySignedOut)
#                     # Do something with the file
#                     fso.close()
#                     #import os
#                     os.rename(ServerRootPath + "//Files//" + FileNameOnlySignedOut, ServerRootPath + "//Files//" + newfilename)
#                 except IOError:
#                     print("File not accessible")
#                     jobPresent = false
#                     if rows:
#                         # now get the filename
#                         # substr(FileName,25) as subFname
#                         cursor.execute(str_execution)
#                         cursor.execute(
#                             "Select FileName from FilesActive WHERE  where JobNumber=" + SJID)
#                         columns = [col[0] for col in cursor.description]
#                         results = [
#                             # there will only be one
#                             dict(zip(columns, row))
#                             for row in cursor.fetchone()
#                         ]
#                         x = json.dumps(results)
#                         ReturnableFilenameOnly == x --not sure how this works
#                         return ReturnableFilenameOnly
#
#                     if FilenameOnly_SignedOut == ReturnableFilenameOnly:
#                         jobPresent = false
#                     else:
#                         try:
#                             fso = open(ServerRootPath + "//Files//" + ReturnableFilenameOnly)
#                             jobPresent = true
#                             fso.close()
#                             os.rename(ServerRootPath + "//Files//" + ReturnableFilenameOnly,ServerRootPath + "//Files//" + newfilename)
#                         except IOError:
#                             print("File not accessible")
#                             jobPresent = false
#
#                 finally:
#
#
#                 if jobPresent == false:
#                     ReturnableFilenameOnly = DatabaseJobNumberFilenameResolutionCheck(JobNumber, ReturnableFilenameOnly,
#                                                                                       "Status")
#                     if ReturnableFilenameOnly != "none":
#                         os.rename(ServerRootPath + "//Files//" + FileNameOnlySignedOut,
#                                   ServerRootPath + "//Files//" + newfilename)
#                         jobPresent = true
#
#
#                 if jobPresent:
#                     # trans_date = now.strftime("%m/%d/%Y")
#                     # trans_time = now.strftime("%H:%M:%S")
#                     # trans_date_time = now.strftime("%m %d %Y %H %M %S")
#                     SJID = request.POST['SJID']
#                     AuID = request.POST['AuID']
#
#                     ReturnableFilenameOnly = request.POST['FileSignedOut']
#                     FilenameOnly_SignedOut = request.POST['FileSignedOut']
#                     UserName = request.POST['UserName']
#                     FStatus = request.POST['FStatus']
#
#                     THERE IS A JOB, CAN WE SEND THIS BACK TO THE USER BEFORE WE UPDATE THE DBS TO MAKE IT FASTER?
#
#                     #RETURN ReturnableFilenameOnly to the audio player and open it up.                                                                         ''
#
#                     #def LogJobSignedOutToDbs(JobNumber,newfilename,TransId,TransName,tStatus,PMCorrectedTransTime,TransDate,TransDateTimeString,FileInReviewModeFlag):
#                     LogJobSignedOutToDbs(False,JobNumber, newfilename,AuID,UserName,FStatus,trans_time,trans_date,"20200425-NotSureYet-Check-SQL", "false")
#
#                 else:
#                     LogJobSignedOutToDbs(true, JobNumber, newfilename, AuID, UserName, FStatus, trans_time, trans_date,
#                                          "20200425-NotSureYet-Check-SQL", "false")
#
#                     CallAuxiliaryJob()
#
#                     return Alert "Sorry, your job has been signed out by another user"
#
#
#                 #substr(FileName,25) as subFname
#                 #return HttpResponse(refreshTable(str_execution, fileSignedOut,Jnom,FStatus, )
#     return render(request, "HomePage.html",
#                   {
#                       "fileSignedOut": ServerFileSharingURL + "//" + newfilename,
#                       "Jnom": Jnom,
#                       "FStatus": FStatus,
#
#                   })