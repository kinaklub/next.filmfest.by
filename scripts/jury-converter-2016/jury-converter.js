#!/usr/bin/env node
'use strict';

/*
The script converts jury from 2106 json format to new json format.
Authors:
 * Eugene Petkevich / http://eugene.zuelum.org
*/

var ArgumentParser = require('argparse').ArgumentParser;
var fs = require('fs');

var pjson = require('./package.json');

// Make CLI arguments and help.
var parser = new ArgumentParser({
  version: pjson.version,
  addHelp:true,
  description: 'Convert Jury values from old to new json format'
});
parser.addArgument(
  [ '-i', '--input' ],
  {
    help: 'directory with source json-files',
    defaultValue: '.'
  }
);
parser.addArgument(
  [ '-o', '--output' ],
  {
    help: 'directory for output of new json and related files',
    defaultValue: './new'
  }
);
var args = parser.parseArgs();

// Make a list of input files.
var filelist = fs.readdirSync(args.input)
var inputFiles = filelist.filter(isJsonFile);

// Parse json files, reformat and unite.
var finalData = [];
for (var i = 0; i < inputFiles.length; ++i) {
  var data = JSON.parse(fs.readFileSync(args.input+'/'+inputFiles[i], 'utf8'));
  var members = data.members;
  for (var key in members) {
    var photo_filename = members[key].photo;
    var new_member = {
      title: key,
      name_en: members[key].en.name,
      name_be: members[key].be.name,
      name_ru: members[key].ru.name,
      info_en: members[key].en.full_info,
      info_be: members[key].be.full_info,
      info_ru: members[key].ru.full_info,
      short_info_en: members[key].en.short_info,
      short_info_be: members[key].be.short_info,
      short_info_ru: members[key].ru.short_info,
      coutry: '@@@',
      photo_ext: photo_filename.substr(photo_filename.lastIndexOf('.')+1),
      photo: photo_filename
    };
    finalData.push(new_member);
  }
}
console.log('Please update "country" fields in the resulting JSON file.  Also check the result for missing fields.  And copy photos manually.')

// Save the result in the file.
fs.writeFileSync(args.output+'/'+'jury.json', JSON.stringify(finalData, null, 2));

//======================================

function isJsonFile(filename) {
  return filename.endsWith('.json');
}
