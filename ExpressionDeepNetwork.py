import theano
from theano import tensor as T
from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams
import numpy as np
from load import faces
from theano.tensor.nnet.conv import conv2d
from theano.tensor.signal.downsample import max_pool_2d

srng = RandomStreams()

f = open('Tainlog.log', 'a')
f.write("Neural Net Train results")

def floatX(X):
    return np.asarray(X, dtype=theano.config.floatX)

def init_weights(shape):
    return theano.shared(floatX(np.random.randn(*shape) * 0.01) , borrow=True )

def init_biases(shape):
    return theano.shared(floatX(np.random.randn(*shape) * 0.01) , borrow=True )

def rectify(X):
    return T.maximum(X, 0.)

def softmax(X):
    e_x = T.exp(X - X.max(axis=1).dimshuffle(0, 'x'))
    return e_x / e_x.sum(axis=1).dimshuffle(0, 'x')

def dropout(X, p=0.):
    if p > 0:
        retain_prob = 1 - p
        X = X * srng.binomial(X.shape, p=retain_prob, dtype=theano.config.floatX)
        X = (X/retain_prob)
    return X

def RMSprop(cost, params, lr=0.001, rho=0.9, epsilon=1e-6):
    grads = T.grad(cost=cost, wrt=params)
    updates = []
    for p, g in zip(params, grads):
        acc = theano.shared(p.get_value() * 0.)
        acc_new = rho * acc + (1 - rho) * g ** 2
        gradient_scaling = T.sqrt(acc_new + epsilon)
        g = g / gradient_scaling
        updates.append((acc, acc_new))
        updates.append((p, p - lr * g))
    return updates


def model(X, w1, w2, w3, w4, w5, b5 , w6 ,b6 , w_o, p_drop_conv, p_drop_hidden):
    
    l1 = rectify(conv2d(X, w1, border_mode='full'))

    l2a = rectify(conv2d(l1, w2))
    l2 = max_pool_2d(l2a, (2, 2))
    l2 = dropout(l2, p_drop_conv)
    
    l3a = rectify(conv2d(l2, w3))
    l3 = max_pool_2d(l3a, (2, 2))
    
    l4a = rectify(conv2d(l3,w4))
    l4 = max_pool_2d(l4a, (2, 2))
    l4 = dropout(l4, p_drop_conv)
    
    l5a = T.flatten(l4, outdim=2)
    l5b = T.dot(l5a, w5) + b5
    l5 = rectify(l5b)
    
    l6a = T.dot(l5, w6) + b6
    l6 = rectify(l6a)

    pyx = softmax(T.dot(l6, w_o))
    
    return l1, l2, l3, l4, l5, l6, pyx


trX, teX, trY, teY = faces()
trX = trX.reshape(-1, 1, 48, 48)
teX = teX.reshape(-1, 1, 48, 48)


#initialize All the parameters
X = T.ftensor4()
Y = T.fmatrix()
w1 = init_weights((32, 1, 11, 11))

w2 = init_weights((64, 32, 7, 7))

w3 = init_weights((128, 64, 5, 5))

w4 = init_weights((128, 128, 3, 3))

w5 = init_weights((128 * 5 * 5 , 100))
b5 = init_biases((10,100))

w6 = init_weights((100 , 100))
b6 = init_biases((10,100))

w_o = init_weights((100, 7))

#Train Loop
noise_l1, noise_l2, noise_l3, noise_l4, noise_l5, noise_l6, noise_py_x = model(X, w1, w2, w3, w4, w5, b5, w6, b6, w_o, 0.2, 0.5)
cost = T.mean(T.nnet.categorical_crossentropy(noise_py_x, Y))
params = [w1, w2, w3, w4, w5 ,b5 ,w6 , b6, w_o]
updates = RMSprop(cost, params, lr=0.009)
train = theano.function(inputs=[X, Y], outputs=cost, updates=updates, allow_input_downcast=True)

#Predict Loop
l1, l2, l3, l4, l5, l6 , py_x = model(X, w1, w2, w3, w4, w5, b5, w6, b6, w_o, 0., 0.)
y_x = T.argmax(py_x, axis=1)
predict = theano.function(inputs=[X], outputs=y_x, allow_input_downcast=True)


for i in range(2870):
    for start, end in zip(range(10*i, len(trX),10), range(10*i+10, len(trX),10)):
        cost = train(trX[start:end], trY[start:end])
    logline = "Interation number: " + str(i) + ", Cost value : " + str(cost)
    print "Interation number: " + str(i)
    print "Cost value : " + str(cost)
    f.write(logline)

for start, end in zip(range(0, len(teX),10), range(10, len(teX),10)):
    error = np.mean(np.argmax(teY[start:end], axis=1) == predict(teX[start:end]))
    logline = "Error = " + str(error)
    print error
    f.write(logline)
    
   
