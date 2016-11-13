const fs = require('fs')

const _ = require('lodash')
const fse = require('fs-extra')
const imageDownloader = require('image-downloader')

const config = require('./config')

// data
let allTranslations = require(`${config.public_dir}translations.json`)
let allSubmissions = require(`${config.public_dir}submissions.json`)

const films2015 = [
  835,
  1875,
  1178,
  1248,
  1248,
  1131,
  1228,
  1585,
  1850,
  1165,
  1407,
  1405,
  1179,
  1159,
  2066,
]

const noTranslationsId = new Set()

const year = '2015'
const ids = films2015
const submissions = allSubmissions.filter((s) => ids.findIndex(tId => tId === s.id) > -1)

const translations = {}
ids.forEach(function (id) {
  translations[id] = allTranslations[id]
})

// fix for incomplete translations
// filter to avoid
const ALL_LANGS = [
  'en',
  'ru',
  'be',
]
Object.keys(translations).forEach(function (id) {
  const t = translations[id]
  const s = submissions.find(s => (s.id === parseInt(id)))

  const langs = _.difference(ALL_LANGS, Object.keys(t))

  if (langs.length > 0) {
    noTranslationsId.add({
      id,
      langs,
    })
    if (langs.includes('en')) {
      t['en'] = {
        language: s.language,
        director: s.director,
        title: s.title_en,
        synopsis: s.synopsis,
        synopsis_short: s.synopsis,
        genre: s.genre,
      }
    }
    const submLang = s['submission_language']
    if (langs.includes(submLang)) {
      t[submLang] = {
        language: s.language,
        director: s.director,
        title: s.title,
        synopsis: s.synopsis,
        synopsis_short: s.synopsis,
        genre: s.genre,
      }
    }
  }
})

const translate = (id, lang, key) => {
  if (!translations[id]) {
    console.log(`no translation for ${id}`)
    return 'no translation'
  }
  const res = translations[id][lang]

  if (!res) throw new Error(`no films in translations ${key}, ${id}, ${lang}`)

  return res[key]
}

const templateNextFilm = {
  film_title_ru: '',
  film_title_en: '',
  film_title_be: '',
  director_ru: '',
  director_en: '',
  director_be: '',
  genre_ru: '',
  genre_en: '',
  genre_by: '',
  synopsis_short_ru: '',
  synopsis_short_en: '',
  synopsis_short_be: '',
  synopsis_ru: '',
  synopsis_en: '',
  synopsis_be: '',
  duration_ru: '',
  duration_en: '',
  duration_be: '',
  city_ru: '',
  city_be: '',
  city_en: '',
  year: 0,
  frame: '',
  id: 0,
}

const IMAGE_DIR = `./result/images`
const saveImage = (id) => {
  fse.ensureDir(`${IMAGE_DIR}/${year}`, function (err) {
    if (err !== null) console.log(err) // => null
    // dir has now been created, including the directory it is to be placed in
    const options = {
      url: `http://filmfest.by/media/screenshots/${id}.jpg`,
      dest: `${IMAGE_DIR}/${year}/`,
      done: function (err, /* filename, image */) {
        if (err) {
          throw err
        }
      },
    }
    imageDownloader(options)
  })
}

function getFilmImage (id) {
  const path = 'images'

  saveImage(id)

  return `${path}/${id}.jpg`
}

const transform = (lang, film) => {
  const trans = translate.bind(null, film.id, lang)

  const nextTitle = trans('title')
  const nextDirector = trans('director')
  // const nextCountry = film.country
  const nextGenre = trans('genre')
  const nextDuration = film.length
  const shortSynopsis = trans('synopsis_short')
  const synopsis = trans('synopsis')

  const city = ''

  _.extend(film, {
    ['film_title_' + lang]: nextTitle,
    ['director_' + lang]: nextDirector,
    ['genre_' + lang]: nextGenre,
    ['duration_' + lang]: nextDuration,
    ['synopsis_' + lang]: synopsis,
    ['synopsis_short_' + lang]: shortSynopsis,
    ['city_' + lang]: city,
    year: film.year,
    frame: getFilmImage(film.id),
  })
}

_(ALL_LANGS)
    .each((lang) => {
      _(submissions).each(transform.bind(null, lang))
    })

const nFilms = _.map(submissions, (film) => {
  return _.pick(film, _.keys(templateNextFilm))
})

// var rawDataDir = `./../../data/raw/cpm${year}/`
fse.ensureDir(`${config.public_dir}`, function (err) {
  if (err !== null) console.log(err) // => null
  // dir has now been created, including the directory it is to be placed in
  fs.writeFile(`${config.public_dir}films_${year}.json`, JSON.stringify(nFilms, 0, 4), (err) => {
    if (err) throw err
    const noLangIds = Array.from(noTranslationsId).filter(e => {
      return ids.includes(parseInt(e.id))
    })
    console.log('no translations: \n', noLangIds)
    console.log('It\'s saved!')
  })
})
