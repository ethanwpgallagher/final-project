import tensorflow as tf
import keras

def res_net():
  resnet = keras.applications.resnet50.ResNet50(include_top=False)
  x = resnet.output
  x = keras.layers.GlobalAveragePooling2D()(x)
  x = keras.layers.Dense(1024, activation='relu')(x)
  predictions = keras.layers.Dense(5, activation='softmax')(x)
  model = keras.Model(inputs=resnet.input, outputs=predictions)
  return model