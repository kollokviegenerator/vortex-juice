from urllib import urlopen
from re import match, search, findall, finditer
from random import sample
from xml.dom.minidom import parseString, parse


class FacultyIndex:
    def __init__( self, url="http://www.uio.no/studier/emner/" ):
        self.url = url
        self.page = urlopen( self.url ).read()
        self.excluded = set( ["alfabetisk", "alphabetical", "nedlagt" ] ) #"index", "v12", "v13", "h12"] )
        self.prefix = "emner/"
        
    def get_faculties( self ):
        pattern = self.prefix + "\w+"
        relatives = findall( pattern, self.page )
        # remove prefix
        relatives = [l.replace( self.prefix, "" ) for l in relatives ]
        # gather unique
        relatives = set(relatives)
        # remove excluded
        relatives = relatives.difference( self.excluded )

        return relatives

class InstituteIndex:
    def __init__( self, faculties, url="http://www.uio.no/studier/emner/" ):
        self.url = url
        self.page = urlopen( self.url ).read()
        self.faculties = faculties
        self.prefix = "studier/emner/"

    def get_all_institutes( self ):

        institutes = []

        for f in self.faculties:
            pattern = "%s%s/%s" % (self.prefix, f, "\w+/")
            relatives = findall( pattern, self.page )
            relatives = [l.replace( self.prefix + f, "" ) for l in relatives ]
            institutes += relatives

        return set(institutes)

    def get_institutes_of_faculty( self, faculty ):
        pattern = "%s%s/%s" % (self.prefix, faculty, "\w+/")
        relatives = findall( pattern, self.page )
        relatives = [l.replace( self.prefix + faculty, "" ) for l in relatives ]

        return set(relatives)




class FacultyData:
    def __init__( self, url="http://www.uio.no/studier/emner/" ):
        self.data = urlopen( url ).read()


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
        #exceptions = "([AZ]){1,10}"
        pattern = "(" + complex_subject + "|" + regular_subject + ")+"
        result = [ match(pattern, d)
            for d in self.get_subject_descriptions() ]



        result = [m.group(1) for m in result if m != None]

        return result
        
    def save( self, name ):
        text = "\n".join( self.get_subject_codes() )
        with open( "data/%s.dat" % name, "w" ) as output:
            output.write(text)



if __name__ == "__main__":
    faculties = ( FacultyIndex() ).get_faculties()
    institutes = InstituteIndex( faculties )

    structure = {}
    for f in faculties:
        members = institutes.get_institutes_of_faculty( f )
        if len(members) > 0:
            structure[f] = members

    #structure["annet"].add( "/teologi/" )
    print structure

    for (faculty, institutes) in structure.iteritems():
        for i in institutes:
            url = "http://www.uio.no/studier/emner/%s/%s" % (faculty, i)
            data = FacultyData( url=url )

            filename = "%s" % (faculty)
            if i != "":
                filename = "%s-%s" % (faculty, i.replace("/", "") )

            data.save( filename )



