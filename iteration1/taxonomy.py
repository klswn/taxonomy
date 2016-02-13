import os
import sys
import pickle

class Taxonomy:

    levelNum = {
        "Order" : 3,
        "Family" : 2,
        "Genus" : 1
    }
    error = ""

    def __init__( self, categoryName, level ):
        self.categoryName = categoryName
        self.level = level

        fileName = categoryName + ".p"

        if ( level == "Order" and os.path.isfile(fileName)): # check if serialized file exists
            order = self.load(fileName)
            self.itemList = order.itemList
        else:
            self.itemList = []

    def addSpecies( self, species ):
        if ( self.level == "Genus" ): # add species to taxonomy and return true
            self.itemList.append(species)
            return True
        else: # set error message and return false
            self.error = "Cannot add species!"
            return False

    def addTaxonomy( self, subTaxonomy):
        if ( self.levelNum[subTaxonomy.level] == self.levelNum[self.level] - 1 ): # add sub-taxonomy to this taxonomy and return true
            self.itemList.append( subTaxonomy )
            return True
        else: # set error and return false
            self.error = "Cannot add sub-taxonomy!"
            return False

    def errorMessage( self ):
        if ( len(self.error) > 0 ):
            return self.error
        else:
            return "Insertion OK"

    def insert( self, path ):
        pathList = path.split('/')

        if ( len(pathList) != self.levelNum[self.level] ): # check path length
            self.error = "Error inserting " + path + " into " + self.categoryName + ": wrong length"
            return False
        else:
            if ( self.levelNum[self.level] != 1 ): # if order or family, deal with sub taxonomies
                categoryName = pathList.pop(0)
                newPath = "/".join(pathList)

                if ( self.exists(categoryName) ): # check for existing taxonomy
                    existingTaxonomy = next(tax for tax in self.itemList if tax.categoryName == categoryName)
                    return existingTaxonomy.insert(newPath)
                else: # family doesn't exist, create a new one
                    subLevel = "Family" if self.levelNum[self.level] == 3 else "Genus"
                    subTaxonomy = Taxonomy(categoryName, subLevel)
                    self.addTaxonomy(subTaxonomy)
                    return subTaxonomy.insert(newPath)
            elif ( self.level == "Genus" ): # add species to genus
                species = pathList.pop(0)
                if ( species in self.itemList ):
                    return True
                else:
                    self.addSpecies( species )
                    return True
            else:
                self.error = "Some unknown error"
                return False

    def list( self ):
        # return a string representing the contents of this taxonomy and its sub taxonomies
        if ( self.level == "Genus" ):
            return self.categoryName + " (" + ", ".join(self.itemList) + ")"
        else:
            str = self.categoryName + " ("
            for i,tax in enumerate(self.itemList):
                if i+1 == len(self.itemList):
                    str += tax.list()
                else:
                    str += tax.list() + ", "
            str += ")"
            return str

    def serialize( self ): # save contents of this object using pickle
        fileName = self.categoryName + ".p"
        os.system("touch " + fileName)
        f = open(fileName, "wb")
        pickle.dump(self, f)
        f.close()
        return True

    def load( self, fileName ): # load serialized file and return object
        f = open(fileName, "rb")
        obj = pickle.load(f)
        f.close()
        return obj

    def exists( self, categoryName ): # check if taxonomy exists in current itemList
        return any(taxonomy.categoryName == categoryName for taxonomy in self.itemList)
