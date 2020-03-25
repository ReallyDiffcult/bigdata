
# coding: utf-8

# In[3]:


# get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt
from gaft.operators.mutation import flip_bit_mutation
from scipy import stats
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import seaborn as sns;sns.set()
import sklearn
import random
import math
from sklearn import svm
from sklearn.decomposition import KernelPCA
import gaft
from gaft import GAEngine
# from gaft.components import BinaryIndividual
# from gaft.components import Population
from gaft.components import BinaryIndividual
# from gaft.components import GAIndividual
from gaft.components import Population
from gaft.operators import RouletteWheelSelection
from gaft.operators import UniformCrossover
from gaft.operators import FlipBitMutation
from gaft.operators.mutation.flip_bit_mutation import FlipBitBigMutation
from gaft.analysis.fitness_store import FitnessStore
from gaft.plugin_interfaces.analysis import OnTheFlyAnalysis
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
import math
from sklearn.preprocessing import OneHotEncoder
#from gaft-master\gaft\operators\mutation\flip_bit_mutation import FlipBitMutation
# import gaft-master
# In[ ]:

def read_flile():

    js = pd.read_excel('train-l.xlsx')
    test = pd.read_excel('test1.xlsx')


    # In[ ]:


    js.head()


    # In[ ]:


    col = js.columns.values.tolist()
    col1 = col[2:-1]
    data_x = np.array(js[col1])
    data_y = js['label']
    colt = js.columns.values.tolist()
    col2 = colt[2:-1]
    test_x = np.array(test[col2])
    test_y = test['label']
    return data_x,data_y,test_x,test_y,js,test

def preprocess_data():
    data_x, data_y, test_x, test_y,js,test = read_flile()
    button_mapping = {
        'NoButton': 1,
        'Left': 2,
        'Scroll': 3,
        'Right': 4}
    js['button'] = js['button'].map(button_mapping)

    test['button'] = test['button'].map(button_mapping)

    # In[ ]:

    state_mapping = {
        'Move': 5,
        'Pressed': 6,
        'Released': 7,
        'Down': 8,
        'Drag': 9,
        'Up': 10
    }
    js['state'] = js['state'].map(state_mapping)
    test['state'] = test['state'].map(state_mapping)

    # In[ ]:

    data_x = js[['record timestamp', 'client timestamp', 'button', 'state', 'x', 'y']].values
    le = LabelEncoder()
    data_x[:, 0] = le.fit_transform(data_x[:, 0])
    data_x
    data_y = js['label']

    test_x = test[['record timestamp', 'client timestamp', 'button', 'state', 'x', 'y']].values
    le = LabelEncoder()
    test_x[:, 0] = le.fit_transform(test_x[:, 0])
    test_x
    test_y = test['label']

    # In[ ]:


    mms = MinMaxScaler()
    data_x = mms.fit_transform(data_x)
    test_x = mms.fit_transform(test_x)

    # In[ ]:

    scaler =  sklearn.preprocessing.StandardScaler().fit(data_x)
    scaler.transform(data_x)
    scaler2 = sklearn.preprocessing.StandardScaler().fit(test_x)
    scaler2.transform(test_x)
    return  data_x, data_y, test_x, test_y
def preprocess_pca():
    data_x, data_y, test_x, test_y = preprocess_data()

    kpca = KernelPCA(kernel="rbf", n_components=4)
    # data_x = kpca.fit_transform(data_x)
    test_x = kpca.fit_transform(test_x)
    print(test_x[0:6])
    return test_x,test_y

def msefunc(predictval,realval):
    squaredError = []
    absError = []
    for i in range(len(predictval)):
        val=predictval[i-1]-realval[i-1]
        squaredError.append(val * val)  # target-prediction之差平方
        print("Square Error: ", squaredError)
        print("MSE = ", sum(squaredError) / len(squaredError))  # 均方误差MSE
        return sum(squaredError) / len(squaredError)
#
# def fitness(indv):
#
#     return msefunc(predictval,reaval)

#@engine.analysis_register
class ConsoleOutput(OnTheFlyAnalysis):
    master_only = True
    interval = 1
    def register_step(self, g, population, engine):
        best_indv = population.best_indv(engine.fitness)
        msg = 'Generation: {}, best fitness: {:.3f}'.format(g, engine.fmax)
        engine.logger.info(msg)
def tain_svm():
    indv_template = BinaryIndividual(ranges=[(-8, 8), (-8, 8), (-8, 8)], eps=[0.001, 0.001, 0.001])
    population = Population(indv_template=indv_template, size=1000)
    population.init()  # Initialize population with individuals.

    # In[ ]:

    selection = RouletteWheelSelection()
    crossover = UniformCrossover(pc=0.8, pe=0.5)
    # mutation = FlipBitMutation(pm=0.1)
    mutation = FlipBitBigMutation(pm=0.1, pbm=0.55, alpha=0.6)

    engine = GAEngine(population=population, selection=selection,
                      crossover=crossover, mutation=mutation,
                      analysis=[ConsoleOutput, FitnessStore])
    #############################################################
    indv=engine.population.best_indv(engine.fitness).variants
    c, e, g = indv.variants[1], indv.variants[2], indv.variants[-1]
    clf = svm.svR(C=c, epsilon=e, gamma=g, kernel='rbf')

    data_x, data_y = preprocess_pca()
    clf.fit(data_x, data_y)
    predictval = clf.predict(data_x)
    reaval = data_y
    print(predictval)

    # In[ ]:

    engine.run(ng=100)






    ##############################################################################
    #####################
    # c,e,g = indv_template.variants[1],indv_template.variants[2],indv_template.variants[-1]
    # clf = svm.svR(C=c,epsilon=e,gamma=g,kernel='rbf')
    #
    # data_x,data_y = preprocess_pca()
    # clf.fit(data_x,data_y)
    # predictval = clf.predict(data_x)
    # reaval = data_y
    # print(predictval)
    #
    # # In[ ]:
    #
    #
    # engine.run(ng=100)


if __name__ == '__main__':
    preprocess_pca()
    tain_svm()

# # In[ ]:
#
#

#
#
# # In[ ]:
#
#

# # In[ ]:
#
#

#
#
# # In[ ]:
#
#

#
#
# # In[ ]:
#
#

#
#
# # In[ ]:
#
#
#@engine.fitness_register


#
#
# # In[ ]:
#
#

#
#
# # In[ ]:
#
#
# if '__main__' == __name__:
#     engine.run(ng=100)
#
#
# # In[ ]:
#
#
# from sklearn import neighbors
# clf2=neighbors.KNeighborsClassifier(n_neighbors,weights=weights,n_classes=2)
# cif2.fit(data_x,data_y)
#
#
# # In[ ]:
#
#
# from itertools import product
# from sklearn.ensemble import VotingClassifier
#
#
# # In[ ]:
#
#
# # eclf = VotingClassifier(estimators=[('svc',clf1),('knn',clf2),voting='soft',weights=[2,1]])
# eclf = VotingClassifier(estimators=[('svc',clf1),('knn',clf2)])
# x_min, x_max = X[:,0].min() -1, X[:,0].max() + 1
# y_min, y_max = X[:,1].min() -1, X[:,1].max() + 1
# xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01), np.arange(y_min, y_max, 0.01))
# fig, axes = plt.subplots(2, 2, sharex='col', sharey='row', figsize=(10, 8))
# for idx, clf, title in zip(product([0, 1],[0, 1]),
#                            [clf1, clf2, eclf],
#                            [ 'KNN ','Kernel SVM', 'Soft Voting']):
#     Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
#     Z = Z.reshape(xx.shape)
#     axes[idx[0], idx[1]].contourf(xx, yy, Z, alpha=0.4)
#     axes[idx[0], idx[1]].scatter(X[:, 0],X[:, 1], c=y, s=20, edgecolor='k')
#     axes[idx[0], idx[1]].set_title(title)
# plt.show()
#
