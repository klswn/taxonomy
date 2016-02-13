#
# Test code for the Taxonomy class, which maintains a
# tree of Linnean category and species names
#
import unittest
import taxonomy

class TestTaxonomy(unittest.TestCase):

    def test_addSpecies(self):
        '''Test adding a species to a genus with no errors'''
        genus1 = taxonomy.Taxonomy('Lepus','Genus')
        genus1.addSpecies('townsendi (White-tailed Jackrabbit')
        self.assertEqual(genus1.categoryName,'Lepus')
        self.assertEqual(len(genus1.itemList),1)
        self.assertEqual(genus1.itemList[0],'townsendi (White-tailed Jackrabbit')

    def test_addGenus(self):
        '''Test adding a genus to a family with no errors'''
        family= taxonomy.Taxonomy('Soricidae', 'Family')
        genus= taxonomy.Taxonomy('Sorex','Genus')
        family.addTaxonomy(genus)
        self.assertEqual(family.categoryName,'Soricidae') 
        self.assertEqual(len(family.itemList),1)
        self.assertEqual(len(genus.itemList),0)
 
    def test_insert1(self):
        '''Test inserting a single species to an empty taxomony'''
        order = taxonomy.Taxonomy('Lepidoptera','Order')
        result = order.insert('Pierida/Colias/eurytheme (alfalfa caterpillar)')
        self.assertTrue(result)
        self.assertEqual(order.errorMessage(), 'Insertion OK')
        self.assertEqual(order.categoryName,'Lepidoptera') 
        self.assertEqual(order.level,'Order')
        self.assertEqual(len(order.itemList),1)
        family = order.itemList[0]
        self.assertEqual(family.categoryName,'Pierida')
        self.assertEqual(family.level,'Family')
        self.assertEqual(len(family.itemList),1)
        genus = family.itemList[0]
        self.assertEqual(genus.categoryName,'Colias')
        self.assertEqual(genus.level,'Genus') 
        self.assertEqual(len(genus.itemList),1)
        self.assertEqual(genus.itemList[0],'eurytheme (alfalfa caterpillar)')
        self.assertEqual(order.list(), 'Lepidoptera (Pierida (Colias (eurytheme (alfalfa caterpillar))))')
 
    def test_insert2(self):
        '''Test inserting a species into a nonempty taxomony'''
        order = taxonomy.Taxonomy('dragons', "Order")
        result = order.insert('Middle/Earth/Smaug')
        self.assertTrue(result)
        self.assertEqual(order.errorMessage(), 'Insertion OK')
        self.assertEqual(order.categoryName,'dragons') 
        self.assertEqual(order.level,'Order')
        self.assertEqual(len(order.itemList),1)
        family = order.itemList[0]
        self.assertEqual(family.categoryName,'Middle')
        self.assertEqual(family.level,'Family')
        self.assertEqual(len(family.itemList),1)
        genus = family.itemList[0]
        self.assertEqual(genus.categoryName,'Earth')
        self.assertEqual(genus.level,'Genus') 
        self.assertEqual(len(genus.itemList),1)
        self.assertEqual(genus.itemList[0],'Smaug')
        
        result = order.insert('Middle/Earth/Ancalcagon the Black')
        self.assertTrue(result)
        self.assertEqual(order.errorMessage(), 'Insertion OK')
        self.assertEqual(order.categoryName,'dragons') 
        self.assertEqual(order.level,'Order')
        self.assertEqual(len(order.itemList),1)
        family = order.itemList[0]
        self.assertEqual(family.categoryName,'Middle')
        self.assertEqual(family.level,'Family')
        self.assertEqual(len(family.itemList),1)
        genus = family.itemList[0]
        self.assertEqual(genus.categoryName,'Earth')
        self.assertEqual(genus.level,'Genus') 
        self.assertEqual(len(genus.itemList),2)
        self.assertEqual(genus.itemList[0],'Smaug')
        self.assertEqual(genus.itemList[1],'Ancalcagon the Black')

        result3 = order.insert('Middle/Ages/Lola')
        self.assertTrue(result3)
        self.assertEqual(order.errorMessage(), 'Insertion OK')
        self.assertEqual(order.categoryName,'dragons') 
        self.assertEqual(order.level,'Order')
        self.assertEqual(len(order.itemList),1)
        family1 = order.itemList[0]
        self.assertEqual(family1.categoryName,'Middle')
        self.assertEqual(family1.level,'Family')
        self.assertEqual(len(family.itemList),2)
        genus0 = family1.itemList[0]
        self.assertEqual(genus.categoryName,'Earth')
        self.assertEqual(genus.level,'Genus') 
        genus1 = family.itemList[1]
        self.assertEqual(genus1.categoryName,'Ages')
        self.assertEqual(genus1.level,'Genus') 
        self.assertEqual(len(genus1.itemList),1)
        self.assertEqual(genus1.itemList[0],'Lola')

        #list subcategories
        self.assertEqual(genus1.list(), 'Ages (Lola)')
        self.assertEqual(family1.list(), 'Middle (Earth (Smaug, Ancalcagon the Black), Ages (Lola))')

    def test_insertion_errors(self):
        '''test error messages for attempting to insert wrong length input'''
        family = taxonomy.Taxonomy('Kitties', 'Family')
        result1 = family.insert('fluffy')
        self.assertFalse(result1)
        self.assertEqual(family.errorMessage(),'Error inserting fluffy into Kitties: wrong length')
        genus = taxonomy.Taxonomy('Earth','Genus')
        result2 = genus.insert('Middle/Earth/Smaug')
        self.assertEqual(genus.errorMessage(),'Error inserting Middle/Earth/Smaug into Earth: wrong length')
        

if __name__ == '__main__':
    unittest.main()
