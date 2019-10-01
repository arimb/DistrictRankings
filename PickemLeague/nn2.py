import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot
from math import sqrt
import tensorflow as tf
from operator import add

with open('competitors.pkl', 'rb') as file:
    data = pickle.load(file)
    X = MinMaxScaler().fit_transform(np.array([c[0][1:] for c in data]))
    y = np.divide(np.array([c[1:4] for c in data]), [22,16,30])

with open('cc.pkl', 'rb') as file:
    data = pickle.load(file)
    cc_teams = [c[0] for c in data]
    cc_X = MinMaxScaler().fit_transform(np.array([c[1][0][1:] for c in data]))
    cc_y = np.array([c[1][1:4] for c in data]), [22,16,30]

# X = np.array([[24.4708494,22.80238239,35.22319231],
#               [22.77617165,14.77373296,0],
#               [19.69831061,14.15816075,6.155722067],
#               [12.92701634,4.309005447,0],
#               [24.56354201,14.92351043,4.634630568]])
# y = np.array([[17,15,0],
#               [14,3,20],
#               [21,15,0],
#               [20,14,20],
#               [22,16,5]])

model = Sequential()
model.add(Dense(3, input_dim=3))
model.compile(loss='mse', optimizer='adam', metrics=['mse'])
model.fit(X, y, epochs=150, batch_size=50, verbose=2)
weights = model.layers[0].get_weights()[0]

model.save('model.h5')

# model.evaluate(cc_X, cc_y)
predictions = [sum(x) for x in np.multiply(model.predict(cc_X), [22,16,30])]
# print(predictions)
# rmse = [0,0,0]
# for pred,act in zip(predictions,cc_y):
#     rmse = [x+(y**2) for x,y in zip(rmse,[p-a for p,a in zip(pred,act)])]
# print("RMSE: " + str([sqrt(x) for x in rmse]))

with open('cc_prediction.csv', 'w+') as file:
    file.write('Team,Pred\n')
    for t,p in zip(cc_teams,predictions):
        file.write('{0},{1}\n'.format(t,p))
