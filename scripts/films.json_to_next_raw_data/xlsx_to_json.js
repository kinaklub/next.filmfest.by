const xlsxj = require('xlsx-to-json')

xlsxj({
  input: './private/submissions_2014.xlsx',
  output: './result/subm_2014.json',
}, function (err, result) {
  if (err) {
    console.error(err)
  } else {
    console.log(result)
  }
})
