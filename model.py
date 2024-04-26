import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, Dense, Dropout, Concatenate, Flatten
from tensorflow.keras.layers import MultiHeadAttention, LayerNormalization, GlobalAveragePooling1D
from tensorflow.keras.models import Model

def create_bst_model(feature_shape, num_tokens, embedding_dim):
    # Input layers for categorical and numerical features
    categorical_inputs = Input(shape=(feature_shape[0],), dtype='int32', name='categorical_inputs')
    numerical_inputs = Input(shape=(feature_shape[1],), dtype='float32', name='numerical_inputs')
    

    # Embedding layer for categorical features
    categorical_embeddings = Embedding(input_dim=num_tokens, output_dim=embedding_dim)(categorical_inputs)
    
    # Transformer layer
    transformer_output = MultiHeadAttention(num_heads=4, key_dim=embedding_dim)(categorical_embeddings, categorical_embeddings)
    x_transformed = LayerNormalization()(transformer_output + categorical_embeddings)
    x_transformed = GlobalAveragePooling1D()(x_transformed)

    # Combine the outputs of the transformer with numerical input
    x_combined = Concatenate()([x_transformed, numerical_inputs])

    # MLP layers
    x = Dense(256, activation='relu')(x_combined)
    x = Dropout(0.2)(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.2)(x)

    # Output layer
    outputs = Dense(1, activation='sigmoid')(x)

    # Build the model
    model = Model(inputs=[categorical_inputs, numerical_inputs], outputs=outputs)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Assume feature_df is prepared with all required preprocessing
# Create a model instance with appropriate dimensions
num_features = (10, 5)  # Example dimensions for categorical and numerical features
num_tokens = 5000  # Example token count for embeddings
embedding_dim = 64  # Embedding dimension size

model = create_bst_model(num_features, num_tokens, embedding_dim)
model.summary()

# model.fit(X_train, y_train, epochs=10, batch_size=32)
# model.save('bst_model.h5')
