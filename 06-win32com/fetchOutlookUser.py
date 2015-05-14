#!/usr/bin/env python
# -*- coding: utf8 -*-

from collections import namedtuple
import win32com.client

# http://stackoverflow.com/questions/27177435/getting-contact-information-from-the-outlook-gal-using-python-and-win32com
# MSDN http://msdn.microsoft.com/en-us/library/microsoft.office.interop.outlook.exchangeuser_members(v=office.15).aspx
# OutlookSpy http://www.dimastr.com/outspy/home.htm

ContactUser = namedtuple('ContactUser', ['Name', 'Alias', 'OfficeLocation', 'PrimarySmtpAddress'])

def fetchUserByList(name_list):
	outlookApp = win32com.client.gencache.EnsureDispatch('Outlook.Application')
	nsMAPI = outlookApp.GetNamespace('MAPI')
	addrList = nsMAPI.AddressLists.Item("Global Address List").AddressEntries
	
	userMap = {}
	for name in name_list:
		addr = addrList.Item(name)
		if addr:
			u = addr.GetExchangeUser()
			userMap[name] = ContactUser(u.Name, u.Alias, u.OfficeLocation, u.PrimarySmtpAddress)
	return userMap

#um = fetchUserByList(['Vika zhou'])
#print um['Vika zhou']

def cutName(name):
	return name.split('(')[0].strip()

if __name__ == '__main__':
	infile = open('ulist2.txt', 'r')
	nameList = [cutName(n) for n in infile if n]
	userMap = fetchUserByList(nameList)
	
	outfile = open('contacts2.txt', 'w')
	for name in nameList:
		u = userMap[name]
		if u:
			outfile.write(name + '|' + '|'.join(u) + '\n')
	#officeMap = {}
	#for val in userMap.itervalues():
	#	l = officeMap.get(val.OfficeLocation, [])
	#	l.append('\'' + val.Alias + '\'')
	#	officeMap[val.OfficeLocation] = l
	#for k, v in officeMap.iteritems():
	#	outfile.write(','.join(v) + '|' + k + '\n')
	outfile.close()
