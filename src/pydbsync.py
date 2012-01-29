# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import relation
import copy

from sqlalchemy.orm import sessionmaker

DeclarativeBase = declarative_base()
from master_schema import *

def FindTableClassName(stringa):
	s = stringa.split('_')
	s = ''.join([i.capitalize() for i in s])
	s = s.split(' ')[:128]
	return eval(s[0])
	
class pyTableSyncManager:
	def __init__(self, master, slave, table_name, mode):
		"""
		needs two SessionManager Objects, master and slave, and an SqlAlchemy Table Object
		"""
		self.master = master
		self.slave = slave
		self.mode = mode
		if not isinstance(table_name, DeclarativeMeta): 
			try:
				table_name = FindTableClassName(table_name)
				if not isinstance(table_name, DeclarativeMeta): raise Exception('La tabella %s is not a DeclarativeBase class' % table_name )
			except:
				raise Exception('La tabella %s is not a DeclarativeBase class' % table_name ) 		
		self._Class_table_name = table_name
		self.table_name = self._Class_table_name.__tablename__
		self.master.ManageTable(table_name)
		self.slave.ManageTable(table_name)
		self.ProposedUpdates = []
		self.ProposedDeletions = []
		self.ProposedInsertions = []
	def flush(self):
		self.ProposedUpdates = []
		self.ProposedDeletions = []
		self.ProposedInsertions = []
	def _BuildAttrName(self, uword, content):
		if not hasattr(self, uword+'_'+self._Class_table_name.__name__):
			setattr(self, uword+'_'+self._Class_table_name.__name__, content )
	def CommitDeletions(self):
		if self.ProposedDeletions:	
			for i_dict in self.ProposedDeletions: 
				d = getattr(self.slave, 'Query_'+self.table_name).filter_by(**i_dict)
				self.slave.session.delete(d[0])
				#print d.all()	
		self.ProposedDeletions  = []
		if self.mode == 'execute': 
			self.slave.session.commit()
			print 'Deletions committed on %s' % self.table_name
	def CommitUpdates(self):
		if self.ProposedUpdates: 
			pk_s =  self.master.Tables_PrimaryKeys[self.table_name]
			pk_col_name = {}
			for i in pk_s:
				c_n = getattr(self.slave.metadata.tables[self.table_name].c, i)
				pk_col_name[i] = c_n
				
			for up_row in self.ProposedUpdates: 
				d_query = {}
				for u in getattr(self.slave, 'PrimaryKeys_'+self.table_name):
					d_query[u] = up_row[u]
				
				slave_row = getattr(self.slave, 'Query_'+self.table_name).filter_by(**d_query).update(up_row)
		self.ProposedUpdates  = []
		if self.mode == 'execute': 
			self.slave.session.commit()
			print 'Updates committed on %s' % self.table_name
	
	def CommitInsertions(self):
		if self.ProposedInsertions: 
			ins = self.slave.metadata.tables[self.table_name].insert()
			for i in self.ProposedInsertions: 
				ins.execute(i)				
		self.ProposedInsertions = []
		if self.mode == 'execute': 
			self.slave.session.commit()
			print 'Insertions committed on %s' % self.table_name
	def HaveSameRecordNumber(self):
		"""
		Check if the master and the slave have the same rows number.
		Doesn't need arguments
		"""
		print """
			Check if the master.%s and slave.%s have the same rows number:
		""" % (self.table_name, self.table_name), 
		self.len_master_table = getattr(self.master, 'Query_' + self.table_name).count()
		self.len_slave_table = getattr(self.slave, 'Query_' + self.table_name).count()
		if self.len_master_table == self.len_slave_table: return True
		else: return False
	def GetProposedSlaveUpdates(self, master_row):
		"""
		Contains the procedure to check if a row on the master is present on the slave
		"""
		table_name = master_row.__tablename__
		
		# se si fossero degnati di fare una chiave primaria singola questo comando sarebbe bastato per salvare l'umanità dall'oblìo
		# invece devo scrivere il codice per coloro i quali hanno creato chiavi primarie composte da più di un campo...
		
		# ecco il codice che giustifica il disagio mentale dell'umanità in un dizionario
		pk_dict = {}
		for cpk in self.master.Tables_PrimaryKeys[master_row.__tablename__]:
			pk_dict[cpk] = getattr(master_row, cpk)

		# usefull  messages 
		message1 = '%s row with primarykey %s: is the the same' % (self.table_name, '|'.join([i.__str__() for i in pk_dict.values()])) 
		message2 = '%s row with primarykey %s: needs to be inserted' % (self.table_name, '|'.join([i.__str__() for i in pk_dict.values()])) 
		message3 = '%s row with primarykey %s: needs to be updated' % (self.table_name, '|'.join([i.__str__() for i in pk_dict.values()])) 
		
		master_row_dict = dict([(x,y) for x,y in master_row.__dict__.items() if x[0] != '_'])
		
		slave_row = getattr(self.slave, 'Query_'+self.table_name).filter_by(**pk_dict)
		if not slave_row.all():
			self.ProposedInsertions.append(master_row_dict)
			print message2
			return 0
		
		if slave_row.all():
			slave_row_dict = dict([(x,y) for x,y in slave_row[0].__dict__.items() if x[0] != '_'])
		
		if master_row_dict != slave_row_dict: 
			self.ProposedUpdates.append(master_row_dict)
			print message3
			return 0
		
	def GetProposedSlaveDeletions(self, slave_row):
		table_name = slave_row.__tablename__
		pk_dict = {}
		for cpk in self.master.Tables_PrimaryKeys[slave_row.__tablename__]:
			pk_dict[cpk] = getattr(slave_row, cpk)		
		
		message1 = '%s row with primarykey %s: needs to be deleted in the slave !' % (self.table_name, '|'.join([i.__str__() for i in pk_dict.values()])) 
		
		slave_row_dict = dict([(x,y) for x,y in slave_row.__dict__.items() if x[0] != '_'])
		
		master_row = getattr(self.master, 'Query_'+self.table_name).filter_by(**pk_dict)
		#print master_row.all()
		if not master_row.all():
			self.ProposedDeletions.append(slave_row_dict)
			print message1
			return 0	
	def InspectTable(self):		
		print 'I\'m getting all the rows from the master.%s. This could take a while...' % self.table_name
		if not hasattr(self, 'master_'+self._Class_table_name.__name__):
			self._BuildAttrName( 'master', getattr(self.master, 'Query_'+ self.table_name).all())
		
		print 'I\'m getting all the rows from the slave.%s. This could take a while...' % self.table_name
		if not hasattr(self, 'self_'+self._Class_table_name.__name__):
			self._BuildAttrName( 'slave', getattr(self.slave, 'Query_'+ self.table_name).all())
		
		# flush oldies and renew the master/slave comparison
		self.flush()
		#
		
		# check if rows in the master needs to be inserted or updated in the slave
		for master_row in getattr(self, 'master_'+self._Class_table_name.__name__):
			self.GetProposedSlaveUpdates(master_row)
		
		# check if rows in the master needs to be inserted or updated in the slave
		for slave_row in getattr(self, 'slave_'+self._Class_table_name.__name__):
			self.GetProposedSlaveDeletions(slave_row)
		
		
def GetTablesPrimaryKeys(db):
	tables_primarykeys = dict()
	for i in db.metadata.tables.values(): 
		#print 'ok'
		tables_primarykeys[i.name] = []
		for u in i.columns:
			if u.primary_key: 
				#print (i.name, u.name)
				tables_primarykeys[i.name].append(u.name)
	return tables_primarykeys


class SessionManager:
	def __init__(self, db_type, db_conn_string):
		self.supported_type = ['master', 'slave']
		if db_type in self.supported_type:
			self.type = db_type
		else: raise Exception('db_type not valid', 'supported type are: %s' % (','.join(self.supported_type)) )
		self.engine = create_engine(db_conn_string)
		self.metadata = DeclarativeBase.metadata
		self.metadata.bind = self.engine
		self.session = sessionmaker(bind=self.engine)()
		self.connection = self.session.connection()
		self.execute = self.connection.execute
		self.Tables_PrimaryKeys = GetTablesPrimaryKeys(self)
		self.Tables = sorted(DeclarativeBase.metadata.tables.keys())
	def ManageTable(self, table_name):
		if not isinstance(table_name, DeclarativeMeta): 
			try:
				table_name = FindTableClassName(table_name)
				if not isinstance(table_name, DeclarativeMeta): raise Exception('La tabella non è una classe DeclarativeBase')
			except:
				raise Exception('La tabella %s non è una classe DeclarativeBase' % table_name ) 
		setattr(self, 'Query_'+ table_name.__tablename__, self.session.query(table_name))
		setattr(self, 'Model_'+ table_name.__tablename__, table_name)
		setattr(self, 'PrimaryKeys_'+ table_name.__tablename__, self.Tables_PrimaryKeys[table_name.__tablename__])
	def FreeMemory(self, table_name):
		if not isinstance(table_name, DeclarativeMeta): raise Exception('La tabella non è una classe DeclarativeBase')
		delattr(self, 'Query_'+ table_name.__tablename__)
		delattr(self, 'Model_'+ table_name.__tablename__)
		delattr(self, 'PrimaryKeys_'+ table_name.__tablename__)
	def save_and_clean_cache(self):
		self.engine.session.commit()
		self.engine.session.rollback()
	def rollback(self):
		self.engine.session.rollback()

		
