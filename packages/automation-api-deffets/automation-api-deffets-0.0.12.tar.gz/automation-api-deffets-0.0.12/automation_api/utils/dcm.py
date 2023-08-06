import os
import pydicom
import numpy as np
from PIL import Image, ImageDraw

class CTImage:
  def __init__(self):
    self.seriesInstanceUID = ""
    self.dcmPath = ""
    self.isLoaded = False
    self.npImages = None
    self.image = None
    self.dcmObjects = []
    
  def loadCT(self, dcmFileName):
    if(self.isLoaded and self.dcmPath==dcmPath):
      return
  
    dcmPath = os.path.dirname(dcmFileName) 
    dcmFiles = getDicomList(dcmFileName)
    
    npImages = []
    images = []
    SOPInstanceUIDs = []
    SliceLocation = np.zeros(len(dcmFiles), dtype='float')
    
    for i, dcmFile in enumerate(dcmFiles):
      dcm = pydicom.dcmread(dcmFile)
      
      try:
        SliceLocation[i] = int(dcm.InstanceNumber)
        SOPInstanceUIDs.append(dcm.SOPInstanceUID)
      except:
        continue
    
    sort_index = np.argsort(SliceLocation)

    ind1 = 0
    for i in sort_index:
      dcm = pydicom.dcmread(dcmFiles[i])
      
      try:
        SliceLocation[ind1] = int(dcm.InstanceNumber)
      except:
        continue
      
      images += dcm.PixelData
      npImages.append(dcm.pixel_array)
      
      SOPInstanceUIDs[ind1] = dcm.SOPInstanceUID
      
      self.dcmObjects.append(dcm)
      
      ind1 += 1
    
    self.image = images
    self.npImage = np.dstack(npImages).astype("float32")
    self.isLoaded = True
  
  def getMeta(self):
    return self.dcmObjects
  
  def getImage(self):
    return self.image
    
  def getNpImage(self):
    return self.npImage
 
class Seg:
  def __init__(self):
    self.isLoaded = False
    self.meta = None
    self.data = None

  def loadSeg(self, fileName, seriesMeta):
    self.isLoaded = False
    
    meta = pydicom.dcmread(fileName)
    
    ImagePositionPatient = list(map(float, seriesMeta[0].ImagePositionPatient))
    PixelSpacing = list(map(float, seriesMeta[0].PixelSpacing))
    SliceThickness = seriesMeta[0].SliceThickness
    Rows = seriesMeta[0].Rows
    Columns = seriesMeta[0].Columns
    Slices = len(seriesMeta)
    
    SegmentSequence = []
    for i, contour in enumerate(meta.ROIContourSequence):
      segItem = {
        "SegmentNumber": meta.StructureSetROISequence[i].ROINumber,
        "SegmentDescription": meta.StructureSetROISequence[i].ROIName,
        "RecommendedDisplayCIELabValue": list(map(float, meta.ROIContourSequence[i].ROIDisplayColor)),
      }
      
      SegmentSequence.append(segItem)
      
      zStride = Rows*Columns
      newContour = np.zeros(Rows*Columns*Slices, dtype="uint8")
      
      for j, contourSequenceItem in enumerate(contour.ContourSequence):
        print("Import contour slice " + str(j+1) + "/" + str(len(contour.ContourSequence)) + " of contour  " + str(i+1) + "/" + str(len(meta.ROIContourSequence)))
        Slice = {}
        
        # list of Dicom coordinates
        posX = np.array(contourSequenceItem.ContourData[0::3])
        posY = np.array(contourSequenceItem.ContourData[1::3])
        posZ = np.array(contourSequenceItem.ContourData[2])
        
        # list of coordinates in the image frame
        pointsIndexes = list(zip( (posX-ImagePositionPatient[0])/PixelSpacing[0], (posY-ImagePositionPatient[1])/PixelSpacing[1] ))
        indexZ = int(round((ImagePositionPatient[2]-posZ)/SliceThickness))
        
        # convert polygon to mask
        try:
          img = Image.new('L', (Rows, Columns), 0)
          ImageDraw.Draw(img).polygon(pointsIndexes, outline=1, fill=1)
          mask = np.array(img, dtype="uint8")
        
          newContour[indexZ*zStride : (indexZ+1)*zStride] = mask.flatten()
        except:
          None
      
      if (i==0):
        uint8Contour = np.packbits(newContour)
      else:
        uint8Contour = np.concatenate((uint8Contour, np.packbits(newContour)))
        
    self.meta = {
      "modalities": str("SEG"),
      "modality": str("SEG"),
      "Modality": str("SEG"),
      "StudyDate": str(meta.StudyDate),
      "SeriesDate": str(meta.SeriesDate) if hasattr(meta, 'SeriesDate') else "",
      "Manufacturer": str(meta.Manufacturer),
      "PatientName": str(meta.PatientName),
      "PatientID": meta.PatientID,
      "BodyPartExamined": str(meta.BodyPartExamined) if hasattr(meta, 'BodyPartExamined') else "",
      "SharedFunctionalGroupsSequence": {
        "PlaneOrientationSequence": {
          "ImageOrientationPatient": list(map(float, seriesMeta[0].ImageOrientationPatient)),
          },
        "PixelMeasuresSequence": {
          "SliceThickness": SliceThickness,
          "SpacingBetweenSlices": SliceThickness,
          "PixelSpacing": PixelSpacing,
        }
      },
      "StudyInstanceUID": str(meta.StudyInstanceUID),
      "SeriesInstanceUID": str(meta.SeriesInstanceUID),
      "Rows": Rows,
      "Columns": Columns,
      "SegmentSequence": SegmentSequence,
      "ImagePositionPatient": list(map(float, ImagePositionPatient)) #This is non standard
    }
    
    self.data = uint8Contour
    self.isLoaded = True
    
  def getMeta(self):
    return self.meta
    
  def getData(self):
    return self.data
    

class Struct:
  def __init__(self):
    self.isLoaded = False
    self.meta = None

  def loadStruct(self, fileName, seriesMeta):
    self.isLoaded = False
    
    meta = pydicom.dcmread(fileName)
    
    if isinstance(seriesMeta[0], dict) and not isinstance(seriesMeta[0]["Rows"], pydicom.DataElement):
      ImagePositionPatient = list(map(float, seriesMeta[0]["ImagePositionPatient"]))
      PixelSpacing = list(map(float, seriesMeta[0]["PixelSpacing"]))
      SliceThickness = seriesMeta[0]["SliceThickness"]
      Rows = seriesMeta[0]["Rows"]
      Columns = seriesMeta[0]["Columns"]
      Slices = len(seriesMeta)
      ImageOrientationPatient = list(map(float, seriesMeta[0]["ImageOrientationPatient"]))
      StudyDate = str(meta["StudyDate"])
      SeriesDate = str(meta["SeriesDate"])
      Manufacturer = str(meta["Manufacturer"])
      PatientID = str(meta["PatientID"])
      StudyInstanceUID = str(meta["StudyInstanceUID"])
      SeriesInstanceUID = str(meta["SeriesInstanceUID"])
    else:
      ImagePositionPatient = list(map(float, seriesMeta[0].ImagePositionPatient))
      PixelSpacing = list(map(float, seriesMeta[0].PixelSpacing))
      SliceThickness = seriesMeta[0].SliceThickness
      Rows = seriesMeta[0].Rows
      Columns = seriesMeta[0].Columns
      Slices = len(seriesMeta)
      ImageOrientationPatient = list(map(float, seriesMeta[0].ImageOrientationPatient))
      StudyDate = str(meta.StudyDate)
      SeriesDate = str(meta.SeriesDate) if hasattr(meta, 'SeriesDate') else "",
      Manufacturer = str(meta.Manufacturer)
      PatientID = meta.PatientID
      StudyInstanceUID = str(meta.StudyInstanceUID)
      SeriesInstanceUID = str(meta.SeriesInstanceUID)
    
    ROIContourSequence = []
    StructureSetROISequence = []
    for i, contour in enumerate(meta.ROIContourSequence):
      StructureSetROISequence.append( {
        "ROINumber": str(meta.StructureSetROISequence[i].ROINumber),
        "ROIName": str(meta.StructureSetROISequence[i].ROIName)
      })
      
      contourSequence = []
      for j, contourItem in enumerate(contour.ContourSequence):
        contourSequenceItem = {
          "NumberOfContourPoints": contourItem.NumberOfContourPoints,
          "ContourData": list(map(float, contourItem.ContourData))
        }
      
        contourSequence.append(contourSequenceItem)
      
      roiConstourSequenceItem = {
        "ROIDisplayColor": list(map(float, contour.ROIDisplayColor)),
        "ContourSequence": contourSequence
      }
      
      ROIContourSequence.append(roiConstourSequenceItem)
        
    self.meta = {
      "modalities": str("RTSTRUCT"),
      "modality": str("RTSTRUCT"),
      "Modality": str("RTSTRUCT"),
      "StudyDate": StudyDate,
      "SeriesDate": SeriesDate,
      "Manufacturer": Manufacturer,
      "PatientName": "",
      "PatientID": PatientID,
      "BodyPartExamined": "",
      "StudyInstanceUID": StudyInstanceUID,
      "SeriesInstanceUID": SeriesInstanceUID,
      "StructureSetROISequence" : StructureSetROISequence,
      "ROIContourSequence": ROIContourSequence,
      "SeriesDescription": "",
      "Rows": Rows, #This is non standard
      "Columns": Columns, #This is non standard
      "Slices": Slices, #This is non standard
      "SliceThickness": SliceThickness, #This is non standard
      "PixelSpacing": PixelSpacing, #This is non standard
      "ImagePositionPatient": ImagePositionPatient, #This is non standard
      "ImageOrientationPatient": ImageOrientationPatient #This is non standard
    }
    
    self.isLoaded = True
    
  def getMeta(self):
    return self.meta
    

def getDicomList(fileName):
  try:
    dcm = pydicom.dcmread(fileName)
    seriesInstanceUID = dcm.SeriesInstanceUID
  except:
    print("Invalid Dicom file: " + fileName)
    return []
  
  
  folderPath = os.path.dirname(fileName)
  fileList = os.listdir(folderPath)
  
  dcmList = []
  for name in fileList:
    try:
      dcm = pydicom.dcmread(os.path.join(folderPath, name))
      sUID = dcm.SeriesInstanceUID
      
      if (sUID==seriesInstanceUID):
        dcmList.append(os.path.join(folderPath, name))
    except:
      None
  
  return dcmList
  
