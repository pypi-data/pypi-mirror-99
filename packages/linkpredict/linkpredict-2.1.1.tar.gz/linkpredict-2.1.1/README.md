# LinkPredict

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gl/librecube%2Flib%2Fpython-linkpredict/master?filepath=docs%2Fexamples)

LinkPredict is a Python3 module for defining radio links in a generic
and modular way and provides time-dependent outputs of the link performance.

*Generic* means that one can construct radio links for terrestrial applications
as well as space-to-ground, ground-to-space, orbiter-to-rover, and others.

*Dynamic* means every input value to the link budget can be supplied as a
time-varying function. This way, the time-dependent effects (such as change of
distance) can be analyzed and visualized.

LinkPredict can be installed via pip:

```bash
$ pip install linkpredict
```

## Getting Started

A link budget is an estimation technique for the evaluation of communication
system error performance. It consists of calculations to determine the
useful signal power and the interfering noise power available at the receiver.

Given a particular link setup the question is whether the communication link
quality will be good, marginal, or insufficient. Each communication link uses
some form of coding and modulation, which requires a certain signal to noise
ratio (or EbNo for digital communication) in order to achieve a desired bit
error probability. When the link budget has margin, the link requirements
are met.

The ``linkpredict`` module provides a number of classes to be assembled
together to form the radio link. The link goes from a transmitting element
to a receiving element and travels through the propagation path.

### Link

In order to assembly a link budget, create an instance for each class and
provide them as arguments to the ``Link`` class.

```python
import linkpredict as lp

channel = lp.Channel(...)
# ...

link = lp.Link(
    channel=channel,
    geometry=geometry,
    transmitter=transmitter,
    transmit_antenna=transmit_antenna,
    receive_antenna=receive_antenna,
    receive_antenna_noise=receive_antenna_noise,
    receiver=receiver,
    medium_losses=medium_losses)

result = link.calculate_link_budget()
```

The ``calculate_link_budget`` method can be called without arguments to return
a static link budget result. If any of the link elements however provide time
dependent characteristics (for example, the slant range will change for moving
objects), then you can supply either a time instance, or a time range. In the
later case, the result will be a list of dicts.

The returned dict or dicts contain the link budget results calculated per time
instance.

For example to display the signal power arriving at the receiver:

```python
print(result[lp.LinkBudgetKeys.received_power])
```

The following paragraphs give a brief overview on the

### Channel

The ``Channel`` class specifies the properties of the radio link. Foremost this is
the frequency being used and also the modulation (if any). There are classes
for analog and digital modulation schemes.

```python
Channel(frequency, pfd_limit=None, received_power_threshold=None, modulation=None)
```

### Geometry

The geometrical layout of your link budget scenario is captured in the
``Geometry`` base class. This could be a static one with fixed distance (slant range)
and antenna angles, or one where geometry is changing over time. The common
use case of groundstation tracking a satellite is captured in the
``GroundstationSpacecraftGeometry`` class, which is a child class of ``Geometry``.

```python
SimpleGeometry(slant_range, tx_antenna_angle=0, rx_antenna_angle=0)
```

### Transmitter

The ``Transmitter`` class contains all the devices on the sending side of the
link, except the antenna. The ``Device`` class is for defining active and passes
components of the transceiver, such as cables and filters.

```python
Transmitter(amplifier_power, devices=None)
```

### Transmit Antenna

The signal from the transmitter is radiated via the antenna. The ``Antenna`` class
is a base class for specific antenna implementations. A commonly used antenna
is the ``OmniDirectionalAntenna``, which radiates evenly in all directions.

```python
OmniDirectionalAntenna(gain, linear_polarized=False)
```

### Receive Antenna

On the receiver side, an antenna receives the radiated signal. The properties
of transmit and receive antennas are identical. This means that for example the
``OmniDirectionalAntenna`` picks up signals evenly from all directions.

### Receive Antenna Noise

There is however a difference between the antenna on the sending side and the
receiving side of the radio link. The later picks up other signals/noise as
well. This can for example be captured using the antenna noise temperature:

```python
SimpleAntennaNoise(noise_temperature)
```

### Receiver

The ``Receiver`` class contains all the devices on the receiving side of the
link, excluding the antenna. Again, the ``Device`` class is for defining active
and passes components of the receiver.

```python
Receiver(noise_temperature=None, devices=None)
```

### Medium Losses

Finally, the signal that travels from the sender to the receiver is subject to
losses due to the medium it travels through. Losses would be zero in vacuum, but
non zero for atmosphere due to reflection, absorption, polarization, scattering,
and so on. The ``MediumLoss`` class is a base class for specific implementations.

```python
SimpleMediumLoss(medium_loss)
```

## Example of Static Link Budget

Let's create the link budget for the example defined in Table 1 from this
reference: http://www.waves.utoronto.ca/prof/svhum/ece422/notes/22-linkbudget.pdf

```python
import linkpredict as lp

# Transmitter
circuit = lp.Device(gain=-2.0)
transmitter = lp.Transmitter(amplifier_power=20, devices=[circuit])
transmit_antenna = lp.MainLobeAntenna(peak_gain=51.6, beam_3db_width=6)

# Path
geometry = lp.SimpleGeometry(slant_range=40.721e6, rx_antenna_angle=2.5)
fade = lp.SimpleMediumLoss(4.0)
other = lp.SimpleMediumLoss(6.0)
medium_losses= [fade, other]

# Channel
modulation = lp.AnalogModulation(bandwidth=2e6)
channel = lp.Channel(frequency=8e9, modulation=modulation)

# Receiver
receive_antenna = lp.MainLobeAntenna(peak_gain=35.1, beam_3db_width=6)
receive_antenna_noise = lp.SimpleAntennaNoise(300)
receiver = lp.Receiver(noise_temperature=3806)

# Link Budget
link = lp.Link(
    channel=channel,
    geometry=geometry,
    medium_losses=medium_losses,
    transmitter=transmitter,
    transmit_antenna=transmit_antenna,
    receive_antenna=receive_antenna,
    receive_antenna_noise=receive_antenna_noise,
    receiver=receiver)
result = link.calculate_link_budget()

k = lp.LinkBudgetKeys
fields = (
    k.tx_amplifier_power,
    k.tx_circuit_loss,
    k.tx_antenna_gain,
    k.eirp,
    k.slant_range,
    k.free_space_path_loss,
    k.medium_loss,
    k.total_path_loss,
    k.received_isotropic_signal_level,
    k.rx_antenna_gain,
    k.received_power,
    k.received_noise_power_density,
    k.rx_system_noise_temperature,
    k.cno_ratio,
    k.snr,
)
for field in fields:
    print("{}: {:0.1f} {}".format(field.name, result[field], field.unit))
```

The output is:

```bash
tx_amplifier_power: 20.0 dBW
tx_circuit_loss: 2.0 dB
tx_antenna_gain: 51.6 dBi
eirp: 69.6 dBW
slant_range: 40721000.0 m
free_space_path_loss: 202.7 dB
medium_loss: 10.0 dB
total_path_loss: 212.7 dB
received_isotropic_signal_level: -143.1 dB
rx_antenna_gain: 35.1 dBi
received_power: -110.0 dBW
received_noise_power_density: -192.5 dBW/Hz
rx_system_noise_temperature: 4106.0 K
cno_ratio: 82.4 dB-Hz
snr: 19.4 dB
```

### More examples

You can find more examples as Jupyter notebooks in the docs folder.
[Try them out right now using Binder](https://mybinder.org/v2/gl/librecube%2Flib%2Fpython-linkpredict/master?filepath=docs%2Fexamples).
