
# Change Log - predictr
All notable changes to this project will be documented in this file.

## [0.1.19] - 2021-03-23
 
### Changed
 - Removed set_cmaps argument in PlotAll. You can now customize the colors for each PlotAll method individually using the color argument.
 - Improved consistency of method arguments throughout code: fontsizes, nomenclature etc.

### Added
 - PlotAll methods can plot median rank markers
 - Possibility to save plots for all methods

### Fixed
 - Fixed bug that resulted in empty saved plots

## [0.1.18] - 2021-03-17
 
### Fixed
 - fig_size didn't work in mult_weibull() due to a bug in the code

## [0.1.17] - 2021-03-13
 
### Added
 - Better documentation in the code

### Change
 - Minor changes to have more consistent nomenclature in the code

## [0.1.16] - 2021-03-03
 
### Fixed
 - fixed last bug in the median rank computation. Bug occured when multiple failure times were identical

### Added
 - PlotAll().simple_weibull(): Plots Weibull probability plot according to input (Weibull parameters) without calculations
 - PlotAll().weibull_pdf: Plots one or more Weibull probability density functions with fully customizable figure attributes (color, labels, width, height, fontsize etc.)
 - Added ability to customize axis labels, title, fontsize etc for Analysis() and PlotAll
 - Added ability to hide legend in Weibull plot

## [0.1.15] - 2021-02-27
 
### Fixed
 - fixed wrong percentile values for adjusted ranks when suspenions have lower time to failure values than actual failures
 - permanent fix for the disappearing Weibull probability line (see changelog for version 0.1.14)

### Added
 - raise ValueError when np_bs and p_bs bias-correction methods are applied to data that has suspensions

## [0.1.14] - 2021-02-16
 
### Fixed
 - temporary fix for instances in Analysis where the Weibull probability line disappears when two-sided bounds are used
 
## [0.1.13] - 2021-01-23
 
### Fixed
 - hrbu was misspelled in the code and raised an error when calling this bias-correction method

## [0.1.12] - 2021-01-14
 
### Added
 - contour_plot() method in PlotAll class: Plots likelihood ratio contours for Analysis class instances

## [0.1.11] - 2021-01-01
 
### Fixed
 - When using npbb and pbb as bounds, bounds types 1sl and 1su would return the same bounds limits. Fixed the percentile method.

## [0.1.10] - 2021-01-01
 
### Fixed
 - Minor fix and code restructuring

## [0.1.9] - 2021-01-01
 
### Added
 - new GithubPage: https://tvtoglu.github.io/predictr/
 - new Class: PlotAll -> plot multiple Weibull plots in one figure

## [0.1.7] - 2020-12-29
  
### Changed
 - changed get_bx_percentile() to a classmethod

## [0.1.6] - 2020-12-29
 
### Added
- Official changelog
- New static method get_bx_percentile() for Analysis class. You can now get the time values for given BX-lives

### Changed
  
- Argument "bounds" for Fisher bounds: 'fisher' -> 'fb'. This is more in line with the other confidence bounds
