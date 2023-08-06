# bdata 

<a href="https://pypi.org/project/bdata/" alt="PyPI Version"><img src="https://img.shields.io/pypi/v/bdata?label=PyPI%20Version"/></a>
<img src="https://img.shields.io/pypi/format/bdata?label=PyPI%20Format"/>
<img src="https://img.shields.io/github/languages/code-size/dfujim/bdata"/>
<img src="https://img.shields.io/tokei/lines/github/dfujim/bdata"/>
<img src="https://img.shields.io/pypi/l/bdata"/>

<a href="https://github.com/dfujim/bdata/commits/master" alt="Commits"><img src="https://img.shields.io/github/commits-since/dfujim/bdata/latest/master"/></a>
<a href="https://github.com/dfujim/bdata/commits/master" alt="Commits"><img src="https://img.shields.io/github/last-commit/dfujim/bdata"/></a>

[bdata] is a lightwieght [Python] package aimed to aid in the analysis of β-detected
nuclear magnetic/quadrupole resonance (β-NMR and β-NQR) data taken at [TRIUMF]. 
These techniques are similar to muon spin rotation ([μSR]) and "conventional"
nuclear magnetic resonance ([NMR]), but use radioactive nuclei as their [NMR]
probe in place of the [muon] or a stable isotope.

The intended user of [bdata] is anyone analyzing data taken from [TRIUMF]'s β-NMR or β-NQR spectrometers.
A key goal of the project is to alleviate much of the technical tedium that is
often encountered during any analysis.

Used with [bfit] and the [SciPy] ecosystem, [bdata] forms part of a flexible API
in the analysis of β-NMR and β-NQR data. [bdata] has been written to fullfill the following needs: 

* Provide an intuitive means of interfacing with [MUD] files in [Python].
* Fetch missing local data from the [archive]. 
* Support analyses by providing common data manipulations, such as calculating 
asymmetries or combining scans. 

## [Contents](https://github.com/dfujim/bdata/wiki)

* [`bdata`](https://github.com/dfujim/bdata/wiki/bdata) [object]: access β-NMR and β-NQR [MUD] files
* [`bjoined`](https://github.com/dfujim/bdata/wiki/bjoined) [object]: append `bdata` objects
* [`bmerged`](https://github.com/dfujim/bdata/wiki/bmerged) [object]: combine `bdata` objects
* [`life`](https://github.com/dfujim/bdata/wiki/life) [`mdict` object]: dictionary of probe lifetimes. 
* [`containers`](https://github.com/dfujim/bdata/wiki/containers) [module]: specially defined `mdict` objects with set function. 

## Citing

If you use [mudpy], [bdata], or [bfit] in your work, please cite:

- D. Fujimoto.
  <i>Digging into MUD with Python: mudpy, bdata, and bfit</i>.
  <a href="https://arxiv.org/abs/2004.10395">
  arXiv:2004.10395 [physics.data-an]</a>.

## Community Guidelines

* Please submit contributions to [bdata] via a pull request
* To report issues or get support, please file a new issue

## Installation and Use

### Dependencies

The following packages/applications are needed prior to [bdata] installation:
- [Python] 3.6 or higher: a dynamically typed programming language. [[install](https://wiki.python.org/moin/BeginnersGuide/Download)]
- [Cython] : [C]-language extensions for [Python]. [[install](https://cython.readthedocs.io/en/latest/src/quickstart/install.html)]
- [NumPy] : array programming library for [Python]. [[install](https://numpy.org/install/)]


and the following are handelled automatically when retrieving [bdata] from the [PyPI]:

- [iminuit] : a [Jupyter]-friendly [Python] interface for the [MINUIT2] library.
- [mudpy] : data structures for parsing [TRIUMF] [MUD] files.
- [pandas] : a fast, powerful, flexible and easy to use data analysis/manipulation tool.
- [requests] : an elegant and simple [HTTP] library for [Python].


### Install Instructions

|  | Command |
|:-- | :--|
From the [PyPI] as user (recommended) | `pip install --user bdata` |
From the [PyPI] as root | `pip install bdata` |
From source | `python3 setup.py install` |

Note that `pip` should point to a (version 3) [Python] executable
(e.g., `python3`, `python3.8`, etc.).
If the above does not work, try using `pip3` or `python3 -m pip` instead.

### Optional Configuration

For convenience,
you may want to tell [bdata] where the data is stored on your machine.
This is done by defining two environment variables:
`BNMR_ARCHIVE` and `BNQR_ARCHIVE`.
This can be done, for example, in your `.bashrc` script.
Both variables expect the data to be stored in directories with a particular
heirarchy:

```
/path/
    bnmr/
    bnqr/
        2017/
        2018/
            045123.msr
```

Here, the folders `/path/bnmr/` and `/path/bnqr/` both contain runs
(i.e., `.msr` files) organized into subdirectories by year of aquasition.
In this case, you would set (in your `.bashrc`):

```bash
export BNMR_ARCHIVE=/path/bnmr/
export BNQR_ARCHIVE=/path/bnqr/
```

If [bdata] cannot find the data, it will attempt to download the relavent [MUD] files 
from the [archive] and store them in `$HOME/.bdata`.
This is the default behaviour for [bdata] installed from [PyPI]
   

[Python]: https://www.python.org/
[SciPy]: https://www.scipy.org/
[Cython]: https://cython.org/
[NumPy]: https://numpy.org/
[pandas]: https://pandas.pydata.org/
[Matplotlib]: https://matplotlib.org/
[requests]: https://requests.readthedocs.io/en/master/
[Jupyter]: https://jupyter.org/

[YAML]: https://yaml.org/
[C]: https://en.wikipedia.org/wiki/C_(programming_language)
[HTTP]: https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol

[TRIUMF]: https://www.triumf.ca/
[CMMS]: https://cmms.triumf.ca
[MUD]: https://cmms.triumf.ca/mud/
[archive]: https://cmms.triumf.ca/mud/runSel.html

[UBC]: https://www.ubc.ca/
[μSR]: https://en.wikipedia.org/wiki/Muon_spin_spectroscopy
[NMR]: https://en.wikipedia.org/wiki/Nuclear_magnetic_resonance
[muon]: https://en.wikipedia.org/wiki/Muon

[PyPI]: https://pypi.org/project/bdata/
[mudpy]: https://github.com/dfujim/mudpy
[bdata]: https://github.com/dfujim/bdata
[bfit]: https://github.com/dfujim/bfit

[iminuit]: https://github.com/scikit-hep/iminuit
[MINUIT2]: https://root.cern/doc/master/Minuit2Page.html
