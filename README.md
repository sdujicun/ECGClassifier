#Emotion Classification Based on Electrocardiogram Signals

<!--
*Preprint*: [arxiv:2102.00457](https://arxiv.org/abs/2102.00457)

> <div align="justify"> Rocket and MiniRocket, while two of the fastest methods for time series classification, are both somewhat less accurate than the current most accurate methods (namely, HIVE-COTE and its variants). We show that it is possible to significantly improve the accuracy of MiniRocket (and Rocket), with some additional computational expense, by expanding the set of features produced by the transform, making MultiRocket (for MiniRocket with Multiple Features) overall the single most accurate method on the datasets in the UCR archive, while still being orders of magnitude faster than any algorithm of comparable accuracy other than its precursors.

## Reference
If you use any part of this work, please cite:
```
@article{Tan2021MultiRocket,
  title={{MultiRocket}: Effective summary statistics for convolutional outputs in time series classification},
  author={Tan, Chang Wei and Dempster, Angus and Bergmeir, Christoph and Webb, Geoffrey I},
  year={2021},
  journal={arxiv:2102.00457}
}
```
-->



## Code
```
Package:
data:				Emotion ECG Dataset
experiments:        The experiments to show results
features:           The used features 
steps:				The steps to classification emotion
results:            The results of experiments
``` 



<!--
The [main.py](main.py) file contains a simple code to run the program on a single UCR dataset.

The [main_ucr_109.py](main_ucr_109.py) file runs the program on all 109 UCR datasets.

The [main_mtsc.py](main_mtsc.py) file contains a simple code to run the program on a single [MTSC](http://timeseriesclassification.com/dataset.php) dataset.
```
Arguments:
-d --data_path          : path to dataset
-p --problem            : dataset name
-i --iteration          : determines the resample of the UCR datasets
-f --featureid          : feature id for MultiRocket
-n --num_features       : number of features 
-k --kernel_selection   : 0=use MiniRocket kernels (default), 1=use Rocket kernels
-t --num_threads        : number of threads (> 0)
-s --save               : 0=don't save results, 1=save results
``` 
-->

## Results
<!--
These are the results on 30 resamples of the 109 UCR Time Series archive 
from the [UCR Time Series Classification Archive](https://www.cs.ucr.edu/~eamonn/time_series_data_2018/).
MultiRocket is on average the current most accurate scalable TSC algorithm, that is more accurate than 
HIVE-COTE/TDE (HC-TDE).
<p align="center">
  <img src="results/figures/cd_multirocket_sota_resample.png"/>
</p>

<p float="center" align="center">
  <img src="results/figures/annotated_scatter_multirocket_vs_hc_resample.png" width="400" align="center"/>
  <img src="results/figures/scatter_multirocket_vs_minirocket_resample.png" width="400" align="center"/>
</p>


The following shows the total compute time for 109 UCR datasets. 
Compute times are averaged over 30 resamples of 109 UCR datasets and run on a cluster using 32 threads on AMD EPYC 7702 CPUs.
<p align="center">
  <img src="results/figures/timings_vs_minirocket.png" width="600" align="center"/>
</p>

The following table contains the averaged accuracy over 30 resamples of 109 UCR datasets, 
found in [results](results/all_resamples_average.csv). 
The results for other classifiers can also be obtained from [timeseriesclassification.com](http://timeseriesclassification.com/results.php).

|dataset_name                  |MultiRocket|HC-TDE     |HC-CIF     |HIVE-COTEv1_0|TS-CHIEF   |MiniRocket |MiniRocket_40k|Rocket     |Rocket_40k |InceptionTime|ResNet     |TDE        |CIF        |ProximityForest|STC        |RISE       |S-BOSS     |WEASEL     |cBOSS      |BOSS       |Catch22    |TSF        |minirocket_202_20k|minirocket_202_40k|minirocket_302_30k|minirocket_304_30k|minirocket_48_20k|minirocket_48_40k|minirocket_58_30k|minirocket_60_40k|rocket_201_20k|rocket_202_20k|rocket_304_30k|rocket_48_20k|rocket_48_40k|rocket_58_30k|
|------------------------------|-----------|-----------|-----------|-------------|-----------|-----------|--------------|-----------|-----------|-------------|-----------|-----------|-----------|---------------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|------------------|------------------|------------------|------------------|-----------------|-----------------|-----------------|-----------------|--------------|--------------|--------------|-------------|-------------|-------------|
|ACSF1                         |0.85       |0.855      |0.851      |0.85         |0.807      |0.822333333|0.822         |0.807      |0.807666667|0.826666667  |0.824      |0.797666667|0.767      |0.638333333    |0.838333333|0.76       |0.815      |0.818      |0.757333333|0.768333333|0.777666667|0.635      |0.85              |0.845333333       |0.852333333       |0.860333333       |0.855333333      |0.849            |0.84             |0.846333333      |0.851666667   |0.844333333   |0.853333333   |0.842666667  |0.844666667  |0.851333333  |



[Here](results/results_128_resample_0.csv) are the results for some MultiRocket variants on the full 128 UCR datasets.

[Here](results/resamples/) are the results for some MultiRocket variants on 30 resamples of 109 UCR datasets.
-->


## Acknowledgement
We would like to thank Professor Mohammad Soleymaniand their team who have provided the [MAHNOB-HCI-Tagging database](https://mahnob-db.eu/hci-tagging). 
<!--
We also would like to thank Professor Geoffrey I. Webb and their team who have provided the codes of  [MiniRocket](https://github.com/angus924/minirocket)([Paper Link](https://arxiv.org/abs/2012.08791)) and [MultiRocket](https://github.com/ChangWeiTan/MultiRocket)([Paper Link](https://arxiv.org/abs/2102.00457)).
-->
We appreciate the python ECG processing packages, **NeuroKit2**([Paper Link](https://link.springer.com/article/10.3758/s13428-020-01516-y)), **pywavelets**([Paper Link](https://joss.theoj.org/papers/10.21105/joss.01237)), **heartpy**([Paper Link](https://www.humanist-vce.eu/fileadmin/contributeurs/humanist/TheHague2018/33-VanGent.pdf)). We also appreciate the open source code to draw the critical difference diagrams from [Hassan Fawaz](https://github.com/hfawaz/cd-diagram).
