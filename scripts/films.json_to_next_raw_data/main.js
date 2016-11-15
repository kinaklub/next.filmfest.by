const program = require('commander')
const download = require('./download_data')
const privateData = require('./clean_films_json_for_private_data')

const config = require('./config')

program
    .version('1.0.0')

program
    .command('download')
    .alias('d')
    .description('download submissions from filmfest.by')
    .action(function () {
      console.log('start downloadJson')
      download.downloadJson(config).then(function () {
        console.log('end downloadJson')
        console.log('file submission is downloaded!')
      }, function (error) {
        console.log('error', error)
        throw error
      })
    })

program
    .command('clean_private <input> <output>')
    .alias('c')
    .description('remove private data from submissions')
    .action(function (input, output) {
      console.log('start cleaning for ', input)
      const parsedInput = input.split(',')
      privateData.clean(parsedInput, output)
    })


program.parse(process.argv)
