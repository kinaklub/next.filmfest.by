const fs = require('fs')
const path = require('path')

var Curl = require('node-libcurl').Curl

const curl = new Curl()

const downloadJson = (config) => {
  const promise = new Promise(function (resolve, reject) {
    const file = path.join(config.submission_dir, 'submissions.json')
    const stream = fs.createWriteStream(file)

    stream.cork()

    curl.setOpt(Curl.option.URL, `${config.domain}/${config.submissions_api_path}`)
    curl.setOpt(Curl.option.USERNAME, `${config.user}`)
    curl.setOpt(Curl.option.PASSWORD, `${config.pass}`)

    curl.on('data', function (chunk) {
      stream.write(chunk)
    })


    curl.on('end', function () {
      stream.uncork()
      stream.end()
      curl.close()

      resolve(fs.readFileSync(`${config.submission_dir}submissions.json`))
    })
    curl.on('error', function (err) {
      curl.close()
      stream.uncork()
      stream.end()
      console.log('error on curl', err)
    })
    curl.perform()
  })

  return promise
}

module.exports = {
  downloadJson,
}
