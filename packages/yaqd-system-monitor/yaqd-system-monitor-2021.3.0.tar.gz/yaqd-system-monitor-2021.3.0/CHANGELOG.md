# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [2021.3.0]

### Fixed
- added forgotten config options to is-daemon: enable, log_level, and log_to_file
- updated is-sensor trait

## [2020.12.0]

### Added
- conda-forge as installation source

## [2020.07.2]

### Added
- additional trait `pre-measure-trigger`, see [YEP-310](https://yeps.yaq.fyi/310/)

## [2020.07.1]

### Fixed
- Correct version of python supported (>=3.7)
- distribute with `-` instead of `_`

## [2020.07.0]

### Changed
- migrated to Apache [Avro](https://yeps.yaq.fyi/107)

## [2020.05.0]

### Added
- added changelog
- traits
- mypy
- added daemon-level version, see [YEP-105](https://yeps.yaq.fyi/105/)

### Changed
- from now on, yaqd-system-monitor will use date based versioning
- Use daemon level logging, see [YEP-106](https://yeps.yaq.fyi/106)
- refactored gitlab-ci
- updated readme

## [0.1.1]

## Changed
- update README
- fix badge

## [0.1.0]

### Added
- initial release

[Unreleased]: https://gitlab.com/yaq/yaqd-system-monitor/-/compare/v2021.3.0...master
[2021.3.0]: https://gitlab.com/yaq/yaqd-system-monitor/-/compare/v2020.12.0...v2021.3.0
[2020.12.0]: https://gitlab.com/yaq/yaqd-system-monitor/-/compare/v2020.07.2...v2020.12.0
[2020.07.2]: https://gitlab.com/yaq/yaqd-system-monitor/-/compare/v2020.07.1...v2020.07.2
[2020.07.1]: https://gitlab.com/yaq/yaqd-system-monitor/-/compare/v2020.07.0...v2020.07.1
[2020.07.0]: https://gitlab.com/yaq/yaqd-system-monitor/-/compare/v0.1.1...v2020.07.0
[2020.05.0]: https://gitlab.com/yaq/yaqd-system-monitor/-/compare/v0.1.1...v2020.05.0
[0.1.1]: https://gitlab.com/yaq/yaqd-system-monitor/-/compare/v0.1.0...v0.1.1
[0.1.0]: https://gitlab.com/yaq/yaqd-system-monitor/-/tags/v0.1.0
