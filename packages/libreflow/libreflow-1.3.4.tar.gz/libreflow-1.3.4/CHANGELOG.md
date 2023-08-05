# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)[^1].

<!---
Types of changes

- Added for new features.
- Changed for changes in existing functionality.
- Deprecated for soon-to-be removed features.
- Removed for now removed features.
- Fixed for any bug fixes.
- Security in case of vulnerabilities.

-->

## [Unreleased]

## [1.3.4] - 2021-03-18

### Changed

* Publish action has been made injectable.
* Some improvements on advanced action dialogs have been made (message content, reset of file reference).

## [1.3.3] - 2021-03-16

### Added

* Action for requesting file revisions now displays a list of found oids given a wildcard-based oid pattern (** not supported).
* Using *[last]* keyword in the pattern allows to get the latest published revision of a file. For instance, according to how the base flow is currently designed, `/project/sequences/*/shots/*/departments/*/files/*/history/revisions/[last]` allows to retrieve the latest publications of all files of the project named `project`.

## [1.3.2] - 2021-03-15

### Fixed

* Action for requesting file revisions does not stop anymore when it falls onto a revision already available on requesting site, or not available on requested site.
* Current user is stored when profile has not already been registered.

### Changed

* Actions on tracked files have been refined and reorganised.

## Added

* Two new actions on tracked files allow respectively:
  - to publish changes made in a file into another file
  - to create a working copy on a file from a selected revision of another file
* Users can now publish their changes made to a file from their working copy in the revision history.

## [1.3.1] - 2021-03-10

### Changed

* project settings are now injectable

## [1.3.0] - 2021-03-10

### Added

* File maps now display tracked element latest revisions and their availability. These can be requested directly from the file map.

### Changed

* Site definitions have been updated to distinguish working and exchange sites. 
* Exchange server configuration is held by the project's exchange site.
* A working site's job queue can be accessed by right-clicking on its entry in the site map.
* Default exchange site has been renamed as *default_site*, to be distinguished from default working site.

### Fixed

* Job emission date is stored as a floating point timestamp (not a formatted date string anymore) to be easily processed.
* Corrections on file list UI for untracked items.
* Publication option is not available anymore when rendering a playblast on a Blender file if the user hasn't a working copy on this file. This fixes an error which causes the resulting publication to be empty.

## [1.2.8] - 2021-03-10

### Fixed

* Logout from project has been fixed.

## [1.2.7] - 2021-03-09

### Fixed

* Subprocess environments are updated with the current site's root path. In particular, this makes root path, required in scene builder, accessible in Blender environment whenever a Blender scene is opened from Libreflow.

### Added

* Subprocess extra environments also include the current user name and contextual settings.

## [1.2.6] - 2021-03-05

### Fixed

* Added FBX file format in PyPI package data to make FBX template available.

## [1.2.5] - 2021-03-01

* Omitted in 1.2.4: *script* folder made as a valid Python package.

## [1.2.4] - 2021-03-01

### Added

* An action to batch revisions request as another site (currently not publicly available).

### Changed

* A new Blender template file.

### Fixed

* *script* folder made as a valid Python package.
* Project object is systematically touched when accessed from a home page widget to ensure user environment update.

## [1.2.3] - 2021-02-15

### Added

MP4, Illustrator and FBX file formats support

### Changed

* Actions to render a Blender file playblast is available in the base flow. Moreover, rendering a revision playblast generate a revision of the same index in a .mov tracked file.  
* Map clearing action relations have been removed to prevent unfortunate deletions.  
* Folder hierarchy in which user settings are stored has been changed to *<user_folder>/.libreflow/<project_name>/<user_name>/<user_settings>.*. This allows:  
  - a single user to be part of multiple projects
  - multiple users to authenticate on a project on the same workstation.
* Revisions display the time elapsed since their publication

## [1.2.2] - 2021-02-09

### Fixed

- Change *Request* action allowing context condition

## [1.2.1] - 2021-02-09

### Changed

- User name is now computed from Kitsu ID at first connection
- Files and folders of any type can be revealed in file explorer

## [1.2.0] - 2021-02-08

### Changed

- Bookmarks have been changed from a local json file to a dedicated map on the project's flow. #12
- File extensions and icons are now constants
- Revisions and TrackedFiles are now injectable
- A site can now request file revisions for other sites, if authorized (*request_files_from_anywhere* BoolParam).

### Added

- The project thumbnail flow can now be saved within the project admin/project settings area. So the thumbnail is available from anywhere no matter the site or OS. The old system is still present. #13

### Deprecated
- The old system for the thumbnail will soon be removed.

### Fixed
- At publish of a trackedFolder on python 3.7 an error appears because of a 3.8 update of stdlib shutil. Made a dirty fix for that.

## [1.1.7] - 2021-02-04

### Added

Users can log out from the project, sending them back to the login page.

### Fixed

User Kitsu id and the one used in the flow are distinguished, in order to ensure users are identified with a unique flow id which matches the pattern of a valid Python attribute, as required by Kabaret features. This currently implies users working on the project to be registered in this map.

## [1.1.6] - 2021-02-01

### Fixed

File data formats have been added in *setup.py* to make template files available within PyPI package.
Unforgivable hard-coded paths of several scripts have been changed for relative ones.

## [1.1.5] - 2021-01-29

### Fixed

Fix revision playblast rendering: Get playblast folder path from *Computed* department path.

## [1.1.4] - 2021-01-29

### Fixed

Fix revision upload: *Revision.get_relative_path()* gets parent file Computed path, instead of wrongly accessing *get_contextual_dict*.

## [1.1.3] - 2021-01-29

### Fixed

Until now, the computation of *File* and *Revision* paths implied implying a costly non-linear look-up of contextual edits, and long wait for maps to display. There is now only one contextual settings look-up to compute a *Department* path, from which department's file paths are computed and cached.

## [1.1.2] - 2021-01-21

### Fixed

User environment map items are now *SessionValue*s to make environment variable values stored at session's scope.

## [1.1.1] - 2021-01-20

### Fixed

MinIO and timeago added in setuptools requirements.

## [1.1.0] - 2021-01-20

*Multisite v1 release*

### Added 

- A ComputedParam named `root_dir` is now available in admin and it's cached as requiered by issue #4. A function `get_root()` at the Project level use it and is able to provide the root folder of the project according to the operative system. Call it from anywhere in the flow with `self.root().project().get_root()`.
- `CHANGELOG.md`, `LICENCE` and `AUTORS` files have been added to the repo
- **Multi-site** file synchronization features (related to issue #5):
  - Add and configure project's sites (type - studio, user or exchange -, per-OS root directories, exchange server properties)
  - Request tracked file's revisions unavailable on current site for download, based on a job submission feature
  - A `SynchronizeFile` action allow users to process files they requested, and files other sites requested from theirs. This currently uses a MinIO client.
  - Retrieve the current site and exchange site in the flow with `self.root().project().[get_current_site()|get_exchange_site()]`
  - UI improvement: revision history maps can toggle site sync statuses
- Runners redirect their logs in a file placed in the user folder (bce8aadf)
- A new `DefaultRunner` is available to let the OS choose the default application for a given file path.
- Previews and renders of AfterEffects file revisions can be launched at revision and episode level, given AfterEffectsRender render settings and output module templates
- Playblasts of blender file revisions can be made with an action (*preview* folder created in department's files if not already added)
- Md5 hash is computed for publishes for later features (cc0478e8)

### Changed

- According to the new `get_root()` function added and requiered by issue #4, the default contextual dict doens't provide a `ROOT_DIR` value anymore. Calls to that value have been changed, and you must define `ROOT_DIR_WINDOWS`, `ROOT_DIR_LINUX` and/or `ROOT_DIR_MAC` in the admin panel.
- Cosmetic changes to get some maps expanded or not (832605d8).
- There is no need to manually specify the user folder anymore: project's `get_user_folder()` method now returns the path to a `.libreflow` in the user's home directory.
- For sake of readability, file maps showcase the time elapsed since file last modification, instead of date (59d364a8).

## [1.0.3] - 2020-12-24

### Fixed

issue #7 libreflow icons are missing from the distributed package (and also the example packages where not accessible)

## [1.0.2-1.0.1] - 2020-12-23

Initial public commit and pypi setup. This version is an early version of libreflow. It includes a baseflow and examples flows overriding the baseflow. We have been working on departments, files, file version history, and stuff like that.

### Fixed

issue #6 : Pip Package is now ready for use


[^1]: Except we started libreflow MAJOR version number at 1, as we consider our in-house previous flow being version 0.