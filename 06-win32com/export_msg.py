#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import win32com.client

def saveMailAsFile(mailItem):
    root_dir = r'D:\msgStore2'
    try:
        dest_dir = os.path.join(root_dir, mailItem.ReceivedTime.Format('%Y/%m/%d'))
    except:
        return
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    mailItem.SaveAs(os.path.join(dest_dir, str(mailItem.EntryID) + '.msg'))


def deleteMail(mailItem):
    try:
        mailItem.Delete()
    except Exception, e:
        print 'Exception when delete', mailItem.Subject
        print e


def saveMailAndDelete(mailItem):
    saveMailAsFile(mailItem)
    deleteMail(mailItem)

def openOutlookFolderWithConfig(config, mailHandler):
    outlookApp = win32com.client.gencache.EnsureDispatch('Outlook.Application')
    nsMAPI = outlookApp.GetNamespace('MAPI')
    folder = nsMAPI

    fPaths = config['folder'].strip('/').split('/')
    for p in fPaths:
        folder = folder.Folders.Item(p)
    print 'Location:', folder.FullFolderPath
    
    while True:
        emailList = folder.Items
        print len(emailList)
        if len(emailList) == 0:
            break
        for msg in emailList:
            mailHandler(msg)
            
def exportMSG():
    config = {
        'folder': 'Archive Folders/Inbox',
    }
    openOutlookFolderWithConfig(config, saveMailAndDelete)

if __name__ == '__main__':
    exportMSG()
    
