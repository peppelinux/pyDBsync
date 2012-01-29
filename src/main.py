#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
#import imp

from validator import *
from settings import *
from utils import *


parser = argparse.ArgumentParser(description='Sync two Databases', epilog="Es: python main.py -run test --db-master=mysql://root:remotepasswd@192.168.0.212/dbname --db-slave=mysql://root:passwdx@localhost/dbname")
parser.add_argument('-run', dest='run', action='store',  type=str, choices=['test','execute'], required=True,
					help='Test Produce only a simulation. Execute does the job !')
parser.add_argument('--no-schemacheck', required=False, action='store_true', help='disable schema check. Use it only if you are shure that the DB\'s schemas are identical and you want bypass the diff valuation of the DB_maps files.')					
#parser.add_argument('--verbose', required=False, action='store_true', help='view a lot of usefull/useless output')					
parser.add_argument('--db-master', dest='master', action='store',
                   required=True, help='es: mysql://user:password@hostname[:3306]/dbname where the data is taken from',
				   type=RegexValidator(DB_CONNECTOR_PATTERN))
				   
parser.add_argument('--db-slave', dest='slave', action='store',
					type=RegexValidator(DB_CONNECTOR_PATTERN),
                   required=True, help='es: mysql://user:password@hostname[:3306]/dbname where we need to store and sync the data taken from master')
parser.add_argument('--tables', required=True, action='store', help='tables names separated by a comma and no space, like this: --tables users,groups,tb_matchs')					
parser.add_argument('--version', action='version', version='pySyncDB 0.1a')

if __name__ == '__main__':
	# fetch arguments from sys.args with a little help from argsparse module :)
	args = parser.parse_args()

	# control if the folder where the tables_maps will stored exists
	Verify_DBMAPS_Folder()
	
	# DO backup
	# TODO: a procedure to do a backups with creational statements and insert queries from sqlalchemy
	# Backup(db_name)
	
	# producing tables_maps with sqlautocode helps a lot :)
	SQLAutoCodeMap('master', args)
	SQLAutoCodeMap('slave', args)
	
	# if there's not the --no-schemacheck this will start the Schema Comparison to control 
	# that the two files are identical
	if not args.no_schemacheck: SchemaComparator()
	
	# use imp to import the tables_schemes. This make all the things more simple !
	# deprecated: I abandoned it because of ugly warnings like this:
	# RuntimeWarning: Parent module 'master_schema' not found while handling absolute import...
	#master_schema = imp.load_source('master_schema.py', DB_MAP_FOLDER+'/master_schema.py')
	#slave_schema = imp.load_source('slave_schema.py', DB_MAP_FOLDER+'/slave_schema.py')
	
	# now I use simply this :)
	sys.path.append(DB_MAP_FOLDER)
	from pydbsync import *
	
	master = SessionManager('master', args.master)
	slave = SessionManager('slave', args.slave)
	
	for table in args.tables.split(','):
		if args.run == 'test': args.run = None
		g = pyTableSyncManager(master, slave, table, args.run)

		g.InspectTable()
		if g.ProposedUpdates:
		    g.CommitUpdates()
		if g.ProposedInsertions:
		    g.CommitInsertions()
		if g.ProposedDeletions:
		    g.CommitDeletions()
		
		# purge it! 
		del(g)
	
	
