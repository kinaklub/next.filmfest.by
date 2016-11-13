const secret = require('./secret')

module.exports = {
  domain: 'filmfest.by',
  submissions_api_path: 'ru/submission/api/submissions/?format=json',
  user: secret.user,
  pass: secret.pass,
  submission_dir: './private/',
  public_dir: './public/',
}
