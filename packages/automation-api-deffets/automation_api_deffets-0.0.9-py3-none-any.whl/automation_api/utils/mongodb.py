
import os
from bson.json_util import dumps
import numpy as np


def convertMetaToCollection(meta):
  if not hasattr(meta, 'Modality'):
    return meta
    
  #TODO Deal with numeric values and arrays
  col = {
    "ImagePositionPatient": list(map(float, meta.ImagePositionPatient)),
    "StudyDate": str(meta.StudyDate),
    "SeriesDate": str(meta.SeriesDate) if hasattr(meta, 'SeriesDate') else "",
    "AcquisitionDate": str(meta.AcquisitionDate),
    "ContentDate": str(meta.ContentDate) if hasattr(meta, 'ContentDate') else "",
    "Manufacturer": str(meta.Manufacturer),
    "PatientName": "",
    "PatientID": meta.PatientID,
    "PatientSex": str(meta.PatientSex),
    "PatientAge": str(meta.PatientAge),
    "PatientBirthDate": str(meta.PatientBirthDate) if hasattr(meta, 'PatientBirthDate') else "",
    "PatientWeight": str(meta.PatientWeight) if hasattr(meta, 'PatientWeight') else "",
    "BodyPartExamined": str(meta.BodyPartExamined) if hasattr(meta, 'BodyPartExamined') else "",
    "SliceThickness": meta.SliceThickness,
    "ProtocolName": str(meta.ProtocolName) if hasattr(meta, 'ProtocolName') else "",
    "PatientPosition": str(meta.PatientPosition),
    "StudyInstanceUID": str(meta.StudyInstanceUID),
    "SeriesInstanceUID": str(meta.SeriesInstanceUID),
    "ImageOrientationPatient": list(map(float, meta.ImageOrientationPatient)),
    "Rows": meta.Rows,
    "Columns": meta.Columns,
    "PixelSpacing": list(map(float, meta.PixelSpacing)),
    "BitsAllocated": meta.BitsAllocated,
    "BitsStored": meta.BitsStored,
    "HighBit": meta.HighBit,
    #"SmallestImagePixelValue": meta.SmallestImagePixelValue,
    #"LargestImagePixelValue": meta.LargestImagePixelValue,
    "RescaleIntercept": str(meta.RescaleIntercept) if hasattr(meta, 'RescaleIntercept') else "",
    "RescaleSlope": str(meta.RescaleSlope) if hasattr(meta, 'RescaleSlope') else "",
    "modalities": str(meta.Modality),
    "modality": str(meta.Modality),
    "Modality": str(meta.Modality),
    "SeriesDescription": str(meta.SeriesDescription) if hasattr(meta, 'SeriesDescription') else ""
  }
  return col


def readImage(dataPath, meta, sftp=None):
  seriesId = meta["seriesId"]
  instanceId = meta["instanceId"]
  
  dirPath = os.path.join(dataPath, seriesId)
  
  if (not sftp):
    with open(os.path.join(dirPath, instanceId+'.raw'), 'rb') as outfile:
      content = outfile.read()
  else:
    fileName = os.path.join(dirPath, instanceId+'.raw')
    fileName = fileName.replace("\\", "/") # We assume that server is always UNIX
    with sftp.open(fileName, 'rb', 1000000) as outfile:
      outfile.prefetch()
      content = outfile.read()
  
  data =  np.frombuffer(content, dtype="int16")
  return data
        

def writeImage(dataPath, metaCol, image, seriesId, instanceId, sftp=None):
  dirPath = os.path.join(dataPath, seriesId)
  
  try:
    if (not sftp):
      os.mkdir(dirPath)
    else:
      sftp.mkdir(dirPath)
  except:
    None
  
  if (not sftp):
    with open(os.path.join(dirPath, instanceId+'.txt'), 'w') as outfile:
      outfile.write(dumps(metaCol))
    
    with open(os.path.join(dirPath, instanceId+'.raw'), 'wb') as outfile:
      for item in image:
        outfile.write(bytes([item]))
  else:
    fileName = os.path.join(dirPath, instanceId+'.txt')
    fileName = fileName.replace("\\", "/") # We assume that server is always UNIX
    with sftp.open(fileName, 'w', 1000000) as outfile:
      outfile.write(dumps(metaCol))
    
    fileName = os.path.join(dirPath, instanceId+'.raw')
    fileName = fileName.replace("\\", "/") # We assume that server is always UNIX
    with sftp.open(fileName, 'wb', 1000000) as outfile:
      for item in image:
        outfile.write(bytes([item]))
        
      
def writeSeg(dataPath, segCol, segData, segId):
  dirPath = os.path.join(dataPath, segId)
  
  try:  
    os.mkdir(dirPath)
  except:
    None
    
  with open(os.path.join(dirPath, "meta.txt"), 'w') as outfile:
    outfile.write(dumps(segCol))
  
  with open(os.path.join(dirPath, 'data.raw'), 'wb') as outfile:
    outfile.write(segData)

