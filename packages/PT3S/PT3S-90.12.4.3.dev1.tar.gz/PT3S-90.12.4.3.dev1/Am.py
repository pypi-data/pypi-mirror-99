"""

"""

__version__='90.12.4.3.dev1'



import os
import sys


import re
import pandas as pd
import numpy as np
import warnings
import tables

import h5py
import time

import base64
import struct

import logging

import glob


import math

import pyodbc

import argparse
import unittest
import doctest

# ---
# --- PT3S Imports
# ---
logger = logging.getLogger('PT3S')  
if __name__ == "__main__":
    logger.debug("{0:s}{1:s}".format('in MODULEFILE: __main__ Context:','.')) 
else:
    logger.debug("{0:s}{1:s}{2:s}{3:s}".format('in MODULEFILE: Not __main__ Context: ','__name__: ',__name__," .")) 

try:
    from PT3S import Dm
except ImportError:
    logger.debug("{0:s}{1:s}".format('ImportError: ','from PT3S import Dm - trying import Dm instead ... maybe pip install -e . is active ...')) 
    import Dm

try:
    from PT3S import Xm
except ImportError:
    logger.debug("{0:s}{1:s}".format('ImportError: ','from PT3S import Xm - trying import Xm instead ... maybe pip install -e . is active ...')) 
    import Xm
   
class AmError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Am():
    """SIR 3S AccessDB to pandas DataFrames.

    Args:
        * accFile (str): SIR 3S AccessDB
           
    Attributes:
       
    Raises:
        AmError
    """

               
    def __init__(self,accFile):

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:             
            if os.path.exists(accFile):  
                if os.access(accFile,os.W_OK):
                    pass
                else:
                    logger.debug("{:s}accFile: {:s}: Not writable.".format(logStr,accFile)) 
                    if os.access(accFile,os.R_OK):
                        pass
                    else:
                        logStrFinal="{:s}accFile: {:s}: Not readable!".format(logStr,accFile)     
                        raise AmError(logStrFinal)  
            else:
                logStrFinal="{:s}accFile: {:s}: Not existing!".format(logStr,accFile)     
                raise AmError(logStrFinal)  
          
            logger.debug("{:s}accFile (abspath): {:s}".format(logStr,os.path.abspath(accFile))) 

            Driver=[x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')]
            if Driver == []:
                logStrFinal="{:s}{:s}: No Microsoft Access Driver!".format(logStr,accFile)     
                raise AmError(logStrFinal)  

            conStr=(
                r'DRIVER={'+Driver[0]+'};'
                r'DBQ='+accFile+';'
                )
            logger.debug("{0:s}conStr: {1:s}".format(logStr,conStr)) 

            con = pyodbc.connect(conStr)
            cur = con.cursor()

            # all Tables in DB
            tableNames=[table_info.table_name for table_info in cur.tables(tableType='TABLE')]
            logger.debug("{0:s}tableNames: {1:s}".format(logStr,str(tableNames))) 
            allTables=set(tableNames)
          
            self.dataFrames={}

            # process pairTables
            pairTables=set()

            pairViews=set()
            pairViews_BZ=set()
            pairViews_ROWS=set()
            pairViews_ROWT=set()
            pairViews_ROWD=set()

            try:
                dfViewModelle=pd.read_sql('select * from VIEW_MODELLE',con)
            except pd.io.sql.DatabaseError as e:
                logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                logger.error(logStrFinal) 
                raise AmError(logStrFinal)
            
            try:
                dfCONT=pd.read_sql('select * from CONT',con)
            except pd.io.sql.DatabaseError as e:
                logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                logger.error(logStrFinal) 
                raise AmError(logStrFinal)   

            try:
                dfKNOT=pd.read_sql('select * from KNOT',con)
            except pd.io.sql.DatabaseError as e:
                logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                logger.error(logStrFinal) 
                raise AmError(logStrFinal)   


            # Paare
            for pairType in ['_BZ','_ROWS','_ROWT','_ROWD']:
                logger.debug("{0:s}pairType: {1:s}: ####".format(logStr,pairType)) 
                tablePairsBVBZ=[(re.search('(?P<BV>[A-Z,1,2]+)('+pairType+')$',table_info.table_name).group('BV'),table_info.table_name) for table_info in cur.tables(tableType='TABLE') if re.search('(?P<BV>[A-Z,1,2]+)('+pairType+')$',table_info.table_name) != None]
                for (BV,BZ) in tablePairsBVBZ:

                    if BV not in tableNames:
                        logger.debug("{0:s}BV: {1:s}: Tabelle gibt es nicht. Falsche Paar-Ermittlung? Weiter. ".format(logStr,BV)) 
                        continue
                    if BZ not in tableNames:
                        logger.debug("{0:s}BZ: {1:s}: Tabelle gibt es nicht. Falsche Paar-Ermittlung? Weiter. ".format(logStr,BZ)) 
                        continue
                    
                    if BZ == 'PGRP_PUMP_BZ': # BV: PUMP BVZ: PGRP_PUMP_BZ V: V_PUMP - Falsch!; wird unten ergaenzt
                        continue
                                        
                    df=Dm.f_HelperBVBZ(
                                    con
                                   ,BV
                                   ,BZ                                 
                                    )


                    df=Dm.f_HelperDECONT(
                        df
                       ,dfViewModelle 
                       ,dfCONT
                        )

                                                                                                                                                        
                    VName='V_BVZ_'+BV
                    self.dataFrames[VName]=df
                    logger.debug("{0:s}BV: {1:s} BVZ: {2:s} V: {3:s}".format(logStr,BV,BZ,VName))                     

                    pairTables.add(BV)
                    pairTables.add(BZ)
                    
                    pairViews.add(VName)

                    if pairType=='_BZ':
                        pairViews_BZ.add(VName)
                    elif pairType=='_ROWS':
                        pairViews_ROWS.add(VName)
                    elif pairType=='_ROWT':
                        pairViews_ROWT.add(VName)
                    elif pairType=='_ROWD':
                        pairViews_ROWD.add(VName)

            # BVZ-Paare Nachzuegler
            for (BV,BZ) in [('PGRP_PUMP','PGRP_PUMP_BZ')]:
                                       
                    df=Dm.f_HelperBVBZ(
                                    con
                                   ,BV
                                   ,BZ                              
                                    )                              

                    df=Dm.f_HelperDECONT(
                        df
                       ,dfViewModelle 
                       ,dfCONT
                        )
                                                   
                    VName='V_BVZ_'+BV                    
                    self.dataFrames[VName]=df
                    logger.debug("{0:s}BV: {1:s} BVZ: {2:s} V: {3:s}".format(logStr,BV,BZ,VName)) 

                    pairTables.add(BV)
                    pairTables.add(BZ)

                    pairViews.add(VName)
                    pairViews_BZ.add(VName)

            # Nicht-Paare             
            notInPairTables=sorted(allTables-pairTables)           
            notInPairTablesW=[ # W: "Sollwert"; erwartete SIR 3S Tabellen, die nicht Paare sind
                'AB_DEF', 'AGSN', 'ARRW', 'ATMO'
               ,'BENUTZER', 'BREF'
               ,'CIRC', 'CONT', 'CRGL'
               ,'DATENEBENE'
               ,'DPGR_DPKT'
               ,'DPKT' # 90-12 ein Paar
               ,'DRNP'
               ,'ELEMENTQUERY'
               ,'FSTF', 'FWBZ'
               ,'GEOMETRY_COLUMNS' # 90-12
               ,'GKMP', 'GMIX', 'GRAV', 'GTXT'
               ,'HAUS'
               ,'LAYR', 'LTGR'
               ,'MODELL'
               ,'MWKA' # nicht 90-12
               ,'NRCV'
               ,'OVAL'
               ,'PARV', 'PGPR', 'PLYG', 'POLY', 'PROZESSE', 'PZON'
               ,'RCON', 'RECT', 'REGP'
               ,'RMES_DPTS'#, 'RMES_DPTS_BZ'
               ,'ROHR_VRTX', 'RPFL', 'RRCT'
               ,'SIRGRAF', 'SOKO', 'SPLZ', 'STRASSE', 'SYSTEMKONFIG'
               ,'TIMD', 'TRVA'
               ,'UTMP'
               ,'VARA', 'VARA_CSIT', 'VARA_WSIT', 'VERB', 'VKNO', 'VRCT'
               ,'WBLZ']
            
            # erwartete SIR 3S Tabellen, die nicht Paare sind
            notPairTables=set()        
            notPairViews=set()            
            for tableName in  notInPairTablesW: 


                 if tableName not in tableNames:
                        logger.debug("{0:s}tableName: {1:s}: Tabelle gibt es nicht - falsche Annahme in diesem Modul bzgl. der existierenden SIR 3S Tabellen? Weiter. ".format(logStr,tableName)) 
                        continue

                 sql='select * from '+tableName 
                 try:
                        df=pd.read_sql(sql,con)
                        self.dataFrames[tableName]=df
                        notPairTables.add(tableName)
                 except pd.io.sql.DatabaseError as e:
                        logger.info("{0:s}sql: {1:s}: Fehler?! Weiter. ".format(logStr,sql)) 
                        continue

                 df=Dm.f_HelperDECONT(
                    df
                   ,dfViewModelle 
                   ,dfCONT
                    )
              
                 VName='V_'+tableName
                 logger.debug("{0:s}V: {1:s}".format(logStr,VName)) 
                 self.dataFrames[VName]=df
                 notPairViews.add(VName)

            # unerwartete Tabellen
            notPairViewsProbablyNotSir3sTables=set()       
            notPairTablesProbablyNotSir3sTables=set()       
            for tableName in  set(notInPairTables)-set(notInPairTablesW):

                 logger.debug("{0:s}tableName: {1:s}: Tabelle keine SIR 3S Tabelle aus Sicht dieses Moduls. Trotzdem lesen. ".format(logStr,tableName)) 

                 sql='select * from '+tableName 
                 try:
                        df=pd.read_sql(sql,con)
                        self.dataFrames[tableName]=df
                        notPairTablesProbablyNotSir3sTables.add(tableName)
                 except pd.io.sql.DatabaseError as e:
                        logger.info("{0:s}sql: {1:s}: Fehler?! Weiter. ".format(logStr,sql)) 
                        continue

                 df=Dm.f_HelperDECONT(
                    df
                   ,dfViewModelle 
                   ,dfCONT
                    )
                 
                 VName='V_'+tableName
                 logger.debug("{0:s}V: {1:s}".format(logStr,VName)) 
                 self.dataFrames[VName]=df
                 notPairViewsProbablyNotSir3sTables.add(VName)

            self.viewSets={}

            self.viewSets['pairViews']=sorted(pairViews)
            self.viewSets['pairViews_BZ']=sorted(pairViews_BZ)
            self.viewSets['pairViews_ROWS']=sorted(pairViews_ROWS)
            self.viewSets['pairViews_ROWT']=sorted(pairViews_ROWT)
            self.viewSets['pairViews_ROWD']=sorted(pairViews_ROWD)
            
            self.viewSets['notPairTables']=sorted(notPairTables)
            self.viewSets['notPairTablesProbablyNotSir3sTables']=sorted(notPairTablesProbablyNotSir3sTables)
            self.viewSets['notPairViews']=sorted(notPairViews)
            self.viewSets['notPairViewsProbablyNotSir3sTables']=sorted(notPairViewsProbablyNotSir3sTables)

            # KNOT (V3_KNOT)
            vKNOT=Dm.f_HelperVKNO(
                    self.dataFrames['V_BVZ_KNOT']
                   ,self.dataFrames['V_VKNO']                   
                    )            
            self.dataFrames['V3_KNOT']=vKNOT

            # VBEL (V3_VBEL)           
            vVBEL_UnionList=[]
            for vName in self.viewSets['pairViews_BZ']:                
                dfVBEL=self.dataFrames[vName]
                if 'fkKI' in dfVBEL.columns.to_list():
                    df=pd.merge(dfVBEL,vKNOT,left_on='fkKI',right_on='pk',suffixes=('','_i'))           
                    if 'fkKK' in df.columns.to_list():
                        df=pd.merge(df,vKNOT,left_on='fkKK',right_on='pk',suffixes=('','_k'))
                        m=re.search('^(V_BVZ_)(\w+)',vName)         
                        OBJTYPE=m.group(2)
                        df=df.assign(OBJTYPE=lambda x: OBJTYPE)

                        logger.debug("{0:s}{1:s} in VBEL-View ...".format(logStr,OBJTYPE))     
                        vVBEL_UnionList.append(df)

            vVBEL=pd.concat(vVBEL_UnionList)
            vVBEL=Xm.Xm.constructNewMultiindexFromCols(df=vVBEL,mColNames=['OBJTYPE','pk'],mIdxNames=['OBJTYPE','OBJID'])
            vVBEL.sort_index(level=0,inplace=True)
            self.dataFrames['V3_VBEL']=vVBEL

            # DPKT (V3_DPKT)    
            if 'V_DPKT' in self.dataFrames.keys():
                vDPKT=self.dataFrames['V_DPKT']                
            elif 'V_BVZ_DPKT' in self.dataFrames.keys():
                vDPKT=self.dataFrames['V_BVZ_DPKT']            
            vDPKT_DPGR1=pd.merge(vDPKT,self.dataFrames['V_DPGR_DPKT'],left_on='pk',right_on='fkDPKT',suffixes=('','_DPGR1')) # fk der DPGR ermitteln
            vDPKT_DPGR=pd.merge(vDPKT_DPGR1,self.dataFrames['V_BVZ_DPGR'],left_on='fkDPGR',right_on='pk',suffixes=('','_DPGR')) # Daten der DPGR (vor allem der NAME der DPGR)
            self.dataFrames['V3_DPKT']=vDPKT_DPGR[[
              'pk'
             ,'OBJTYPE'
             ,'fkOBJTYPE'
             ,'ATTRTYPE'
             ,'EPKZ'
             ,'TITLE'
             ,'UNIT'
             ,'FLAGS'             
             ,'CLIENT_ID'
             ,'OPCITEM_ID'
             ,'pk_DPGR'
             ,'NAME'
            ]].drop_duplicates().reset_index(drop=True)
                                                        
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise AmError(logStrFinal)              
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

  



