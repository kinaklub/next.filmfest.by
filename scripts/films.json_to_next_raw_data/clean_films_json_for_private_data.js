const fs = require('fs')
const fse = require('fs-extra')

// const download = require('./download_data')
// const config = require('./config')


const publicDir = './public/'

const publicFields = [
  'id',
  'title',
  'title_en',
  'country',
  'language',
  'genre',
  'section',
  'synopsis',
  'length',
  'aspect_ratio',
  'year',
  'premiere',
  'film_awards',
  'director_awards',
  'budget',
  'attend',
  'backlink',
  'director',
  'producer',
  'screenwriter',
  'editor',
  'music',
  'director_photography',
  'other_credits',
  'applicant',
  'submission_language',
  'submitted_at',
]

const ensure = new Promise(function (resolve, reject) {
  fse.ensureDir(publicDir, function (err) {
    if (err !== null) {
      console.log(err)
      reject(err)
    } // => null
    // dir has now been created, including the directory it is to be placed in
    resolve()
  })
})

const getSubmissions = new Promise(function (resolve, reject) {
  // download.downloadJson(config),
  const subms = require('./private/submissions')
  resolve(subms)
})

Promise.all([
  getSubmissions,
  ensure,
]).then(function ([ submissions, ]) {
  const cleanSubms = submissions.map(s => {
    var publicSubm = {}

    publicFields.forEach(field => {
      publicSubm[field] = s[field]
    })

    return publicSubm
  })

  fs.writeFile(`${publicDir}/submissions.json`, JSON.stringify(cleanSubms, 0, 4), (err) => {
    if (err) throw err
    console.log('Public submissions are saved!')
  }, function (err) {
    console.log('Error on writing submissions')
    console.log(err)
  })
}, function (err) {
  console.log('error inside all', err)
  throw err
})

