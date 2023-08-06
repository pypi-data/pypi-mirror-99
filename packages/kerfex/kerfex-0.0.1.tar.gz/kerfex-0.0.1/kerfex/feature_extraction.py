import numpy as np
import pandas as pd
from keras.models import Model
from keras.preprocessing import image
from keras.layers import Flatten, Input

def extract(keras_model, keras_preprocess, image_list, shape, summary = False):
    
    model = keras_model(weights='imagenet', include_top = False)
    
    if summary:
        model.summary()

    images = []
    for img in image_list:
        img_data = image.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = keras_preprocess(img_data)
        images.append(img_data)

    images = np.vstack(images)
    
    input = Input(shape=shape, name='input')
    
    output = model(input)
    x = Flatten(name='flatten')(output)
    
    extractor = Model(inputs=input, outputs=x)
    features = extractor.predict(images)

    df = pd.DataFrame.from_records(features)
    df = df.loc[:, (df != 0).any(axis=0)]
    df.columns = np.arange(0,len(df.columns))
    
    return df