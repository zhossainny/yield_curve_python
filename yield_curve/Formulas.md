Interpolation Formulas - 
Linear Discount Factor Interpolation

$$
\text{ay} = y_1 + (a_x - x_1) \cdot \frac{y_2 - y_1}{x_2 - x_1}
$$

Yield Transformation

$$
\text{Interpolated Yield} = -\frac{\ln(\text{ay})}{t}
$$

where 

$$
t = \frac{a_x - x_0}{365.0}
$$

# LinearZeroInterpolator

## Formula
The interpolation formula used is:

$$
\text{ay} = y_1 + (a_x - x_1) \cdot \frac{y_2 - y_1}{x_2 - x_1}
$$

## Description
The `LinearZeroInterpolator` performs linear interpolation directly on the zero rates of a curve. It calculates an intermediate value using known data points. This method ensures smooth and precise zero-rate estimation for financial curve modeling.

