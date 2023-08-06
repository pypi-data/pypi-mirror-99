
import os
import pymongo
from automation_api.utils.dcm import CTImage, Seg, Struct
from automation_api.utils.mongodb import convertMetaToCollection, writeImage, readImage
import time
import datetime
import numpy as np
import pydicom
from ssh_pymongo import MongoSession
import pysftp
from bson.objectid import ObjectId
import hashlib
import random


class DB:
  def __init__(self, dataPath="home/ubuntu/test_data", dbName='automation', host="127.0.0.1", user=None, password=None, key=None, port=22, to_host='127.0.0.1', to_port=27017):
    if (not (host=="127.0.0.1" or host=="localhost")):
      self.session = MongoSession(host, user, password, key=key, uri=None, port=port, to_host=to_host, to_port=to_port)
      self.db = self.session.connection[dbName]
      self.sftp = pysftp.Connection(host, username=user, password=password, private_key=key)
    else:
      self.session = None
      self.sftp = None
      self.db = pymongo.MongoClient('mongodb://localhost:27017/')[dbName]
    
    self.dataPath = dataPath;
    
  def __del__(self):
    if (self.sftp):
      self.session.stop()
      self.sftp.close()
  
  
  
  def deleteWorkflow(self, workflowId):
    workflows = self.db["workflows"]
    
    workflow = workflows.remove({'workflowId': str(workflowId)})
  
  
  def deleteWorkflowEntry(self, entryId):
    workflows = self.db["workflows"]
    
    workflow = workflows.removeOne({'_id': ObjectId(entryId)})
  
  
  def getRT(self, segId):
    data = self.db["data"]
    
    seg = data.find_one({'_id': ObjectId(segId)}, {"_id": 0})
    
    return seg
    
    
  def getSeries(self, seriesId):
    data = self.db["data"]
    
    seriesEntries = list(data.find({'seriesId': str(seriesId)}, {"_id": 0}).sort("sliceNb"))
    
    npImages = []
    
    for i, meta in enumerate(seriesEntries):
      print("Import slice " + str(i+1) + "/" + str(len(seriesEntries)))
      
      sliceData = readImage(seriesEntries[0]["dataPath"], meta, sftp=self.sftp)
      npImages.append(sliceData)
      
      sliceData.reshape((seriesEntries[0]["Rows"], seriesEntries[0]["Columns"]))
    
    data = np.dstack(npImages).astype("float32")
    
    return {"meta": seriesEntries, "data": data}
  
  
  def getUsers(self):
    mycol = self.db["users"]
    
    users = mycol.find().sort("username")
    
    return list(users)
    

  def getUserNames(self):
    users = self.getUsers()
    
    userNames = []
    for user in users:
      userNames.append(str(user['username']))

    return userNames
    
  
  def getWorkflow(self, workflowId):
    workflows = self.db["workflows"]
    
    workflow = workflows.find({"workflowId": str(workflowId)})
      
    return list(workflow)
  
  
  def getWorkflowEntry(self, entryId):
    workflows = self.db["workflows"]
    
    workflow = workflows.find_one({'_id': ObjectId(entryId)}, {"_id": 0})

    return workflow

  
  def insertData(self, seriesMeta, seriesData=None):
    data = self.db["data"]
    
    ctCols = None
    
    if (seriesData is None):
      ctCols = convertMetaToCollection(seriesMeta)
      
      if "_id" in ctCols:
        del ctCols["_id"]
        
      dataId = data.insert(ctCols)
    else:
      seriesId = None
      
      # TODO Use reshape instead of a loop
      ct = []
      for i in range(seriesData.shape[-1]):
        newData = seriesData[:, :, i].flatten()
        if (i==0):
          ct = newData
        else:
          ct = np.concatenate((ct, newData))
      
      ct = ct.astype(np.int16).tobytes()
        
      ctCols = []
      for i, meta in enumerate(seriesMeta):
        print("Import slice " + str(i+1) + "/" + str(len(seriesMeta)))

        ctCol = convertMetaToCollection(meta)
        ctCol["dataPath"] = self.dataPath
        
        if "_id" in ctCol:
          del ctCol["_id"]
        
        ctCols.append(ctCol)
        instanceId = data.insert(ctCol)
        
        stride = ctCol["Rows"]*ctCol["Columns"]*2;
        
        if (i==0):
          seriesId = instanceId
          myquery = { "_id": seriesId }
          
        newvalues = { "$set": { "seriesId": str(seriesId), "instanceId": str(instanceId), "sliceNb": i } }
        data.update_one({"_id": instanceId}, newvalues)
        
        writeImage(self.dataPath, ctCol, ct[i*stride:(i+1)*stride], str(seriesId), str(instanceId), sftp=self.sftp)
        
        dataId = seriesId
     
    return {"id": str(dataId), "meta": ctCols}
  
  
  def insertDcmStruct(self, structFileName, ctMeta):
    data = self.db["data"]
    
    segImage = Struct()
    
    #TODO Ideally, we should change RTReferencedSeriesSequence.SeriesInstanceUID, etc. with the correct id in the DB... In the meantime provide all the necessary metaData...
    segImage.loadStruct(structFileName, ctMeta)
    
    segCol = segImage.getMeta()
    
    segId = self.insertData(segCol)["id"]
    
    return {"id": str(segId), "meta": segCol}
    
  
  # Only one dcm file per series. ctList can contain several series
  def insertDcmSeries(self, ctList):
    if not isinstance(ctList, list):
      ctList = [ctList]
    
    data = self.db["data"]
    
    seriesIds = []
    ctMetas = []
    cts = []
    
    for _, ctFileName in enumerate(ctList):
      print("Import series " + str(ctFileName))
      
      ctImage = CTImage()
      ctImage.loadCT(ctFileName)
      
      ctMeta = ctImage.getMeta()
      
      ct = ctImage.getNpImage()
      cts.append(ct)
      
      res = self.insertData(ctMeta, ct)
      seriesIds.append(res["id"])
      ctMetas.append(res["meta"])
        
    return {"id": seriesIds, "meta": ctMetas, "data": cts}
  
  
  def insertUser(self, username, pwd, role):
    salt = str(random.getrandbits(128))
    
    hash = hashlib.pbkdf2_hmac('sha512', pwd.encode(), salt.encode(), 1000).hex()
  
    users = self.db["users"]
    users.insert({
      "username": username,
      "salt": salt,
      "hash": hash,
      "role": role
    })
  
  
  def insertWorkflowEntry(self, seriesId, segId, users, meta, info, parents, label):
    if(not seriesId):
      seriesId = []
    if(not segId):
      segId = ""
    if(not users):
      users = []
    if(not parents):
      parents = []
      
    #TODO: convert parents, seriesId, and segId to Strings if they are ObjectIds
    
    workflows = self.db["workflows"]
    
    ts = time.time()
    isodate = datetime.datetime.fromtimestamp(ts, None)
    
    if isinstance(meta, dict) and not isinstance(meta["PatientID"], pydicom.DataElement):
      col = {
        "parents": parents,
        "date": isodate,
        "users": users,
        "seriesId": seriesId,
        "segId": segId,
        "PatientName": str(meta["PatientName"]),
        "PatientID": meta["PatientID"],
        "PatientSex": str(meta["PatientSex"]),
        "PatientAge": str(meta["PatientAge"]),
        "PatientWeight": str(meta["PatientWeight"]),
        "BodyPartExamined": str(meta["BodyPartExamined"]),
        "info": str(info),
        "label": label
      }
    else:
      col = {
        "parents": parents,
        "date": isodate,
        "users": users,
        "seriesId": seriesId,
        "segId": segId,
        "PatientName": str(meta.PatientName),
        "PatientID": meta.PatientID,
        "PatientSex": str(meta.PatientSex),
        "PatientAge": str(meta.PatientAge),
        "PatientWeight": str(meta.BodyPartExamined) if hasattr(meta, 'PatientWeight') else "",
        "BodyPartExamined": str(meta.BodyPartExamined) if hasattr(meta, 'BodyPartExamined') else "",
        "info": str(info),
        "label": label
      }    
    
    entryId = workflows.insert(col)
    
    if (not len(parents)):
      workflowId = str(entryId)
    else:
      parentEntry = self.getWorkflowEntry(parents[0])
      workflowId = parentEntry["workflowId"]
    
    workflows.update_one({"_id": entryId}, {"$set": {"workflowId": workflowId}})
    
    return str(entryId)

