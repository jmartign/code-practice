#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import os
import os.path
import zipfile
import tempfile
import win32com.client

DEST_DIR = r'./'
SUBJECT_RESTRICT = '[Subject] = "test"'

def openOutlookFolder(mailHandler):
    outlookApp = win32com.client.gencache.EnsureDispatch('Outlook.Application')
    nsMAPI = outlookApp.GetNamespace('MAPI')
    f = nsMAPI.Folders.Item('Archive Folders')
    # print f.FullFolderPath
    emailList = f.Folders.Item('in').Items.Restrict(SUBJECT_RESTRICT)
    for msg in emailList:
        mailHandler(msg)

def saveMailAttachment(mailItem):
    print '{0} - {1}'.format(mailItem.ReceivedTime, mailItem.Subject)
    if mailItem.Attachments.Count > 0:
        newName = mailItem.ReceivedTime.Format('%Y%m%d%H%M')
        attachment = mailItem.Attachments.Item(1)
        ext = os.path.splitext(attachment.FileName)[1]
        if ext.lower() == '.zip':
            #tp = attachment.GetTemporaryFilePath()
            # tp = tempfile.mkstemp()
            tp = os.path.join(DEST_DIR, newName + attachment.FileName)
            attachment.SaveAsFile(tp)
            #print 'GetTemporaryFilePath()', tp
            with zipfile.ZipFile(tp, 'r') as zf:
                name = zf.namelist()[0]
                #zf.extract(name, folder)
                f = open(os.path.join(DEST_DIR, newName + os.path.splitext(name)[1]), 'wb')
                f.write(zf.read(name))
                f.close()
            os.remove(tp)
        elif ext.lower() in ('.xls', '.xlsx'):
            attachment.SaveAsFile(os.path.join(DEST_DIR, newName + ext))

openOutlookFolder(saveMailAttachment)