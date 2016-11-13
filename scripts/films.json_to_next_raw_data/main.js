const program = require('commander')
const download = require('./download_data')

const config = require('./config')

program
    .version('1.0.0')
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

program.parse(process.argv)
