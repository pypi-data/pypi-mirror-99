# Low Rank Denoising Tools

Tools for low-rank denoising of MRSI.

This package contains functions to carry out:
- Global and local spatio-temporal low-rank denoising <sup>[4](#Nguyen)</sup>
- Global and local LORA <sup>[4](#Nguyen)</sup>
- Linear-predictability denoising <sup>[1,](#Cadzow)</sup><sup>[ 4](#Nguyen)</sup>
- SURE optimised local soft thresholding (SURE-SVT) <sup>[2](#Candès)</sup>
- SURE optimised local hard thresholding (SURE-SVHT) <sup>[6](#Ulfarsson)</sup>

## Command line script
#### Spatio-temporal
`mrsi_denoise st [--mask MASK] [-r RANK | -mp] [-p PATCH PATCH PATCH] [-s STEP] input output noise [noise]`

#### LORA
`mrsi_denoise lora ...`

#### LP
`mrsi_denoise lp ...`

#### SVT/SVHT
`mrsi_denoise svt...` / `mrsi_denoise svht ...`

## Python library
Denoising functions can be found in the _mrs_denoising.denoising_ module.

## Citation
If you use these tools please cite:  
```Clarke WT and Chiew M. ISMRM 2021```

## References
<a name="Cadzow">1</a>: Cadzow JA. Signal enhancement-a composite property mapping algorithm. IEEE Transactions on Acoustics, Speech, and Signal Processing 1988;36:49–62 doi: 10.1109/29.1488.

<a name="Candès">2</a>: Candès EJ, Sing-Long CA, Trzasko JD. Unbiased Risk Estimates for Singular Value Thresholding and Spectral Estimators. IEEE Transactions on Signal Processing 2013;61:4643–4657 doi: 10.1109/TSP.2013.2270464.

<a name="Chen">3</a>: Chen Y, Fan J, Ma C, Yan Y. Inference and uncertainty quantification for noisy matrix completion. PNAS 2019;116:22931–22937 doi: 10.1073/pnas.1910053116.

<a name="Nguyen">4</a>: Nguyen HM, Peng X, Do MN, Liang Z. Denoising MR Spectroscopic Imaging Data With Low-Rank Approximations. IEEE Transactions on Biomedical Engineering 2013;60:78–89 doi: 10.1109/TBME.2012.2223466.

<a name="Song">5</a>: Song J, Xia S, Wang J, Patel M, Chen D. Uncertainty Quantification for Hyperspectral Image Denoising Frameworks based on Low-rank Matrix Approximation. arXiv:2004.10959 [cs, eess] 2021.

<a name="Ulfarsson">6</a>: Ulfarsson MO, Solo V. Selecting the Number of Principal Components with SURE. IEEE Signal Processing Letters 2015;22:239–243 doi: 10.1109/LSP.2014.2337276.
