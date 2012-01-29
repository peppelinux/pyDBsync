#test pySyncDB

from main import *

args = parser.parse_args(['-run=test', '--no-schemacheck' ,'--db-master=mysql://root:xXx@192.168.0.212/ultrabet', '--db-slave=mysql://root:xXx@localhost/ultrabet', '--tables=annotazioni_squadre'])


sys.path.append(DB_MAP_FOLDER)

from pydbsync import *

master = SessionManager('master', args.master)
slave = SessionManager('slave', args.slave)


g = pyTableSyncManager(master, slave, 'arbitri_campionato_stagione', args.run)

g.InspectTable()

if g.ProposedUpdates:
    g.CommitUpdates()

if g.ProposedInsertions:
    g.CommitInsertions()

if g.ProposedDeletions:
    g.CommitDeletions()

python main.py --no-schemacheck -run test --db-master=mysql://root:xXx@192.168.0.212/ultrabet --db-slave=mysql://root:xXx@127.0.0.1/ultrabet --tables allenatori,allenatori_squadre,annotazioni_squadre,\
arbitri_campionato_stagione,campionati,cartellini_incontro,\
corner_incontro,rete_minuto_incontro,derby,gruppi,gruppi_campionati_stagioni,\
squadre,squadre_campionato_stagione,squadre_seriali,stagioni,\
incontri,nazioni,note_incontri,pesi_indicatori,pos_campionato_stagione,\
scommesse_campi_significati,soglie_under_over,tab_condizione,tab_range_pesi,\
tab_scommesse_campi,tab_stagioni,tab_valori_asiatica,tipo_obiettivo,\
tipo_scommessa

