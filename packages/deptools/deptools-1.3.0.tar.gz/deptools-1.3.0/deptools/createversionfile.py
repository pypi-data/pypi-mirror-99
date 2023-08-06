'''Creates or overwrites a version.txt file in the current working directory
containing the "full version" of the current AlazarTech project. The full
version is a string that respects Semantic Versioning, with the following
scheme:

- for official releases, the version is "X.Y.Z" with X the major, Y the minor
  and Z the patch version number
- for "internal" releases, the version is "X.Y.Z-<pre>" with "X.Y.Z" as before,
  and <pre> a prerelease identifier, for example "1.2.3-beta2".
- otherwise, the version should be "X.Y.Z+<build>" with "X.Y.Z" as before and
  <build> the build identifier, e.g. "1.2.3+34082b74".

Official and internal releases are identified by tags in the ${CI_COMMIT_TAG}
environment variable. Note that these tags have a "v" prefix. Otherwise, the
root of the version number is found by parsing the CHANGELOG.md change log
file, and the SHA of the current commit is found in the ${CI_COMMIT_SHORT_SHA}
environment variable

'''


import os

try:
    from . import changelogparser
except:
    import changelogparser


def get_changelog_version(filename):
    with open(filename, 'r') as clfile:
        changelog = changelogparser.ChangeLogRuleVisitor().parse(clfile.read())
        return changelogparser.version_string(
            changelogparser.changelog_version(changelog))


def main():
    with open("version.txt", "w") as vfile:
        if "CI_COMMIT_TAG" in os.environ:
            tag = os.environ["CI_COMMIT_TAG"]
            vfile.write(tag.lstrip('v') + "\n")
        else:
            if "CI_COMMIT_SHORT_SHA" not in os.environ:
                raise ValueError(
                    "CI_COMMIT_SHORT_SHA environment variable missing")
            version = "{}+{}".format(get_changelog_version("CHANGELOG.md"),
                                     os.environ["CI_COMMIT_SHORT_SHA"])
            vfile.write(version + "\n")


if __name__ == "__main__":
    main()
