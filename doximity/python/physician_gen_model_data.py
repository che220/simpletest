"""
generate modeling data
"""
import sys
from physician_data import *

pd.set_option('display.width', 5000)
pd.set_option('max_columns', 600)

def usage():
    print('usage: python {} <data directory> <physician type>'.format(sys.argv[0]))
    sys.exit(1)

if len(sys.argv) < 3:
    usage()

dataDir = sys.argv[1]
docType = sys.argv[2]

dataProcessor = DocDataProcessor(dataDir, docType)
dataProcessor.processData()

modelData = dataProcessor.getModelData()
print("Modeling Data:")
print(modelData.shape)
print(modelData.columns)

specs = dataProcessor.getSpecialtyCodes()
print("Specialty Codes:")
print(specs.head(10))
print(specs.shape)

features = dataProcessor.getModelFeatures()
print("Model Features:")
print(features.head(10))
print(features.shape)
