module.exports = {
  "extends": "standard",
  "installedESLint": true,
  "plugins": [
    "standard",
    "promise"
  ],
  "globals": {
    "require": true,
  },
  "rules": {
    "no-console": 0,
    "comma-dangle": ["error", "always"],
    "no-multiple-empty-lines": [
        "error",
        {
          "max": 2,
          "maxEOF": 1
        }
      ]
  }
}
