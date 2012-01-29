# DeprecaTED

			
			#print ".",
			# la chiave primaria è Incontri.id_incontro.property.key
			# a = Incontri.metadata.tables[Incontri.__tablename__]
			# master.metadata.tables[Incontri.__tablename__]
			# master.metadata.tables[Incontri.__tablename__].columns.id_incontro.primary_key
			# for i in Incontri.metadata.tables.values(): 
			#	if i.columns.id_incontro.primary_key: 
			#		print i, 'sdrfsdfsdf'
			
			# per trasformare una sqlalchemy query in un dizionario senza valori privati
			# dove b = sqlalch_query
			# dict([(x,y) for x,y in b.__dict__.items() if x[0] != '_'])

#tables_primarykeys = dict()
#for i in Incontri.metadata.tables.values(): 
    #for u in i.columns:
        #if u.primary_key: 
            #print (i.name, u.name)
            #tables_primarykeys[i.name] = u.name
			
# una lista modificata per 
#class TypedList(list):
    #def __init__(self, type):
        #self.type = type


#import hashlib
#converted = hashlib.sha1("My text").hexdigest()



	#def FetchAllFromTable(self, table_name):
		#"""Usage self.FetchAllFromTable(tablename) \n
		#where tablename could be a sqlalchemy's DeclarativeMeta o a raw table name. It works all the ways """
		#if isinstance(table_name, DeclarativeMeta): _table_name = table_name.__tablename__
		#else: _table_name = table_name
		#attrname = 'Table_'+_table_name
		#fetchall = self.execute('select * from %s' % _table_name)
		#fetchall = fetchall.fetchall()
		#setattr(self, attrname, [])
		#for record in fetchall:
			#getattr(self, attrname).append(QueryHasher(_table_name,record))
	#def FetchAllFromTable_SQLALchemy(self, table_name):
		#"""Usage self.FetchAllFromTable(tablename) \n
		#where tablename could be a sqlalchemy's DeclarativeMeta o a raw table name. It works all the ways """
		#if not isinstance(table_name, DeclarativeMeta): raise Exception('La tabella non è una classe DeclarativeBase')
		#attrname = 'Table_'+ table_name.__tablename__ + '_ALL'
		#fetchall = self.session.query(table_name).all()
		#setattr(self, attrname, fetchall)

class QueryHasher:
	def __init__(self, _table_name, row_tuple):
		# convert sqlalchemy.engine.base.RowProxy into pure sorted list !
		# sistemo con un sort l'ordine dei campi, cosi se cambia l'ordine delle colonne
		# non abbiamo eccezioni o casini
		# ANZI: ancora meglio. lavoro con il dizionario e buonanotte (l'esperienza insegna...)
		self.table_name = _table_name
		self.columns = row_tuple.keys()
		self.sqlalch_result = row_tuple
		#self.row = sorted(row_tuple)
		self.row = tuple(row_tuple)
		self.row_dict = dict(zip(self.sqlalch_result.keys(), self.sqlalch_result))
	def __eq__(self, other):
		return self.row_dict == other.row_dict
	def __hash__(self):
		return hash('|'.join([str(i) for i in self.row_dict.values()]))

# Preleva scaglioni di records e li confronta	
class Stagger:
	def __init__(self, number):
		pass


def GetTablesPrimaryKeys(db):
	tables_primarykeys = dict()
	for i in db.metadata.tables.values(): 
		#print 'ok'
		for u in i.columns:
			if u.primary_key: 
				#print (i.name, u.name)
				tables_primarykeys[i.name] = u.name
	return tables_primarykeys

# importare gli schemi adatti: py_mod = imp.load_source(mod_name, filepath)
# master_schema = imp.load_source('master_schema.py', DB_MAP_FOLDER+'/master_schema.py')
# slave_schema = imp.load_source('slave_schema.py', DB_MAP_FOLDER+'/slave_schema.py')
# sys.modules['master_schema'] = master_schema


		#self._master_table_name = master_table_hashed[0].table_name
		#self._slave_table_name = slave_table_hashed[0].table_name
		#self._master_table_name = master_table_hashed[0].__class__.__name__
		#self._slave_table_name = slave_table_hashed[0].__class__.__name__		
		#self._master_attrname = 'master_' + self._master_table_name
		#self._slave_attrname = 'slave_' + self._master_table_name		

	
	def SlaveUpdates(self):
		"""
		Fetch all rows from master that needs to be inserted in the slave
		Doesn't need arguments
		"""
		setattr(self, 'SlaveUpdates_'+self._Class_table_name, [])
	def SlaveUseless(self):
		"""
		Fetch all rows from slave that should be removed
		Doesn't need arguments
		"""
		setattr(self, 'SlaveUseless_'+self._Class_table_name, [])
	def SlaveDifferences(self):
		"""
		Fetch all rows from master db that exists on the slave but that are differents
		Doesn't need arguments
		"""
		setattr(self, 'SlaveDifferences_'+self._Class_table_name, [])


master_row = master.Query_allenatori_squadre.filter_by(data_inizio=datetime.date(2009,8,22),id_squadra=2,id_allenatore=2)[0]

pk_dict = {}
for cpk in g.master.Tables_PrimaryKeys[master_row.__tablename__]:
	pk_dict[cpk] = getattr(master_row, cpk)

where_st = ''
for up_row in g.ProposedUpdates: 
	#pk_value = self.ProposedUpdates[pk_name]
	#d = getattr(self.slave, 'Query_'+self.table_name).get(i)
	##d_dict = dict([(x,y) for x,y in d.__dict__.items() if x[0] != '_'])
	for pk_name in pk_s:
		where_st += "%s==%s," % (pk_name,up_row[pk_name])
	ex = ups.where(pk_c==pk_value).values(**up_row)
	ex.execute()

pk_s =  g.slave.Tables_PrimaryKeys[g.table_name]

pk_col_name = []
for i in pk_s:
	c_n = getattr(g.slave.metadata.tables[g.table_name].c, i)
	pk_col_name.append((i,c_n))

for up_row in self.ProposedUpdates: 
    d_query = {}
    for u in geattr(self.slave, 'PrimaryKeys_'+self.table_name):
	d_query[u] = up_row[u]
	
for up_row in g.ProposedUpdates: 
    d_query = {}
    for u in getattr(g.slave, 'PrimaryKeys_'+g.table_name):
	d_query[u] = up_row[u]
	slave_row = getattr(g.slave, 'Query_'+g.table_name).filter_by(**d_query).update(up_row)
