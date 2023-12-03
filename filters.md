## The Unit of _Power_ 
If you're confused about the _power_ of a frequency band and its relation to _amplitude_, here's an explanation from the perspective of base quantities:

Recall Ohm's Law in physics

$$R = \frac{V}{I}$$

where $R$ is the resistance of an electric circuit. This can be extended to impedance as follows

$$Z = \frac{V}{I}$$

The definition of "voltage", i.e., _electric potential_ (measured in volts or microvolts) is the amount of _work_ (energy transferred) needed per unit charge to move from a reference point to another point in space against an electric field, and that the definition of _current_ (measured in amperes) is the flux of electric charge per unit time. Therefore, multiplying voltage by current, we obtain the energy per unit time, i.e., _power_ (measured in watts, which is joules per second)

$$P = VI = \frac{V^2}{Z}$$

In signal processing, however, the term "power" refers to the energy (measured in joules) at a frequency band, instead of energy per unit time, and, for some odd reason, power here is conventionally not divided by ohm, so we have

$$P_f = \frac{V^2}{Hz}$$

as $1$ Hertz is the inverse of $1$ second.

## Decibel
Decibel (dB) is the ratio $L$ of $P$ (some power value) to $P_0$ (reference power)

$$L = 10log(\frac{P}{P_0})\text{ dB}$$

Thus, "half power" (i.e., $P = 0.5P_0$) corresponds to

$$10log(0.5) ≈ 10 × (-0.3) = -3\text{ dB}$$

To get "half amplitude" is equivalent to getting "a quarter power" (since $0.5 × 0.5 = 0.25$), so half amplitude corresponds to

$$10log(0.25) ≈ 10×(-0.6) = -6\text{ dB}$$

## Filter Roll-offs
About the three measures of _roll-off_ you see in the `ERPLAB > Filter & Frequency tools` GUI, please note that the relation between $dB/octave$ and $dB/decade$ always holds true mathematically, but their relation with order is only so because we're implementing the IIR Butterworth filter.

The key to converting $dB/octave$ to $dB/decade$ (or vice versa) is understanding that one octave means doubling, whereas one decade means multiplying by $10$, and that roll-off in $dB/octave$ means "the power ratio to some reference power when the frequency doubles" (or, in plain English, "how many times greater does the power become relative to some reference power value when the frequency becomes twice as high"). Below we convert $6\text{ }dB/octave$ to its $dB/decade$ equivalent:

$6\text{ dB/octave}$

⮕ The power becomes $10^{0.6}$ times as large when the frequency doubles

⮕ When the frequency is multiplied by $10$, which is $2^{log_{2}\left(10\right)}$, the power is then multiplied by $(10^{0.6})^{log_{2}\left(10\right)}$

⮕ In $dB$, you take the logarithmic, which means multiplying $6\text{ dB}$ by $log_{2}(10)$

$$6log_{2}\left(10\right) ≈ 19.93 ≈ 20$$

That is, 
$$6\text{ dB/octave} ≈ 20\text{ dB/decade}$$

As for order, just accept that with an IIR Butterworth filter, $n-th$ order corresponds to a $6n\text{ dB/octave}$ roll-off for now as we'll need a better understanding of impulse response functions and frequency response functions (transfer functions) — read on!

## Impulse Response Functions
There are different types of filters: _causal_ vs _non-causal_, _finite impulse response (FIR)_ vs _infinite impulse response (IIR)_, etc.

_Causal_ refers to when the filter is only determined by signals at the present time and at time points in the past. Online filters are causal since future signals are unknown. ERPLAB offline filters are _non-causal_, for — according to Luck — such filters are less likely to cause "phase shifts" (I'm not sure why exactly).

An _impulse response function_ refers to the signals in response to an impulse (Dirac Delta function). What's meant by _finite_ is that the response function has a finite length in time, whereas _infinite_ refers to when the response function lasts an infinitely long duration. One key difference between FIR and IIR is that IIR has a feedback mechanism. The rest of this section focuses on causal FIR filters (because that's the one I understand better).

Let $x[n]$ denote the input signal at the $n$-th discrete time point, and $y[n]$ the output, then a causal finite impulse response filter of order N is expressed as

$$y[n] = b_{0}x[n] + b_{1}x[n-1] +\text{ ... }b_{N}x[n-N]$$

where $b_{i}$ are weight coefficients. This means that the output signal $y[n]$ at time $n$ is determined by the present input and past input from $N-1$ time points. Here $N$ is called the _order_ of the finite response.

The _impulse response function_ $h[n]$, then, can be expressed as

$$h[n] = \sum_{i=0}^{N} b_{i}\delta[n-i]$$

where $\delta[n]$ is the Dirac Delta function with value $1$ at time $n$ and value $0$ everywhere else. Note also that the Dirac Delta function has this nice property

$$f(t) = \sum_{i=-\infty}^{\infty}f(i)\delta(t-i)$$

As such, we can express the output signal $y[n]$ in terms of _discrete convolution_

$$
\begin{aligned}
y[n] &= \sum_{i=0}^{N} b_{i}x[n-i] \\
     &= \sum_{i=0}^{N} b_{i}\sum_{j=-\infty}^{\infty}x[j]\delta[n-i-j] \\
     &= \sum_{i=0}^{N}\sum_{j=-\infty}^{\infty}b_{i}\delta[n-i-j]x[j] \\
     &= \sum_{j=-\infty}^{\infty}x[j] \sum_{i=0}^{N} b_{i}\delta[n-j-i] \\ 
     &= \sum_{j=-\infty}^{\infty}x[j] h[n-j] \\
     &= (x*h)[n] \\
\end{aligned}
$$

