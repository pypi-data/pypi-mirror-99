```python
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import sbibm
from sbi.inference import MCABC, SMCABC
from sbi.utils import pairplot
import torch
import numpy as np
```


```python
task = sbibm.get_task("gaussian_linear_uniform")
prior = task.get_prior_dist()
simulator = task.get_simulator()
num_obs = 1
x_o = task.get_observation(num_obs)
ref = task.get_reference_posterior_samples(num_obs)[:1000]
```


```python
inferer = MCABC(simulator, prior, show_progress_bars=False, simulation_batch_size=1000)
pilot_posterior = inferer(x_o, num_simulations=2000, quantile=0.2)
```


```python
pairplot([ref, pilot_posterior.sample((1000,))], upper="scatter");
```


![png](SAAS_files/SAAS_3_0.png)



```python
theta_pilot = pilot_posterior.sample((400,))
x_pilot = simulator(theta_pilot)
```


```python
poly = PolynomialFeatures(1)

coef = np.zeros(shape=(task.dim_data, task.dim_parameters))
bias = np.zeros(shape=(task.dim_parameters))

for ip in range(task.dim_parameters):
    reg_model = LinearRegression(fit_intercept=True, normalize=False)
    reg_model.fit(X=x_pilot, y=theta_pilot[:, ip])
    coef[:, ip] = reg_model.coef_
    bias[ip] = reg_model.intercept_
```


```python
x_pilot.shape
```




    torch.Size([400, 10])




```python
PolynomialFeatures(1).fit_transform(x_pilot)[:, 1:]
```




    array([[-0.2031682 , -0.48954996,  0.96856982, ...,  0.71458125,
            -0.40119061,  0.57383084],
           [ 0.7047686 , -0.66010571,  0.26302183, ..., -1.17002964,
            -0.37095746,  0.26936266],
           [ 0.0188488 ,  0.81169927,  0.58200991, ..., -0.81080019,
            -0.92812759,  0.29775125],
           ...,
           [-1.0352726 , -0.05900063,  0.67377096, ...,  0.69162774,
            -0.69020683, -0.83395469],
           [ 0.12557407,  0.19850314,  0.48951373, ..., -0.32562912,
             0.66842121,  0.6879915 ],
           [ 0.61038578, -0.48689294,  0.00632868, ..., -0.15661705,
            -1.0272882 , -0.02754444]])




```python
def ss_transform(x):
    return x.mm(torch.tensor(coef, dtype=torch.float32))

def ss_simulator(theta):
    return ss_transform(simulator(theta))
```


```python
pairplot([ref, theta_pilot, ss_transform(simulator(theta_pilot))+bias], upper="scatter");
```


![png](SAAS_files/SAAS_9_0.png)



```python
inferer = SMCABC(ss_simulator, prior, show_progress_bars=False, simulation_batch_size=1000)
posterior = inferer(ss_transform(x_o), 200, 1000, 8000, 0.5, distance_based_decay=True, )
```


```python
pairplot([ref, pilot_posterior.sample((1000,)), posterior.sample((1000,))], upper="scatter");
```


![png](SAAS_files/SAAS_11_0.png)



```python
inferer = SMCABC(simulator, prior, show_progress_bars=False, simulation_batch_size=1000)
posterior2 = inferer(x_o, 200, 1000, 10000, 0.5, distance_based_decay=True, )
```


```python
from sbibm.metrics import c2st
```


```python
c2st(ref, pilot_posterior.sample((1000,)))
```




    tensor([0.9885])




```python
c2st(ref, posterior.sample((1000,)))
```




    tensor([0.9605])




```python
c2st(ref, posterior2.sample((1000,)))
```




    tensor([0.9525])




```python

```
