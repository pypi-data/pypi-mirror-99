#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 15:43:23 2021

@author: zhihao
"""

import pymysql
from clickhouse_driver import Client
import os
import psutil
import sys
import math



def connectMySql(DBNAME, DBPASS, DBHOST="localhost", DBUSER="root"):
    try:
        db=pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
        print('mysql数据库连接成功！')  
    except pymysql.Error as e:
        print('mysql数据库连接失败 '+str(e))
        os._exit(0)
    return db

def connectClickHouse(ckDBNAME, ckDBHOST="localhost", ckDBPORT="9000", ckDBUSER="default", ckDBPASS=""):
    try:
        ckClient=Client(host=ckDBHOST, port=ckDBPORT, user=ckDBUSER, database=ckDBNAME, password=ckDBPASS)
        print('clickhouse数据库连接成功 !')
    except ckClient.Error as e:
        print('clickhouse数据库连接失败' + str(e))   
        os._exit(0)
    return ckClient


def getMemorySize():
    #readin the size of the free memory
    phyMemory=psutil.virtual_memory()
    sizeMemory=int(phyMemory.free / 1024 / 1024)
    print('空余内存为(MB) ' + str(sizeMemory))
    return sizeMemory



def estimateBatchFetch(myCursor, TBNAME):    
    query_row = " SELECT COUNT(*) from "  + TBNAME
    myCursor.execute(query_row)
    rowResult = myCursor.fetchall()
    numRow = rowResult[0][0]
    print('mySQL表的总条数是 ' + str(numRow))
    # estimate the total size for all data of the table
    query2 = "SELECT * from " + TBNAME
    myCursor.execute(query2)
    Stock_sample = myCursor.fetchone() 
    sizeOne = [sys.getsizeof(Stock_sample)/(1024*1024)][0]
    sizeTot = sizeOne * numRow
    print('mySQL表的输出数据总大小为(MB) ' + str(sizeTot))
    # the size for the memory
    sizeMemory = getMemorySize()
    #estimatethe total number for fetching data
    batchfetch = math.floor(sizeTot/sizeMemory) + 1
    numfetch   = math.floor(sizeMemory/sizeOne)
    print('mySQL表的读取轮次为 ' + str(batchfetch))
    return batchfetch, numfetch
    
    
def deliverData(db, TBNAME, ckClient, ckTBNAME):
    myCursor=db.cursor()
    # for mysql
    query3= "SELECT * from " + TBNAME
    myCursor.execute(query3)
    # for clickhouse
    sqlCK   = eval( ' """ insert into '  + ckTBNAME +' values""" ')
    # deliver the data according to batchFetch
    batchFetch, numFetch = estimateBatchFetch(myCursor, TBNAME) 
    if batchFetch == 1:
        # fetch data from mysql
        StockData = myCursor.fetchall()
        # insert data into clickhouse
        ckClient.execute(sqlCK, StockData)
    else:
        for fetchid in range(batchFetch):
            print('传输批次为 ' + str(fetchid+1))
            StockData = myCursor.fetchmany(numFetch)   
            ckClient.execute(sqlCK, StockData)    
    db.close()
