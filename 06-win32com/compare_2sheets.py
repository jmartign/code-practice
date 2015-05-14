#compare content in 2 excel sheets
import os
import win32com.client
#import re

EXCEL_FILE = r'test.xlsx'
SHEET_NAME1 = 'old'
SHEET_NAME2 = 'new'
#SHEET_RESULT = 'result'

columnHeaders = []
skipColumns = []

app = win32com.client.Dispatch('Excel.Application')
workbook = app.Workbooks.Open(EXCEL_FILE)
sheet1 = workbook.Sheets(SHEET_NAME1)
sheet2 = workbook.Sheets(SHEET_NAME2)
#sheet3 = workbook.Sheets(SHEET_RESULT)

#get row count and column count
rowCount = sheet1.UsedRange.Rows.Count
columnCount = sheet1.UsedRange.Columns.Count
#print rowCount, columnCount

columnTitles = []
titleColumnMap = {}
#sheet2.Cells(1, 1).Value = 'did'
#cell index begin from 1

#copy title row to result sheet
#for c in range(1, columnCount+1):
#    sheet3.Cells(1, c).Value = sheet1.Cells(1, c).Value
    
#print "%x"%(sheet3.Cells(1,1).Interior.Color,)
    #sheet3.Cells(4,1).Interior.Color = 0xFFFF
    #sheet3.Rows(1).Interior.Color = 0xFFFF
def getColumnTitles(sheet):
    global columnTitles, titleColumnMap
    
    for i in range(1, columnCount+1):
        title = sheet.Cells(1, i).Value
        columnTitles.append(title)
        titleColumnMap[title] = i
        
def putResultInSheet(sheet, row, col, value):
    sheet.Cells(row, col).Value = value
    sheet.Cells(row, col).Interior.Color = 0xFFFF
    sheet.Cells(row, 1).Interior.Color = 0xFF

def indicateInSheet(sheet, row, col):
    sheet.Cells(row, col).Interior.Color = 0xFFFF
    sheet.Cells(row, 1).Interior.Color = 0xFF

#getColumnTitles(sheet1)

try:
    for i in range(2, rowCount+1):
        for j in range(1, columnCount+1):
            #if j in skipColumns:
            #    continue
            v1 = sheet1.Cells(i, j).Value
            v2 = sheet2.Cells(i, j).Value
            #print i,j
            if v1 != v2:
                #putResultInSheet(sheet3, i, j, v1 + "<>" + v2)
                indicateInSheet(sheet2, i, j)

    workbook.Save()
    print 'done'
except Exception as e:
    print e
finally:
    pass
    #workbook.Close()

#if app.Workbooks.Count == 0:
#    app.Quit()




