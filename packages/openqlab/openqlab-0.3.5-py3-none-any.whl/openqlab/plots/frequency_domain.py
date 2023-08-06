"""Plotting scripts in frequency domain."""
from typing import Optional
from warnings import warn

import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from openqlab import analysis

from ..conversion import db
from ..io import DataContainer


def _clamp_phase(phase):
    """Return phase with all values mapped to between +/- 180 degrees."""
    warn(
        "DEPRECATED: _clamp_phase is deprecated, \
            use openqlab.analysis.phase.clamp_phase.",
        DeprecationWarning,
    )
    return analysis.phase.clamp_phase(phase)


def amplitude_phase(
    amplitude,
    phase,
    logf=True,
    bodeplot=True,
    clamp_phase=True,
    dbunits=True,
    title="Transfer Function",
    **kwargs
):
    """
    Create an amplitude-phase plot to display transfer function measurements.

    Parameters
    ----------
    amplitude: :obj:`DataFrame`
        A Pandas :obj:`DataFrame` containing the frequency-domain
        amplitude data (in dB).
    phase: :obj:`DataFrame`
        A Pandas :obj:`DataFrame` containing the frequency-domain
        phase data (in degrees).
    logf: :obj:`bool`
        Use logarithmic frequency axis.
    bodeplot: :obj:`bool`
        Use Bode plot style (magnitude and phase in separate plots).
    clamp_phase: :obj:`bool`
        Map phase values to +/- 180deg.
    dbunits: :obj:`bool`
        Use dB units for display. Otherwise convert to linear units.
    title: :obj:`str`, optional
        The figure title.
    **kwargs:
        Parameters are passed to the :obj:`pandas.DataFrame.plot` method

    Returns
    -------
    :obj:`matplotlib.figure.Figure`
        A handle to the created matplotlib figure.

    """
    if bodeplot:
        fig, (ax, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 8))
    else:
        fig, ax = plt.subplots()
        ax2 = ax.twinx()

    if dbunits:
        ampl = amplitude
    else:
        ampl: DataContainer = db.to_lin(
            amplitude / 2.0
        )  # the /2.0 accounts for power/amplitude

    ampl.plot(ax=ax, title=title, legend=False, logx=logf, logy=(not dbunits), **kwargs)
    if not bodeplot:
        for _ in range(len(ax.lines) + 1):
            # HACKHACK: advance color cycler so we get continuous colours across
            #          the two plots. May break in future versions of matplotlib.
            next(ax2._get_lines.prop_cycler)

    if clamp_phase:
        phase = analysis.phase.clamp_phase(phase)
    phase.plot(ax=ax2, legend=False, logx=logf)
    ax.set_ylabel("Amplitude (dB)")
    ax2.set_ylabel(u"Phase (º)")
    ax2.grid(linestyle="--")
    ax.grid()

    return fig


def power_spectrum(
    data,
    normalize_to=None,
    logf=True,
    title="Power Spectrum",
    ax: Optional[Axes] = None,
):
    """
    Create a plot for power spectrum data (in dB units), e.g. squeezing measurements over a frequency range.

    Note that this function only does the plotting, it does not calculate
    the power spectrum by itself.

    Parameters
    ----------
    data: :obj:`DataFrame`
        A Pandas :obj:`DataFrame` containing the frequency-domain
        power spectrum data (in dBm).
    normalize_to: :obj:`DataFrame` or :obj:`float`, optional
        Normalize all data columns by this value.
    logf: :obj:`bool`, optional
        Use logarithmic frequency axis.
    title: :obj:`str`, optional
        The figure title.
    ax (Axes, optional):
        Provide an Axes for advanced figures.

    Returns
    -------
    :obj:`matplotlib.figure.Figure`
        A handle to the created matplotlib figure.

    """
    if ax is None:
        _, ax = plt.subplots()

    if normalize_to is not None:
        my_data = data.subtract(normalize_to, axis="index")
        ylabel = "Relative Power (db)"
    else:
        my_data = data
        ylabel = "Power (dBm)"
    my_data.plot(ax=ax, title=title, legend=True, logx=logf)

    ax.set_ylabel(ylabel)
    ax.grid(which="both")

    return ax.figure


def relative_input_noise(
    data: DataContainer,
    volt_dc: float,
    logf: bool = True,
    logy: bool = True,
    title: Optional[str] = None,
    ylabel: str = r"RIN ($1/\sqrt{\mathrm{Hz}}$)",
    **kwargs
) -> Axes:
    """Create a plot for relative input noise.

    The values of data are devided by the constant voltage :obj:`volt_dc`
    and plottet using the :obj:`DataContainer.plot` method.

    Parameters
    ----------
    data: :obj:`DataContainer`
        input data
    volt_dc: bool
        dc voltage for reference
    logf: bool
        frequency log scale
    logy: bool
        y axis log scale

    Returns
    -------
    :obj:`matplotlib.axes.Axes`
        Axes object
    """
    data /= volt_dc  # type: ignore
    plot = data.plot(logx=logf, logy=logy, title=title, **kwargs)
    plot.grid(which="both")
    plot.set_ylabel(ylabel)
    plot.set_xlabel("Frequency (Hz)")

    return plot
