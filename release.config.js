let config = require('semantic-release-preconfigured-conventional-commits')
const buildCmd = `
python - <<EOF
import tomli, tomli_w
from pathlib import Path

path = Path("pyproject.toml")
data = tomli.loads(path.read_text())
data["project"]["version"] = "${nextRelease.version}"
with path.open("wb") as f:
    tomli_w.dump(data, f)
EOF
python -m build
twine check dist/*
`;
config.plugins.push(
  ['@semantic-release/exec', { prepareCmd: buildCmd }],
  ['@semantic-release/github', { assets: ['dist/t2c-${nextRelease.version}.tar.gz', 'dist/t2c-${nextRelease.version}-py3-none-any.whl'] }],
  [
    '@semantic-release/git',
    {
      assets: ['CHANGELOG.md'],
      message: 'chore(release): ${nextRelease.version} [skip ci]',
    },
  ]
);
module.exports = config;
