# `deepchain-apps` : Package for creating a personnal app to deploy on the DeepChain platform

## Getting started with the package
The package provide some high level interface and templates to create your own application (score to optimize for example) and deploy on deepchain.

## CLI
The CLI provides 3 main commands:

- login : you need to supply the token provide on the plateform
(need to provide your password and a config file)
> deepchain login

- create : create a folder with a template scorer file
> deepchain create my_application

Create a folder with the architecture:
- my_application
    - myscorer.py
    - checkpoints (model.[h5/pt])
    - requirements

- deploy : the code and folder is deployed on the plateform, you can select your app on the plateform
>deepchain deploy my_application --checkpoints path_to_checkpoints

The application will be deploy in DeepChain plateform.

## Embedding

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
