import os
import shutil
import csv
import re # regex
from csv import DictReader
from csv import DictWriter

wrksp = r"G:\Safe Documents\Resume\PoliticJobs\DataEngineer\Tests\TMC"
sampleFileIn = os.path.join(wrksp, "TMC_Q2_sample.csv")
sampleFileOut = os.path.join(wrksp, "TMC_Q2_results.csv")

TAB = "\t"
DLM = "|"
EOL = '\n'
NULL = "NULL"
UP_O = 'O'
Lower_O = 'o'
ZERO = '0'

LOCAL_AREA_CODE = '888'
FORMAT_DASH = 1
FORMAT_AREA = 2


def normalizePhone(phoneIn) :
    phoneOut = ""
    try:      
        # parse for digits only
        for char in phoneIn :
            if (char.isdigit()) :
                phoneOut += char
            elif (UP_O == char) or (Lower_O == char) :
                # convert letter O to zero
                phoneOut += ZERO
            # end if
        # end for each char

        # 7-digits assumes the area code was left off and will use a default local area code
        if (len(phoneOut) == 7):
            phoneOut = LOCAL_AREA_CODE + phoneOut
        # truncate to 10 digits
        # assumes international numbers have leading digits to truncate.
        # so it will truncate from the left, pulling the right-most 10 digits
        elif (len(phoneOut) > 10) :
            phoneOut = phoneOut[-10:]
        # check for min and max digits
        # this will blank out the phone number as invalid
        # over 16 assumes an invalid entry as international numbers are less than this.
        elif (len(phoneOut) < 10) or (len(phoneOut) >= 16) :
            phoneOut = ""
        # end if
            
    except:
        print("ERROR converting phone value: " + phoneIn)
        phoneOut = ""
    # end try

    return phoneOut

# end normalizePhone

def formatPhone(phone, formatCode) :
    # for user convenience, this will assume the phone needs to be normalized first
    # this way, it ensures the phone numbers are valid before formatting
    
    phoneNorm = normalizePhone(phone)
    phoneOut = phoneNorm
    if (len(phoneOut) == 10) : # valid phone has 10 digits
        
        if (FORMAT_AREA == formatCode) :    
            phoneOut = "(" + phoneNorm[:3] + ") " + phoneNorm[3:6] + "-" + phoneNorm[6:]
        # end if        
        else : # use FORMAT_DASH     
            phoneOut = phoneNorm[:3] + "-" + phoneNorm[3:6] + "-" + phoneNorm[6:]
        # end if
    # end if valid phone
    return phoneOut
# end formatPhone



#########################################
# read each sample phone number and format it.
#########################################
with open(sampleFileOut, 'w', newline='') as write_csv:
    # field names 
    fields = ['name', 'raw', 'normalized', 'dash-foramt', 'area-foramt']
    # write column headers 
    csvwriter = csv.DictWriter(write_csv, fieldnames = fields)
    csvwriter.writeheader()
    rowsOut = []

    with open(sampleFileIn, 'r') as read_obj:
        csv_dict_reader = DictReader(read_obj)
        for row in csv_dict_reader:
            
            name = row["name"]
            phoneRaw = row["phone"]
            # normalize phone number
            phoneOut = normalizePhone(phoneRaw)
            
            testOut = "Test: " + name + TAB+ "Raw[" + phoneRaw + "]" + TAB + "Norm[" + phoneOut + "]"
            testOut += TAB + "Dash[" + formatPhone(phoneRaw, FORMAT_DASH) + "]"
            testOut += TAB + "Area[" + formatPhone(phoneRaw, FORMAT_AREA) + "]"
            print(testOut)

            # Write results to csv
            rowOut = {}
            rowOut["name"] = name
            rowOut["raw"] = phoneRaw
            rowOut["normalized"] = phoneOut
            rowOut["dash-foramt"] = formatPhone(phoneRaw, FORMAT_DASH)
            rowOut["area-foramt"] = formatPhone(phoneRaw, FORMAT_AREA)
            rowsOut.append(rowOut)
        # end for each row
    # end with csv read
    
    #Write as CSV file
    csvwriter.writerows(rowsOut)
    print("WRITE file: " + sampleFileOut)
# end with write csv
del write_csv
del rowsOut
