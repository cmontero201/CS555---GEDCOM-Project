# Main Function lets user open proj02test.ged file
# and prints valid and invalid tags based on https://sit.instructure.com/courses/34746/files/5021872/download documentation
# the code was tested with proj02test.ged

import re
import collections

def printyes(line, match):
    print(line.rstrip())
    print(match.group("lvl").strip(),match.group("tag").strip(),"Y",match.group("arg1").strip(),match.group("arg2").strip(), sep="|")

def printno(line, match):
    print(line.rstrip())
    print(match.group("lvl").strip(),match.group("tag").strip(),"N",match.group("arg1").strip(),match.group("arg2").strip(), sep="|")

def main():
    try:
        filename= input("Please input a .get file?")
        # Used Regex to extract groups in to test pattern is to find all valid and invalid statements in .ged file
        # 1st is lvl= (?P<lvl>^0|[1-9]+[0-9]*) pattern to find any non negative number including zero
        # 2nd tag = (?P<tag>.[_a-zA-Z0-9]+) pattern to find a word character 
        # 3rd arg1 groups= (?P<arg1>[^\n\r]*|) patter to find the string before newline and return
        # 4rd arg2  groups= (?P<arg2>[\r\n]{1,2}) pattern to find newline and return at the end of the line
        test = re.compile('(?P<lvl>^0|[1-9]+[0-9]*)(?P<tag>.[_a-zA-Z0-9]+)(?P<arg1>[^\n\r]*|)(?P<arg2>[\r\n]{1,2})', re.VERBOSE)
        if not filename:
            raise FileNotFoundError
        else:
            with open(filename) as filehandler:
                for line in filehandler:
                    match = test.match(line)
                    if match:
                        line_parts = match.groups()
                        lvl =  match.group("lvl").strip() # level
                        tag = match.group("tag").strip()  # tag 
                        Ind_fam_tag = match.group("arg1").strip() # if the statments is in the exception such INDI or FAM 
                        if lvl == "0": # Checks INDI, FAM, HEAD, TRLR and Note tags
                            if Ind_fam_tag == "INDI" or Ind_fam_tag == "FAM" or tag == "HEAD" or tag == "TRLR" or tag == "NOTE":
                                if Ind_fam_tag == "INDI":
                                    printyes(line, match)
                                elif tag == "NOTE":
                                    printyes(line, match)
                                elif tag == "TRLR":
                                    printyes(line, match)
                                elif tag == "HEAD":
                                    printyes(line, match)
                                elif Ind_fam_tag == "FAM":
                                    printyes(line, match)
                                else:
                                    print(line.rstrip())
                                    print(match.group("lvl").strip(),match.group("tag").strip(),"N",match.group("arg1").strip(),match.group("arg2").strip(), sep="|")
                            else: # Prints the none matching 
                                print(line.rstrip())
                                print(match.group("lvl").strip(),match.group("tag").strip(),"N",match.group("arg1").strip(),match.group("arg2").strip(), sep="|")
                        elif lvl == "1": # Checks NAME, SEX, BIRT, DEAT, FAMC and FAMS tags
                            if tag == "NAME" or tag == "SEX" or tag == "BIRT" or tag == "DEAT" or tag == "FAMC" or tag == "FAMS":
                                printyes(line, match)# Checks MARR, HUSB, WIFE, CHIL and DIV 
                            elif tag == "MARR" or tag == "HUSB" or tag == "WIFE" or tag == "CHIL" or tag == "DIV":
                                printyes(line, match)
                            else: # Prints the none matching 
                                print(line.rstrip())
                                print(match.group("lvl").strip(),match.group("tag").strip(),"N",match.group("arg1").strip(),match.group("arg2").strip(), sep="|")
                        elif lvl == "2": #Checks DATE tag
                            if tag == "DATE":
                                printyes(line, match)
                    else:
                        print(line)
                        print("No Match")
           
    except FileNotFoundError:
        print("You did not enter a filename")
    except Exception as e:
        print(e)
            

if __name__ == "__main__":
    main()
    pass
