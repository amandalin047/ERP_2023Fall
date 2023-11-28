## The Unit of _Power_ 
If you're confused about the _power_ of a frequency band and its relation to _amplitude_, here's an explanation from the perspective of base quantities:

Recall Ohm's Law in physics

$$R = \frac{V}{I}$$

where R is the resistance of an electric circuit. This can be extended to impedance as follows

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




