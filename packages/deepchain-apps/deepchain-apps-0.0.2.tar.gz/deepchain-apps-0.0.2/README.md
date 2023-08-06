# `deepchainapps` package for creating a personnal app to deploy on the DeepChain platform

## Getting started with the package
The package provide some high level interface and templates to create your own application (score to optimize for example) and deploy on deepchain.

### CLI

You can create a template, in which you can find a base template that you have to follow do safely deploy you application.

>deepchainsapp create --type score --folder-name my_app

It will create a folder with the following architecture:
 - my_app
    - score.py
    - example_scorer.py
    - checkpoint
        - model_weights.h5 (for tf/keras)
        - model.pt (for pytorch)
    - requirements.txt

>deepchainapps deploy --app my_app

The application will be deploy in DeepChain plateform.

### Embedding

Some embeddings are provided in the `TransformersApp` module
> from deepchainapps.components import TransformersApp

The model are furnished, but not mandatory, if you want to make an embedding of your protein sequence.
Only the ESM (evolutionary scale modeling) model is provided, with different architecture.
Here for some full details of the architecture (https://github.com/facebookresearch/esm)
 - 'esm1_t6_43M_UR50S'
 - 'esm1_t12_85M_UR50S'
 - 'esm_msa1_t12_100M_UR50S'
 - 'esm1b_t33_650M_UR50S' 
 - 'esm1_t34_670M_UR100' 
 - 'esm1_t34_670M_UR50D'
 - 'esm1_t34_670M_UR50S'

!! The embedding will run on a GPU on the plateform. But for a testing phase on your personal computer (CPU), you should choose the smaller architecture.
