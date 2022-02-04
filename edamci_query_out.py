import unittest
from rdflib import ConjunctiveGraph, Namespace
import json
import os
import pandas as pd

class EdamQueryTest(unittest.TestCase):

    @classmethod  
    def setUpClass(cls):  
        cls.edam_graph = ConjunctiveGraph()
        cls.edam_graph.parse(os.environ.get('EDAM_PATH'), format='xml')
        cls.report = pd.DataFrame(columns = ['Level','Test Name','Entity','Label','Debug Message'])
        print(cls.report)
        print("setupclass")
    
    def test_deprecated_replacement_obsolete(self):
        
        query = "queries/deprecated_replacement_obsolete.rq"
        with open(query,'r') as f:
            query_term = f.read()
        results = self.edam_graph.query(query_term)
        nb_err = len(results)
        f.close()

        for r in results:
            new_error = pd.DataFrame([['ERROR','deprecated_replacement_obsolete',r['entity'],r['label'],(f"concept is replaced by ({r['property']}) an obsolete concept: {r['replacement']}")]], columns=['Level','Test Name','Entity','Label','Debug Message'])
            self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True) 
            #self.report = self.report.append({'Level':'ERROR','Test Name':'deprecated_replacement_obsolete','Entity':r['entity'],'Label':r['label'],'Debug Message':(f"concept is replaced by ({r['property']}) an obsolete concept: {r['replacement']}")}, ignore_index=True)
        


        print(self.__class__.report)
        
        self.assertEqual(nb_err, 0)

    def test_super_class_refers_to_self(self):
        
        query = "queries/super_class_refers_to_self.rq"
        with open(query,'r') as f:
            query_term = f.read()

        results = self.edam_graph.query(query_term)
        nb_err = len(results)

        for r in results:
            new_error = pd.DataFrame([['ERROR','super_class_refers_to_self',r['entity'],r['label'],'concept declared as superclass of itself']], columns=['Level','Test Name','Entity','Label','Debug Message'])
            self.__class__.report = pd.concat([self.report, new_error],  ignore_index=True) 
        
        print(self.__class__.report)

    
        self.assertEqual(nb_err, 0)

if __name__ == '__main__':

    unittest.main()
