from  tensorflow.keras import applications
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import GlobalAveragePooling2D, Dropout, Dense
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

basepath = "C:/Users/kevin/DL_Practice/SignProject/images/"

datagen_train = ImageDataGenerator(preprocessing_function=tf.keras.applications.resnet_v2.preprocess_input,
                                   validation_split=0.2, horizontal_flip=True, zoom_range=0.1,
                                   featurewise_center=True)
datagen_test = ImageDataGenerator(preprocessing_function=tf.keras.applications.resnet_v2.preprocess_input)

batch_size=128

train_generator = datagen_train.flow_from_directory(basepath+"rps_train_2",
                                                    target_size=(200, 200),
                                                    color_mode='rgb',
                                                    batch_size=batch_size,
                                                    class_mode='categorical',
                                                    shuffle=True,
                                                    subset=("training"))

validation_generator = datagen_train.flow_from_directory(basepath+"rps_train_2",
                                                    target_size=(200, 200),
                                                    color_mode='rgb',
                                                    batch_size=batch_size,
                                                    class_mode='categorical',
                                                    shuffle=False,
                                                    subset=("validation"))

test_generator = datagen_test.flow_from_directory(basepath+"rps_test_2",
                                                    target_size=(200, 200),
                                                    color_mode='rgb',
                                                    batch_size=batch_size,
                                                    class_mode='categorical',
                                                    shuffle=False)


Res50V2 = applications.ResNet50V2(weights="imagenet", include_top=False, input_shape= (200, 200, 3))

NAME = f'RPS_2_Resnet'
base_model = Res50V2
base_model.summary()
x = base_model.output

for layer in base_model.layers[:-33]:
    layer.trainable = False


x = GlobalAveragePooling2D()(x)

predictions = Dense(4, activation='softmax')(x)
    
model = Model(inputs = base_model.input, outputs = predictions)     

model.compile(optimizer='Adam',loss='categorical_crossentropy', metrics=['accuracy'])

epochs=3
    
tensorboard = TensorBoard(log_dir=f'logs\{NAME}')

lr_plat = ReduceLROnPlateau(patience=2, mode='min')
checkpoint = ModelCheckpoint(f"{NAME}_model_weight.h5", monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
callback_list = [lr_plat, checkpoint, tensorboard]

history = model.fit(train_generator,
                epochs=epochs,
                steps_per_epoch=train_generator.n//train_generator.batch_size,
                callbacks=callback_list,
                validation_data=validation_generator,
                validation_steps=validation_generator.n//validation_generator.batch_size)

model.evaluate(test_generator)

model_json = model.to_json()
with open(f'{NAME}_model.json', 'w') as json_file:
    json_file.write(model_json)