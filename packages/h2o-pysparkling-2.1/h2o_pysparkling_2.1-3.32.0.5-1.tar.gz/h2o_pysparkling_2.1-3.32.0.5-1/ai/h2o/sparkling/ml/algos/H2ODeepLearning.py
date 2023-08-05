#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from warnings import warn
from pyspark import keyword_only
from ai.h2o.sparkling import Initializer
from ai.h2o.sparkling.ml.Utils import Utils
from ai.h2o.sparkling.ml.algos.H2OSupervisedAlgorithm import H2OSupervisedAlgorithm
from ai.h2o.sparkling.ml.models.H2ODeepLearningMOJOModel import H2ODeepLearningMOJOModel
from ai.h2o.sparkling.ml.params.H2ODeepLearningParams import H2ODeepLearningParams
from ai.h2o.sparkling.ml.params.H2OCommonParams import H2OCommonParams
from ai.h2o.sparkling.ml.algos.DistributionBasedH2OTrainFramePreparation import DistributionBasedH2OTrainFramePreparation


class H2ODeepLearning(H2ODeepLearningParams, H2OCommonParams, H2OSupervisedAlgorithm, DistributionBasedH2OTrainFramePreparation):

    @keyword_only
    def __init__(self,
                 initialBiases=None,
                 initialWeights=None,
                 ignoredCols=None,
                 columnsToCategorical=[],
                 withContributions=False,
                 withLeafNodeAssignments=False,
                 namedMojoOutputColumns=True,
                 convertInvalidNumbersToNa=False,
                 detailedPredictionCol="detailed_prediction",
                 validationDataFrame=None,
                 featuresCols=[],
                 predictionCol="prediction",
                 convertUnknownCategoricalLevelsToNa=False,
                 splitRatio=1.0,
                 withStageResults=False,
                 withDetailedPredictionCol=True,
                 balanceClasses=False,
                 classSamplingFactors=None,
                 maxAfterBalanceSize=5.0,
                 activation="Rectifier",
                 hidden=[200, 200],
                 epochs=10.0,
                 trainSamplesPerIteration=-2,
                 targetRatioCommToComp=0.05,
                 seed=-1,
                 adaptiveRate=True,
                 rho=0.99,
                 epsilon=1.0E-8,
                 rate=0.005,
                 rateAnnealing=1.0E-6,
                 rateDecay=1.0,
                 momentumStart=0.0,
                 momentumRamp=1000000.0,
                 momentumStable=0.0,
                 nesterovAcceleratedGradient=True,
                 inputDropoutRatio=0.0,
                 hiddenDropoutRatios=None,
                 l1=0.0,
                 l2=0.0,
                 maxW2=3.402823E38,
                 initialWeightDistribution="UniformAdaptive",
                 initialWeightScale=1.0,
                 loss="Automatic",
                 scoreInterval=5.0,
                 scoreTrainingSamples=10000,
                 scoreValidationSamples=0,
                 scoreDutyCycle=0.1,
                 classificationStop=0.0,
                 regressionStop=1.0E-6,
                 quietMode=False,
                 scoreValidationSampling="Uniform",
                 overwriteWithBestModel=True,
                 autoencoder=False,
                 useAllFactorLevels=True,
                 standardize=True,
                 diagnostics=True,
                 variableImportances=True,
                 fastMode=True,
                 forceLoadBalance=True,
                 replicateTrainingData=True,
                 singleNodeMode=False,
                 shuffleTrainingData=False,
                 missingValuesHandling="MeanImputation",
                 sparse=False,
                 averageActivation=0.0,
                 sparsityBeta=0.0,
                 maxCategoricalFeatures=2147483647,
                 reproducible=False,
                 exportWeightsAndBiases=False,
                 miniBatchSize=1,
                 elasticAveraging=False,
                 elasticAveragingMovingRate=0.9,
                 elasticAveragingRegularization=0.001,
                 modelId=None,
                 nfolds=0,
                 keepCrossValidationModels=True,
                 keepCrossValidationPredictions=False,
                 keepCrossValidationFoldAssignment=False,
                 distribution="AUTO",
                 tweediePower=1.5,
                 quantileAlpha=0.5,
                 huberAlpha=0.9,
                 labelCol="label",
                 weightCol=None,
                 offsetCol=None,
                 foldCol=None,
                 foldAssignment="AUTO",
                 categoricalEncoding="AUTO",
                 ignoreConstCols=True,
                 scoreEachIteration=False,
                 stoppingRounds=5,
                 maxRuntimeSecs=0.0,
                 stoppingMetric="AUTO",
                 stoppingTolerance=0.0,
                 exportCheckpointsDir=None,
                 aucType="AUTO"):
        Initializer.load_sparkling_jar()
        super(H2ODeepLearning, self).__init__()
        self._java_obj = self._new_java_obj("ai.h2o.sparkling.ml.algos.H2ODeepLearning", self.uid)
        self._setDefaultValuesFromJava()
        kwargs = Utils.getInputKwargs(self)

        if 'interactionPairs' in kwargs:
            warn("Interaction pairs are not supported!")
        self._set(**kwargs)
        self._transfer_params_to_java()

    def _create_model(self, javaModel):
        return H2ODeepLearningMOJOModel(javaModel)
