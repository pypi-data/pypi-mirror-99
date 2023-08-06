[![Build Status](https://travis-ci.com/arteagac/xlogit.svg?branch=master)](https://travis-ci.com/arteagac/xlogit)

# xlogitprit
A Python package for GPU-accelerated estimation of mixed logit models.
Multinomial and conditional logit models are also supported.
Allows for box-cox transformation and correlations between random parameters.

### Example:
The following example analyzes choices of fishing modes. See the data [here](examples/data/fishing_long.csv) and more information about the data [here](https://doi.org/10.1162/003465399767923827). The parameters are:
- `X`: Data matrix in long format (numpy array, shape [n_samples, n_variables])
- `y`: Binary vector of choices (numpy array, shape [n_samples, ])
- `varnames`: List of variable names. Its length must match number of columns in `X`
- `alt`:  List of alternatives names or codes.
- `randvars`: Variables with random distribution. (`"n"` normal, `"ln"` lognormal, `"t"` triangular, `"u"` uniform, `"tn"` truncated normal)
- `transvars`: Variables to apply box-cox transformation on

The current version of `xlogitprit` only supports data in long format.

#### Usage
```python
from xlogitprit import MultinomialLogit
# Read data from csv file
import pandas as pd
data_file = "https://raw.githubusercontent.com/arteagac/xlogit/master/examples/data/fishing_long.csv"
df = pd.read_csv(data_file)

varnames = ['price', 'catch']
X = df[varnames].values
y = df['choice'].values

model = MultinomialLogit()
model.fit(
  X,
  y,
  transvars=['price', 'catch'],
  transformation="boxcox",
  alts=['beach', 'boat', 'charter', 'pier'],
  varnames=varnames
)
model.summary()
```

#### Output
```
Estimation time= 0.1 seconds
---------------------------------------------------------------------------
Coefficient              Estimate      Std.Err.         z-val         P>|z|
---------------------------------------------------------------------------
price               -0.1217490820  0.0321450572 -3.7874899777      0.000635 ***
catch                1.0551803433  0.0897528665 11.7565085548      3.12e-29 ***
lambda.price         0.5989527910  0.0632937159  9.4630688430      1.39e-19 ***
lambda.catch         0.7122570277  0.0664899144 10.7122566429      1.26e-24 ***
---------------------------------------------------------------------------
Significance:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Log-Likelihood= -1290.203
AIC= 2588.405
BIC= 2608.705
```
For more examples of `xlogitprit` see [this Jupyter Notebook](https://github.com/PrithviBhatB/xlogit/tree/master/examples_prit).
To test how fast is MixedLogit with GPU processing you can use Google Colaboratory that provides some GPU processing for free. In the Jupyter Notebook above you just need to click the "Open in Colab" button to run your analysis.

## Installation
Install using pip:  
`pip install xlogitprit`  
Alternatively, you can download source code and import `xlogitprit.MixedLogit`

### Enable GPU Processsing
To enable GPU processing you must install the CuPy library  ([see installation instructions](https://docs.cupy.dev/en/stable/install.html)).  When xlogit detects that CuPy is installed, it switches to GPU processing.

## Notes:
The current version allows estimation of:
- Mixed logit models with normal, lognormal, triangular, uniform, and truncated normal distributions.
- Mixed logit models with panel data (balanced or unbalanced).
- Multinomial Logit Models: Models with individual specific variables
- Conditional Logit Models: Models with alternative specific variables
- Models with both, individual and alternative specific variables
- Lambda parameters for box-cox transformation of fixed and random parameters
- Correlations between random parameters

