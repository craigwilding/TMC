import os
import shutil
from datetime import datetime
import csv
from csv import DictReader
from csv import DictWriter
##################################################
# TMC Q4:
# Match list of names, birth year, and address to Ohio Voter files
# Steps:
# Read voter info from voter files
# Build a data dictionary lookup based on birtyYear+zip5 as the key
# Read match file info
# lookup maches based on birtyYear+zip5 key
##################################################


dirTMC = r"G:\Safe Documents\Resume\PoliticJobs\DataEngineer\Tests\TMC"
dirVoterFiles = os.path.join(dirTMC, "Ohio_VoterFiles")
fileNameIn = os.path.join(dirTMC, "eng-matching-input-v3.csv")
fileNameOut = os.path.join(dirTMC, "TMC_Q4_Results.csv")
dirOut = dirTMC

wrksp = dirTMC
os.chdir(wrksp)
print(os.getcwd())

if not os.path.exists(dirOut):
    os.makedirs(dirOut)
    
TAB = "\t"
DLM = "|"
EOL = '\n'
SPACE = ' '

##################################################
# Voter info
# This class holds the voter's info from the voter file
##################################################
class VoterInfoClass:

    def __init__(self) :
        self.voterID = ""
        self.countyID = ""
        self.lastName = ""
        self.firstName = ""
        self.dateOfBirth = ""
        self.birthYear = ""
        self.zip5 = ""
        self.key = ""
    # end init
    
    def GetData(self, rowOut):
        contacts = self.contactCount()
        rowOut['contactCount'] = contacts
        rowOut['phone'] = self.phone
        rowOut['email'] = self.email
        return rowOut
    # end GetData()

    def GetHeader(self):
        header = ['contactCount', 'phone', 'email']
        return header
    # end GetHeader()

#end VoterInfoClass  

##################################################
# parseLastName
# Parse the last name from the input file which has it as one value
# Examples:
# Jeremy T Patterson -> Patterson
# Juanita J Dettwiller -> Dettwiller
##################################################
def parseLastName(name) :
    # Assumes last name is separated by a blank space from the rest of the name
    lastName = ""
    ixSpace = name.rfind(SPACE) # finds last instance of SPACE
    if (ixSpace > -1) :
        lastName = name[ixSpace+1:]
    #endif
    return lastName
# end parseLastName

##################################################
# matchLastName
# Check if the last names match
# Do any cleaning on the names here to help ensure they match
# Examples:
# user lower to prevent case mismatch
# Remove any suffix such as JR. SR.
##################################################
def matchLastName(matchLastNameIn, VoterLastNameIn) :
    # 
    match = False
    matchLastName = matchLastNameIn.lower().replace('.',"").replace("jr","").replace("sr","")
    VoterLastName = VoterLastNameIn.lower().replace('.',"").replace("jr","").replace("sr","")
    if (VoterLastName == matchLastName) :
        match = True
    #endif
    return match
# end parseLastName


##################################################
# data Dictionary
# This is a key-value dictionary
# key = birthYear + zip5
# returns List of VoterInfoClass objects with that key
# Example:
# key[1994+33344] = [Voter1, Voter2, Voter3]
# Voter# = an instance of VoterInfoClass
#
# dictVotersByBirth
# same as above, but the key is just the birth year.
##################################################
dictVotersByBirthZip = {}
dictVotersByBirth = {}

##################################################
# Get Voter info
# Recurse through voter files.
# This builds the data dictionary used for lookup
##################################################
for countyFile in os.listdir(dirVoterFiles) :
    fnameCounty = os.path.join(dirVoterFiles, countyFile)

    with open(fnameCounty, 'r') as read_obj:
        csv_dict_reader = DictReader(read_obj)

        for row in csv_dict_reader:
            Voter = VoterInfoClass()
            Voter.voterID = row["SOS_VOTERID"]
            Voter.countyID = row["COUNTY_ID"]
            Voter.lastName = row["LAST_NAME"]
            Voter.firstName = row["FIRST_NAME"]
            Voter.dateOfBirth = row["DATE_OF_BIRTH"]
            # Date Format: "1993-06-02"
            Voter.birthYear = Voter.dateOfBirth[:4]
            Voter.zip5 = row["RESIDENTIAL_ZIP"]
            Voter.key = Voter.birthYear + "+" + Voter.zip5

            if (Voter.key not in dictVotersByBirthZip) :
                # new key
                voterList = []
                voterList.append(Voter)
                dictVotersByBirthZip[Voter.key] = voterList
                
            else :
                # add Voter to list of matches
                voterList = dictVotersByBirthZip[Voter.key]
                voterList.append(Voter)
                dictVotersByBirthZip[Voter.key] = voterList
            # end if

            if (Voter.birthYear not in dictVotersByBirth) :
                # new key
                voterList = []
                voterList.append(Voter)
                dictVotersByBirth[Voter.birthYear] = voterList
                
            else :
                # add Voter to list of matches
                voterList = dictVotersByBirth[Voter.birthYear]
                voterList.append(Voter)
                dictVotersByBirth[Voter.birthYear] = voterList
            # end if
        # end for each row
    # end read csv
# end county voter files in dir
    

##################################################
# Read input file
# Lookup BirthYear+zip5 for possible matches
# Check last name for matches
# Write matches to output file
##################################################

with open(fileNameOut, 'w', newline='') as write_csv:
    # field names 
    fields = ['row', 'name', 'birth_year']
    fields += ['address', 'city', 'state', 'zip']
    fields += ['matched_voterid']
    # write column headers 
    csvwriter = csv.DictWriter(write_csv, fieldnames = fields)
    csvwriter.writeheader()
    rowsOut = []

    with open(fileNameIn, 'r') as read_obj:
        csv_dict_reader = DictReader(read_obj)

        for row in csv_dict_reader:
            # read the line in, save the values for output.
            rowID = row["row"]
            name = row["name"]
            birth_year = row["birth_year"]
            address = row["address"]
            city = row["city"]
            state = row["state"]
            zip5 = row["zip"]
            matched_voterid = ""
            
            key = birth_year + "+" + zip5    
            lastName = parseLastName(name)
            
            if (key in dictVotersByBirthZip) :
                # MATCH 1: Birth Year + Zip5 + Last Name
                voterList = dictVotersByBirthZip[key]
                matchCount = 0
                for Voter in voterList :
                    # compare name to voter file
                    if matchLastName(lastName, Voter.lastName) :
                        matchCount += 1
                        matched_voterid = Voter.voterID
                        if (matchCount > 1) :
                            # multiple match on last name found
                            # TODO: do 2nd level matching here
                            # reset matched voter id
                            matched_voterid = ""
                        # end matchCount
                    # end matchLastName
                # end for voterList
            elif (birth_year in dictVotersByBirth) :
                # Match 2: Birth Year + Last Name
                voterList = dictVotersByBirth[birth_year]
                matchCount = 0
                for Voter in voterList :
                    # compare name to voter file
                    if matchLastName(lastName, Voter.lastName) :
                        matchCount += 1
                        matched_voterid = Voter.voterID
                        if (matchCount > 1) :
                            # multiple match on last name found
                            # TODO: do 2nd level matching here
                            # reset matched voter id
                            matched_voterid = ""
                        # end matchCount
                    # end matchLastName
                # end for voterList
            # end if key found
                        
            rowOut = {}
            rowOut["row"] = rowID
            rowOut["name"] = name
            rowOut["birth_year"] = birth_year
            rowOut["address"] = address
            rowOut["city"] = city
            rowOut["zip"] = zip5
            rowOut["matched_voterid"] = matched_voterid
            rowsOut.append(rowOut)
    
        # end for match file

    #Write as CSV file
    csvwriter.writerows(rowsOut)
    print("WRITE file: " + fileNameOut)
# end with write csv
del write_csv
del rowsOut


    
print("********************************")
print("********************************")
print("********************************")
print("********************************")
print("Finished")

##############################################
# END - Cleanup
#################################################
del dictVotersByBirthZip
del dictVotersByBirth




    


