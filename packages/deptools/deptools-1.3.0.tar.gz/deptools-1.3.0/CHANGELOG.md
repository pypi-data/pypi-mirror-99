# AlazarTech Deployment Tools Change Log

This file contains all important changes to the AlazarTech deployment tools

## [1.3.0] - 2020-03-24
### Added
- createversionfile script. [#28]

## [1.2.2] - 2020-03-23
### Fixed
- Issue that prevented the release of v1.2.1

## [1.2.1] - 2020-03-23
### Fixed
- Issue that prevented the release of v1.2.0

## [1.2.0] - 2020-03-22
### Added
- run-clang-format tool

## [1.1.1] - 2020-11-24
### Fixed
- Remove debugging statements

## [1.1.0] - 2020-11-23
### Added
- Full support for SemVer 2.0.0 version numbers in change logs. [#25]
- Add `-o` option to `changelogparser version`. [#26]

## [1.0.1] - 2020-11-03
### Fixed
- Issue with v1.0.0 release, where deploy failed because of the missing Azure
  python dependency. [#24]

## [1.0.0] - 2020-10-27
### Added
- Support for artifacts upload on Azure blob storage used by
  alazar-package-manager [#23]

## [0.4.2] - 2020-09-02
### Fixed
- Issue with v0.4.1 release, where the package couldn't be installed from PyPI
  [#22]

## [0.4.1] - 2020-05-19
### Changed
- Use new code signing certificate

## [0.4.0] - 2020-05-07
### Added
- Support for ticket references in change log items [#19]

### Fixed
- Issue where H3 tags are not closed properly in changelogparser's HTML output

## [0.3.4] - 2019-10-03
### Fixed
- Issue where deploy did not work correctly with Python 2

## [0.3.3] - 2019-09-27
### Added
- Support for Markdown output
- Support for Python 2.7

## [0.3.2] - 2019-07-23
### Fixed
- Spec file build issue when version log is empty

## [0.3.1] - 2019-07-23
### Fixed
- Build issues when version log is empty

## [0.3.0] - 2019-05-06
### Added
- deploy: split "encrypt" into "compress" and "encrypt". This adds support for
  creating non-password protected ZIP files [#10].
- deploy: add "destdir" option [#11].

### Fixed
- Build issues by using a "version.txt" file for this package

## [0.2.0] - 2019-05-02
### Added
- Support for [YANKED] tag in change log files [#4]
- Add option to publish only encrypted files, and option to read password from
  file. [#6]
- Support publishing to FTP sites [#5]
- Add "tospec" to changelogparser [#8]
- Deploy to AlazarTech's PyPI server [#9]

### Changed
- Make encrypt's default value "no" in deploy.py [#7]

## [0.1.0] - 2019-03-20
### Added
- Change log parser utility [#3]

## [0.0.2] - 2019-01-25
### Fixed
- Make directory copy work even if destination already exists

## [0.0.1] - 2019-01-23
### Added
- Initial version: deploy.py [#1]
