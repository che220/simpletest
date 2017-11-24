"""
class to process raw data and generate modeling data
"""
from physician_funcs import *

# generates data and handles all data caching
class DocDataProcessor:
    # positiveClass: the physician type interested
    def __init__(self, rawDataDir, positiveClass):
        self.isDebug = (not os.environ.get('DEBUG') is None)
        self.ignoreCache = (not os.environ.get('IGNORE_CACHE') is None)
        self.ignoreInfoGainCache = (not os.environ.get('IGNORE_INFO_GAIN_CACHE') is None)
        print('debugging: {}'.format(self.isDebug))
        print('ignore cache: {}'.format(self.ignoreCache))
        print('ignore info-gain cache: {}'.format(self.ignoreInfoGainCache))

        self.rawDataDir = rawDataDir
        self.positiveClass = positiveClass.upper()

        self.modelDataDir = '{}/model_data'.format(rawDataDir)
        if not os.path.isdir(self.modelDataDir):
            os.makedirs(self.modelDataDir)
        self.procCodeFile = '{}/{}'.format(self.modelDataDir, 'procedure_codes.csv')
        self.specCodeFile = '{}/{}'.format(self.modelDataDir, 'specialty_codes.csv')
        self.modelFeatureFile = '{}/{}'.format(self.modelDataDir, 'modeling_features.csv')
        self.modelDataFile = '{}/{}'.format(self.modelDataDir, 'modeling_data.csv')
        self.unknownDocFile = '{}/{}'.format(self.modelDataDir, 'unknown_physicians.csv')

        self.procs = None
        self.specs = None
        self.modelData = None
        self.modelFeatures = None

    def getModelData(self):
        return self.modelData

    def getModelFeatures(self):
        return self.modelFeatures

    def getSpecialtyCodes(self):
        return self.specs

    def processData(self):
        if not self.ignoreCache:
            print("reading model data from cache {} ...".format(self.modelDataDir))
            self.procs = pd.read_csv(self.procCodeFile)
            self.specs = pd.read_csv(self.specCodeFile)
            self.modelData = pd.read_csv(self.modelDataFile)
            self.modelFeatures = pd.read_csv(self.modelFeatureFile)
            print('done reading data from cache')
            return

        proc = pd.read_csv('{}/procedures.csv'.format(self.rawDataDir))

        # uppercase procedures and codes to avoid typos
        proc.procedure_code = proc.procedure_code.map(lambda x: x.upper())
        proc.procedure = proc.procedure.map(lambda x: x.upper())

        # procedure codes are used in modeling. It is important to keep this mapping around.
        # this mapping will be persisted with the model
        procMapping = proc[['procedure_code', 'procedure']].drop_duplicates()
        self.procs = procMapping
        to_csv(self.procCodeFile, self.procs)

        procCodes = pd.DataFrame(proc.procedure_code.unique(), columns=['procedure'])
        procCodes.procedure = procCodes.procedure.map(lambda x: 'P'+x)
        numProcs = procCodes.shape[0]

        dd = proc.groupby(['physician_id', 'procedure_code'])[['number_of_patients']].sum().astype(float)
        dd.columns = ['patients']
        dd['physician_id'] = dd.index.get_level_values('physician_id')

        # prefix P to code to avoid codes being all digits
        dd['procedure_code'] = dd.index.get_level_values('procedure_code').map(lambda x: 'P'+x)
        print(dd.head(4))

        phys = pd.read_csv('{}/physicians.csv'.format(self.rawDataDir))
        phys.specialty = phys.specialty.map(lambda x: x.upper()) #uppercase specialty to avoid case-errors

        unknowns = phys[phys.specialty == 'UNKNOWN']
        to_csv(self.unknownDocFile, unknowns)

        phys = phys[phys.specialty != 'UNKNOWN'] # Doctors with unknown specialty will be excluded from modeling
        numPhysicians = phys.shape[0]
        numCards = phys[phys.specialty == self.positiveClass].shape[0]

        # all specialties will be assigned codes (Sxx) except self.positiveClass
        specs = pd.DataFrame(phys.specialty.unique(), columns=['specialty'])
        specs['spec_code'] = specs.index.map(lambda x: 'S'+str(x))
        specs.at[specs.specialty == self.positiveClass, 'spec_code'] = self.positiveClass
        self.specs = specs
        to_csv(self.specCodeFile, specs)

        phys = phys.merge(specs, on='specialty')
        phys = phys[['id', 'spec_code']]
        phys.columns = ['physician_id', 'spec_code']
        dd = dd.merge(phys, on='physician_id')
        print(dd.head(4))

        y = dd.pivot_table(index=['physician_id', 'spec_code'], columns='procedure_code', values='patients').fillna(0)

        # TODO: laplace proportional to totals?
        # Laplace constant can be regarded as a hyperparameter for tuning, if there are machine power
        # when laplace = 1/numProcs, 899 features are selected by info gain alone
        # when laplace = 0.00001/numProcs, 863 features are selected by info gain alone
        laplace = 0.00001/numProcs # laplace applied for minimal possibilities
        totals = proc.groupby('physician_id')[['number_of_patients']].sum().astype(float)
        totals.columns = ['total']
        totals['physician_id'] = totals.index.get_level_values('physician_id')
        totals.total += laplace * numProcs
        print(totals.head(4))

        cols = y.shape[1]
        y += laplace

        y['physician_id'] = y.index.get_level_values('physician_id')
        y['spec_code'] = y.index.get_level_values('spec_code')
        y = y.merge(totals, on='physician_id')
        y.iloc[:, 0:cols] = y.iloc[:, 0:cols].div(y.total, axis=0)

        # two classes: NOT or self.positiveClass
        y.spec_code = y.spec_code.map(lambda a: 'NOT' if a != self.positiveClass else a)

        physicians = y.physician_id
        y = y.drop(['total', 'physician_id'], axis=1)
        cols = len(y.columns)
        print(y.iloc[0:10, cols-8:cols])
        print(y.shape)

        print("Number of unknown physicians: {}".format(unknowns.shape[0]))
        print('Number of known physicians: {}'.format(numPhysicians))
        print('Number of {}: {}'.format(self.positiveClass, numCards))

        # Pick features that have enough info gains
        yCol = 'spec_code'
        labels = y[yCol]
        selector = InfoGainFeatureSelector(y, yCol, cacheDir=self.modelDataDir,
                                           isDebug=self.isDebug, ignoreCache=self.ignoreInfoGainCache)
        df = selector.selectFeatures()
        y = y[df.feature]
        print('after info-gain feature selection: {}'.format(y.shape))

        selector = CorrelationFeatureSelector(y, isDebug=self.isDebug)
        df = selector.selectFeatures(df)
        y = y[df.feature].copy()
        print('after correlation feature selection: {}'.format(y.shape))

        y['physician_id'] = physicians
        y['spec_code'] = labels

        self.modelFeatures = df
        self.modelData = y
        to_csv(self.modelFeatureFile, df)
        to_csv(self.modelDataFile, y)
