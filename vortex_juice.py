from urllib import urlopen
from re import match, search, findall, finditer
from random import sample
from xml.dom.minidom import parseString, parse


class SubjectIndex:
    def __init__( self, url = "http://www.uio.no/studier/emner/" ):
        self.url = url
        self.page = urlopen( self.url ).read()
        self.excluded = set( ["alfabetisk", "alphabetical", "nedlagt"] )
        
    def get_faculty_links( self ):
        pattern = "emner/\w+"
        relatives = findall( pattern, self.page )
        absolutes = set( 
            [ ( self.url.replace( "emner/", "" ) + e ) for e in relatives ] 
        )
        
        # here
        
        return absolutes
        
        

class FacultyData:
    def __init__( self, url ):
        self.data = urlopen( location + "/" + suffix ).read()


    def get_subject_descriptions( self ):
        model = parseString(self.data)

        clean = model.getElementsByTagName( "ul" )
        clean = [e for e in clean if e.getAttribute("class") == "main"]
        clean = [e.childNodes for e in clean]
        clean = clean[0]
        
        subjects = [e.firstChild for e in clean]
        subjects = [e.firstChild.toxml() for e in subjects]
            
        return subjects
    
    def get_precise_subject_quantity( self ):
        model = parseString( self.data )
        clean = model.getElementsByTagName( "h2" )
        clean = clean.item(0).firstChild.nodeValue
        
        number = findall( "\d+", clean )

        return number
    
    def verify_number_of_subjects( self ):

        number = self.get_subject_quantity( self.data )
        
        return( 
            int(number[0]) == len( self.get_subject_descriptions() ) 
        )
    
    def get_subject_codes( self ):
        complex_subject = "(\w{1,4}-\w{1,4}\d{1,4})+"
        regular_subject = "(\w{1,4}\d{1,4})+"
        pattern = "(" + complex_subject + "|" + regular_subject + ")+"
        result = [ findall(pattern, d) 
            for d in self.get_subject_descriptions() ]
        result = [c[0][0] for c in result if c[0][0] != ""]
        
        return result
        
    def save( self, name ):
        text = "\n".join( self.get_subject_codes() )
        with open( "matnat.dat", "w" ) as output:
            output.write(text)



if __name__ == "__main__":
    location = "http://www.uio.no/studier/emner/"
    suffix = "matnat"
    
    si = SubjectIndex()
    
    for s in si.get_faculty_links():
        print s
    
    v = FacultyData( location + "/" + suffix )
    v.save( "matnat.dat" )


