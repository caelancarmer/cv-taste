# Publication

## Before a release

- Render the reference and inspect its extracted text, PDF metadata, and preview.
- Run the renderer tests.
- Check tracked files for real contact details, biographies, employer documents, credentials, signed URLs, private workspace links, and machine-specific paths.
- Do not add generated candidate documents to release assets.

## Repository visibility

Review commit metadata, branches, tags, releases, and build artifacts before publication. Removing a file does not remove it from earlier Git commits.

Change repository visibility only when authorized. Public repository URLs reveal the owner's GitHub account.

## Versioning

The first public package is `0.0.0`. Increase the patch number for fixes
(`0.0.1`), the minor number for new features or designs (`0.1.0`), and use
`1.0.0` when the supported design and workflow contract is considered stable.
After 1.0.0, incompatible changes increase the major number.

For a release, keep `skill.json`, `CHANGELOG.md`, and the Git tag aligned.
The tag has a `v` prefix, such as `v0.0.0`. The license’s own version number
is independent of the package version. Changes use normal commits and releases;
a new repository is not needed for each version.
