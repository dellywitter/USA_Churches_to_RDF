# Python script converting tabular data into RDF form
# Data specific
# MASWS CW1P2

import csv, os, re, string, sys
import xml.dom.minidom
class Schemar(object):
	def __init__(self):
		self.denominations=dict()
	# open a text file
	# return a string 
	def openFile(self,file_name):
		f = open(file_name, 'r')
		try:
		    text = f.readlines()#text is a list of strings ending with \r\n tags
		finally:
			f.close()
			return text
	# associate the denomination acronyms with the denominations themselves
	def feedDenominations(self,text):
		for line in text:
			l=line[:-2].split(" - ")
			self.denominations[l[0]]=l[2]
	
	def process(self, text):
		id=0
		w = open("MegachurchesTriples.rdf","wb")
		w.write("@prefix megachurches: <http://vocab.inf.ed.ac.uk/megachurches#> .\n")
		w.write ("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
		w.write ("@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n")
		w.write ("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n")
		w.write ("@prefix places: <http://purl.org/ontology/places#> .\n")
		w.write ("@prefix usgov: <http://www.rdfabout.com/rdf/usgov/geo/us/>.\n")
		w.write ("@prefix db: <http://dbpedia.org/ontology/> .\n")
		w.write ("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n")
		w.write ("@prefix url: <http://purl.org/dc/dcmitype/> .\n")
		w.write ("@prefix dc: <http://purl.org/dc/elements/1.1/> .\n")
		w.write ("@prefix owl: <http://www.w3.org/2002/07/owl#> .\n")
		for line in text:
			id=id+1
			triple=line[:-2].split("\t")
			num=str(triple[5])
			denom=self.denominations[triple[len(triple)-1]]
			someline="megachurches:"+str(id)+" a megachurches:Megachurch ; \n" +\
			"\t"+"megachurches:name \"" + triple[1]+"\" ; \n "+ \
			"\t"+"megachurches:senior_minister \""+triple[2]+"\" ; \n"+\
			"\t"+"megachurches:identifier" +" \""+triple[0]+"\""+" ; \n"+\
			"\t"+"megachurches:weeklyAttendance " + "\""+num +"\"^^xsd:int"+" ; \n"+\
			"\t"+"places:City "+ "\""+str(triple[3])+"\""+" ; \n"+"\t"+\
			 "places:State "+ "usgov:"+ str(triple[4])+" ; \n"+\
			"\t"+"db:religion " + "\""+denom+"\""+" . \n"
			w.write(someline)
def main():
	s=Schemar()
	s.feedDenominations(s.openFile("churchURIs.txt"))
	s.process(s.openFile("churches-2.txt"))
if __name__=="__main__":
	main()