MATCH VOTERS to OHIO Voter files
Craig Wilding 1/30/23

MATCHING PROCESS USED:
1) Check Birth Year + Zip + Last Name
2) Check Birth Year + Last Name
	Addresses may change so this is a secondary match that ignores the address and zip
	
Birth year 
	Date of Birth filters the possibile matches down the most.  SOE offices use this first, then the name to find someone quickly
	The birth year appears to be entered in each of the voter files, though 1901-01-01 may be an invalid date.

Zip Code
	Zip Code also helps filters the possibile matches down.  This narrows it to the correct county.
	Zip 5 also appears to be entered for all voters.
	Zip is used over city so I don't have to address mispelling of city names.
	addresses are the hardest to parse for comparison and will not be used.
	
Last Name
	Last Names are the next field to compare given a DOB and/or zip
	Surnames
		The surnames JR. and SR. are removed from the matching names.  
		A more thorough list of surnames should be checked.
		
	TODO: Middle Names
		Middle names and last names havedifferences in how they are used in different cultures.  
		Reviewing the middle names in the voter file, I could see that Hispanic, French, Arabic and Vietnamese names often include 
		multiple names as part of either their middle or last name.  It can be unclear to the voter and/or the election administrator 
		which parts of the name to include as the last name and which to include as a first or middle name.  
		Women also have a cultural trend of appending a married name onto their maiden name.  Again, this can result in the same 
		problems of where the split name shows up in the voter data file.  
		
		With more time, a check of middle names and middle + last name combinations should be used if a last name match is not found

First Name
	First Name is the least reliable because of nick-names, aliases, or shortened names being used.
	I am not using it to certify a match because of this unreliability.
	TODO: If there are multiple matches on the DOB + Last Name, then it could do a check of first names to compare.
	
I will only find a match if the birth year and/or zip are included.
There are multiple entries in the match file that only have the name.  Without the birth year or zip code, name matching
produces too many duplicates to confirm the correct person.  Especially for Hispanic names.


	
DATA LOADING PROCESS 

Step 1) Process the voter files
From the voter files, I need the birth year, zip code, last name and first name, and voter ID.
The voter file is a comma delimited file, but is labeled with a .txt extension.  

Step 2) Data-Dictionary lookup
The python script uses a data dictionary to store voter info from the voter file.
It uses the birth-year + zip5 as the lookup key.  Each key holds a list of matching voters by the birth+zip key.
I used a class object to store the voter's last and first name.  
As the script reads through the match file, it will use the dictionary to get all matches with the birth+zip key and check the
last and first name for matches.  

I added a second data dictionary for lookup by just the birth year.  If a match is not found on the first pass by year+zip+last name,
then it will lookup matches by just birth year and check for matching last names.

Any entry without a birth date and/or zip will be skipped.

Step 3) READ MATCH FILE
Read through the eng-matching-input-v3.csv file and save the values for output.

parseLastName 
	This method parses the last name from the name field in the match file since the first and last name are combined.
	This way any changes to how the name is parsed can be changed here.
	
matchLastName
	This method compares the last name in the voter file to the last name from the match file
	It is used to put any comparison requirements in one place.
	It currently accounts for:
		case - by using lower()
		surnames - by removing JR. or SR.
		
Step 4 ) Write Results
Write results to TMC_Q4_Results.csv
Append matched_voterid column to original column format
