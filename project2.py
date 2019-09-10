"""
Created by Christian Montero
September 5, 2019

This file uses python3.6 to parse GEDCOME files and determine the va;idity of each line with 
respect to the accepted tokens laid out within the ProjectDescription.

"""

file_name = input("Enter the test file path... ")
print(file_name)
try:
    data = open(file_name, 'r')
except:
    print('The file does not exist')
    exit()


# Contains Valid Tag and Level Tokens
valid = {
    0: ["INDI", "FAM", "HEAD", "TRLR", "NOTE"],
    1: ["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "MARR", "HUSB", "WIFE", "CHIL", "DIV"],
    2: "DATE"
}

# Parses GEDCOM file to determine valid and invalid lines based on tokens
for line in data:
    print("--> " + line.strip())
    tokens = line.split()
    level = int(tokens[0])

    # Check Validity
    levCheck = level in valid
    if levCheck is False:
        tagCheck = False
    else:
        tagCheck = tokens[1] in valid[level]

    
    if (levCheck and tagCheck):
        if (tokens[1] == "INDI" or tokens[1] == "FAM"):
            # IGNORE LINE
            print("<-- " + str(level) + "|" + tokens[1] + "|N|" + " ".join(tokens[2:]))
        else:
            print("<-- " + str(level) + "|" + tokens[1] + "|Y|" + " ".join(tokens[2:]))

    elif (levCheck == False or tagCheck ==  False):
        if (len(tokens) >= 3):
            if (tokens[2] == "INDI") or (tokens[2] == "FAM"):
                print("<-- " + str(level) + "|" + tokens[1] + "|Y|" + " ".join(tokens[2:]))
            else: 
                # IGNORE LINE
                print("<-- " + str(level) + "|" + tokens[1] + "|N|" + " ".join(tokens[2:]))
                
        else:
            # IGNORE LINE
            print("<-- " + str(level) + "|" + tokens[1] + "|N|" + " ".join(tokens[2:]))
