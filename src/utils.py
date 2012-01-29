import os
from settings import *
from filematcher import *

def SQLAutoCodeMap(nome_tipo, argparse_object):
	if not nome_tipo in ['master', 'slave']: raise Exception('ERROR: Can\'t inspect unknow Database type name. Set a master and a slave DB type')
	msg = """ 
	
	Inspecting DB %s to Map it in SQLalchemy behaviour :
	
	""" % nome_tipo
	print msg
	#os.system('sqlautocode -d -e %s -o %s/%s_schema.py' %\
	os.system('sqlautocode --noindex -d %s -o %s/%s_schema.py' %\
	(argparse_object.__getattribute__(nome_tipo), SAFE_DB_MAP_FOLDER, nome_tipo, ))


def Verify_DBMAPS_Folder():
	try: os.listdir(DB_MAP_FOLDER)
	except: os.mkdir(DB_MAP_FOLDER)	
	try: 
		os.listdir(DB_MAP_FOLDER)
		print 'DBMAPS folder successfull identified... OK.'
		return 0
	except: 
		raise Exception('DB Maps Directory creation failed in %s !' % DB_MAP_FOLDER )
		return 1

def SchemaComparator():
	master_f = 	File(DB_MAP_FOLDER+'/master_schema.py' , 'r')
	slave_f = 	File(DB_MAP_FOLDER+'/slave_schema.py' , 'r')
	if master_f == slave_f: return 0
	else: raise Exception('ERROR: master and slave schema maps DIFFERS ! You must sync the Schema first to avoid data truncations or unbound columns. Do a diff between master and slave maps and look their differencies, if they are incosistent change CHECK_SCHEMA flag inside settings.py')
	
