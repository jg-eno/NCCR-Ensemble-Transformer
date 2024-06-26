# Cold Wave Analysis using Self-Attentive Ensemble Transformer

Representing Ensemble Interactions in Neural Networks for Earth System Models

This project and repository is dedicated to enable processing of ensemble data
for Earth system models with neural networks.
Based on ideas from self-attention and ensemble data assimilation, specifically
the ensemble Kalman filter, this repostory includes modules for the
self-attentive ensemble transformer.
The ensemble transformer is a novel type of neural network to process
ensemble data without a parametric assumption, as it is usually done in
post-processing or Model Output Statistics.

We use this Model Architecture to improve cold wave analysis.

The scripts and module is written in PyTorch , Pytorch lightning and
configured with Hydra.

The folder structure is the following:

```
.
|-- configs            # The hydra config scripts.
|-- data               # Storage of the data
|   |-- interim        # Data that is included within the repo
# The experiment data (the used configs for all experiments can be found in
# sub directories and the hydra folder.
|   |-- models         # The trained models will be stored here
|   |-- processed      # The processed data is stored here
|   |   |-- era5       # The processed ERA5 data as zarr directories
|   |   |-- ifs        # The processed IFS data as zarr directories
|   |   |-- predicted  # The post-processed network predictions as NetCDF-files
|   |-- raw            # The raw data should be stored here
|   |   |-- era5       # The raw ERA5 data as NetCDF-files
|   |   |-- ifs        # The raw IFS data as NetCDF-files
|   |-- tensorboard    # Data for tensorboard visualization can be stored here
|-- ens_transformer    # The python module with different model etc.
|   |-- layers         # Different PyTorch modules for ensemble processing
|   |-- models         # Pytorch Lightning network specifications
|   |-- transformers   # Different self-attentive transformer modules
|-- notebooks          # Notebooks that were used to visualize the results
|-- scripts            # The scripts that were used to train the models
|   |-- data           # Scripts and notebooks to download and process the data
|   |-- predict.py     # Script to predict with a trained neural network
|   |-- train.py       # Hydra-script to train the networks
|-- environment.yml    # A possible environment configuration
|-- LICENSE            # The license file
|-- README.md          # This readme
|-- setup.py           # The setup.py to install the ens_transformer modules
|-- used_env.yml       # The used conda environment with pinned versions
```

In almost all scripts only relative directories are used to reference the
data and models.

As a first step the ERA5 data has to be downloaded from . All other
scripts to pre-process the data can be found in `scripts/data/`.
The data raw model data to be put into `scripts/data/raw`.

To download IFS dataset, use the script, `download_tigge.py` and specify
the required arguments.

To pre-process the data, Follow the below steps:

1. Merge and regrid the ERA5 files of induvidual variables(t2m, z500,
   t850) using `regrid_merge_era5.py` to match the downloaded resolution of ifs.
2. Then run `process_process_era5.ipynb` to do a train, test split and
   save it locally.
3. Then run `process_ecmwf.ipynb` to do a train, test split and save it
   locally.

   Afterwards, the `scripts/train.py` script can be used to train the networks.
   Specific options can be overwritten via Hydra syntax.
   To reproduce networks from the paper different model configurations are
   stored under `data/models/*/hydra/config.yaml`.
   These files can be then used to rerun the experiment.
   The subfolder `data/models/subsampling` was used for the subsampling experiments.
   The subfolder `data/models/baseline_scaling` was used for the scaling
   experiments with the baseline models.
   The subfolder `data/models/transformer_scaling` was used for the scaling
   experiments with the transformer networks.

   Inorder to plot the graphs and check for the accuracy and occurances of cold waves follow the below steps:

   1. Open the `Cold_Wave_Predictor.py` in the `Cold_Wave_Predictor` folder.
   2. Move the files that are required for the Climatology Temperature calculation(1990-2023.nc) into the Cold_Wave_Predictor folder.
      Requirements for these files are :
      a. 6°N 37°N 68°E 98°E
      b.Time-Stamps : 00 , 12
      c.Variables : t2m
      d.Pressure Levels : sfc
      e.Scale : 0.25
      f.Name all these files as {Year}.nc
   3. Move the Prediction file into the same folder and give it's name to line 30 in `Cold_Wave_Predictor.py`
   4. Now run the file and you will get a plot for the month of December 2023 (This plot is made for the central grid of Delhi `latitude=28.75,longitude=77.75`).
   5. You can also try experimenting the `T_current_min` to `T_current_mean` to get a better idea.
   6. You can also try plotting the raw ensemble members using plt.plot.
---

## References

<a id="1">[1]</a> https://pytorch.org/

<a id="2">[2]</a> https://www.pytorchlightning.ai/

<a id="3">[3]</a> https://hydra.cc/

<a id="4">[4]</a> https://cds.climate.copernicus.eu/

<a id="rasp">[Rasp & Lerch 2018]</a> Rasp, Stephan, and Sebastian Lerch.
"Neural Networks for Postprocessing Ensemble Weather Forecasts", Monthly
Weather Review 146, 11 (2018): 3885-3900,
https://doi.org/10.1175/MWR-D-18-0187.1

---
