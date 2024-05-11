# Movie-Recommender-DL-Spring2024

We are interested in movie recommendation model and want to find a NN model in this field to reimplement it for our final project. We choose the BST model because it utilize the transformer architecture. Since transformer is SOA model in many fields, we want to see if it is also good at movie recommendation. 

BST takes as input the user’s behavior sequence, including the target item, and “Other Features”. The first layer is embedding layers which embeds the input features. The second layer is transformer layers which is used to learn deeper representation of the input features. (only ENCODER is used because we do not need to generate sequence output) Then by concatenating the embeddings of Other Features and the output of the transformer layer, the three-layer MLPs are used to learn the interactions of the hidden features, and sigmoid function is used to generate the final output.

The concept of our project will be product-driven, meaning the architecture design and functionality will be more important than some performance metric numbers that we output. So it is crucial to think about what kind of product we are going to shape our framework into, and what a on-point, non-judgemental, diversified movie recommendation system should be different from Google’s “You might also like..”. 
We are interested in movie recommendation models and want to find a NN model in this field to reimplement it for our final project. We choose the BST model because it utilizes the transformer architecture. Since Transformers are SOA models in many fields, we want to see if it is also good for movie recommendation.

## Model Architecture
BST takes as input the user’s behavior sequence, including the target item, and “Other Features”. 
The first layer is embedding layers which embeds the input features.
The second layer is transformer layers which is used to learn deeper representation of the input features. 
(only ENCODER is used because we do not need to generate sequence output)
Then by concatenating the embeddings of Other Features and the output of the transformer layer, the three-layer MLPs are used to learn the interactions of the hidden features, and sigmoid function is used to generate the final output. 

## Results

(Check BST Model.ipynb for codes)

<img src="https://github.com/urspuc/Movie-Recommender-DL-Spring2024/assets/113117803/7695ce72-ae01-4595-8a73-8a6b516a1408" width="400"> <!-- Adjust width as needed -->

<img src="https://github.com/urspuc/Movie-Recommender-DL-Spring2024/assets/113117803/04ee0708-d8f8-470d-bb1c-0ae16aeb0753" width="400"> <!-- Adjust width as needed -->

<img src="https://github.com/urspuc/Movie-Recommender-DL-Spring2024/assets/113117803/f4353a2e-4943-4399-9fb6-066de057b288" width="400"> <!-- Adjust width as needed -->

## References

1. **Original Paper**: [Behavior Sequence Transformer for E-commerce Recommendation in Alibaba](https://arxiv.org/pdf/1905.06874) - This paper introduces the Behavioral Sequence Transformer model, providing foundational concepts.
2. **Supplementary Paper**: [Multimodal Movie Recommendation System Using Deep Learning](https://www.mdpi.com/2227-7390/11/4/895) - This paper discusses extensions and variations to the original model, applying it within the context of movie recommendations.
3. **Previous Implementation**: [Behavior Sequence Transformer implemented in PyTorch by jiwidi](https://github.com/jiwidi/Behavior-Sequence-Transformer-Pytorch) - This GitHub repository features an implementation of the BST model in PyTorch, serving as a reference for practical application.
