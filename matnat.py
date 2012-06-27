from urllib import urlopen
from re import match, search, findall, finditer
from random import sample
from xml.dom.minidom import parseString, parse

location = "http://www.uio.no/studier/emner/"
suffix = "matnat"

data = urlopen( location + "/" + suffix ).read()


class VortexData:
    def __init__( self, url ):
        self.data = urlopen( location + "/" + suffix ).read()


def get_subjects( data ):
    model = parseString(data)

    clean = model.getElementsByTagName( "ul" )
    clean = [e for e in clean if e.getAttribute("class") == "main"]
    clean = [e.childNodes for e in clean]
    clean = clean[0]
    
    subjects = [e.firstChild for e in clean]
    subjects = [e.firstChild.toxml() for e in subjects]
        
    return subjects


def get_precise_number_of_subjects( data ):
    model = parseString(data)
    clean = model.getElementsByTagName( "h2" )
    clean = clean.item(0).firstChild.nodeValue
    
    number = findall( "\d+", clean )

    return number

 
def verify_number_of_subjects( data ):

    number = get_precise_number_of_subjects( data )
    
    return( 
        int(number[0]) == len( get_subjects(data) ) 
    )


if verify_number_of_subjects:
    print "[OK] The number of collected subjects fits the description"

    
#print get_subjects( data )

def get_subject_codes( subject_descriptions ):
    complex_subject = "(\w{1,4}-\w{1,4}\d{1,4})+"
    regular_subject = "(\w{1,4}\d{1,4})+"
    pattern = "(" + complex_subject + "|" + regular_subject + ")+"
    result = [ findall(pattern, d) for d in subject_descriptions ]
    result = [c[0][0] for c in result if c[0][0] != ""]
    
    return result





