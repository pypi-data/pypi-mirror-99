##  Overview

`clusterbootstraps` is a Python library for **estimating a linear regression model and carrying accurate inference with clustered errors using the (i) Pairs Cluster Bootstrap-T and (ii) Wild Cluster Bootstrap-T procedures.**

Detailed introduction of the bootstrap methodology are in reference: Cameron, A. Colin, Jonah B. Gelbach, and Douglas L. Miller. "Bootstrap-based improvements for inference with clustered errors." The Review of Economics and Statistics 90.3 (2008): 414-427.

The method is also programmed in Stata and namely wcbregress.

Last edited on 21st Sep 2020. Comments are welcome. 

##  Installations

This Python package can be installed via the **pip package manager** [pip](https://pip.pypa.io/en/stable/), i.e.:

```bash
pip install clusterbootstraps
```


##  Usages

###  Install Requires
`numpy` `pandas`  `statsmodels` `prettytable`

###  Syntax
```python
import clusterbootstraps.pair as cbp  # For Pairs Cluster Bootstrap-T
import clusterbootstraps.wild as cbw  # For Wild Cluster Bootstrap-T

result = cbp.Pair(Y,X,cluster_var,*args)  # input matrices or dataframes
result.table()                      # return the table
result = cbw.Wild(Y,X,cluster_var,*args)  # input matrices or dataframes
result.table()                      # return the table
```         
###  Arguments/Options
`clusterbootstraps`

Arguments|Introduction
:---:|:---:
`Y`|the dependent variable
`X`|the independent variables
`cluster_var`|the cluster variable you choose
`iter`[integer]|number of iterations,default = 10000 (optional)
`seed`[integer]|set random seed number,default = 2020 (optional)
`alpha`[float]|set the (1-alpha)% confidence level,default = 5 (optional)
`constant`[boolean]|set whether to add a constant term,default = True (optional)

###  Saved Variables
`clusterbootstraps` stores the following:

Saved Variables|Introduction
:---:|:---:
self.coef|Original Coefficient(s) of Sample
self.mean_coef|Average Coefficient(s) of n Iterations
self.mean|Mean of Bootstrap Sample Wald Statistic
self.upper_bound|Upper Bound of the Wald Statistic
self.lower_bound|Lower Bound of the Wald Statistic

###  Examples

#### Example 1: Pairs Cluster Bootstrap-T
Here, we run the linear regression of `logprice` on a set of covariates stored in the the matrix `X.matrix` and use the Pairs Cluster Bootstrap-T method to cluster the standard errors on level of five categories of variable `rep78`. 

In Python, we code:

```python
import clusterbootstraps.pair as cbp
result = cbp.Pair(Y = logprice,X = X.matrix,cluster_var = 'rep78')
result.table() 
```
Variables  | Original Coefs | Average Coefs | Pair Bootstrap Wald mean | Cluster Standard Error | Confidence Interval 
:---:|:---:|:---:|:---:|:---:|:---:
Constant|8.6109|8.5175|-0.1287|5.9876|[-1.5887,0.5903] 
mpg|-0.0029|-0.0035|0.1010|0.2905|[-5.1478,1.0900]   
headroom|-0.0571|-0.0667|-0.0127|8.3685|[-0.8497,1.1894]  
trunk|0.0134|0.0168|0.0645|0.8770|[-0.5975,0.9402]   
weight|0.0007|0.0006|-0.0247|0.0074|[-1.5046,1.3087]   
length|-0.0097|-0.0083|0.1133|0.2107|[-0.4805,0.6589]   
gear_ratio|-0.0976|-0.1123|-0.2112|0.7176|[-1.3575,0.5179]   
Foreign|0.5785|0.5624|0.2108|11.9997|[-0.6242,2.3799]

#### Example 2: Wild Cluster Bootstrap-T
We run the same regression and use the Wild Cluster Bootstrap-T to cluster the standard errors.

```python
import clusterbootstraps.wild as cbw
result = cbw.Wild(Y = logprice,X = X.matrix,cluster_var = 'rep78')
result.table() 
```
Variables  | Original Coefs | Average Coefs | Wild Bootstrap Wald mean | Cluster Standard Error | Confidence Interval 
:---:|:---:|:---:|:---:|:---:|:---:
Constant|8.5856|9.9176|-0.0005|4.4941|[-0.4562, 0.4540] 
mpg|0.0375|0.0191|-0.0010|0.1833|[-0.4230, 0.4274]  
headroom|-0.0564|0.0985|0.0016|0.1387|[-0.4482, 0.4463]  
trunk|0.0119|-0.0211|-0.0017|0.0618|[-0.3145, 0.3158]   
weight|0.0007|0.0003|0.0027|0.0009|[-0.4290, 0.4369]  
length|-0.0101|-0.0105|-0.0012|0.0298|[-0.4168, 0.4160]  
gear_ratio|-0.0827|0.1363|0.0003|0.7062|[-0.4237, 0.4246]  
Foreign|0.5241|-0.3451|0.0008|0.6639|[-0.3882, 0.3967]  


## Reference
Cameron, A. Colin, Jonah B. Gelbach, and Douglas L. Miller. "Bootstrap-based improvements for inference with clustered errors." The Review of Economics and Statistics 90.3


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Authors and Contact
Bingkun Lin (Coder maintainer, email: linbingkun.iesr18u@outlook.com)

Shiyue Shen 

Ziyi Zhan 

Zizhong Yan

Authors are from the IESR, Jinan University, Guangzhou, China.

## Package Homepage
https://github.com/BingkunLin/clusterbootstraps


## License
[MIT License](https://choosealicense.com/licenses/mit/)

Copyright (c) 2020 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

