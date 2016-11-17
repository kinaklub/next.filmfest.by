# scripts for filmfest.by

Here we aggregate scripts which help to process Cinema Perpetuum Modile festival data for new website
 
# scripts list

* jsoncheck.py - python script to check json in /data folder
* jury-converter-2016/jury-converter.js - nodejs script to convert manually crafted json for jury member of 2016 to migration suitable format
* scripts/films.json_to_next_raw_data/submission_download.js - used to download submission.json from website and later usage
* scripts/films.json_to_next_raw_data/submission_filter.js - clean from submissions.json all private data ( email, address, phone number )
* scripts/films.json_to_next_raw_data/submission_process.js - convert submissions by their id using translation.json for migrate suitable format
 
# usage
 
* for node you need to have nodejs v.7 and higher

## scripts/films.json_to_next_raw_data/

`> npm install`

### submission_filter.js

` > node main.js d` 

### submission_filter.js

` > node clean_films_json_for_private_data.js`

### submission_process.js

`> node next_films.js`
  
Also you can change ids inside script itself assign another array of ids 

`const ids = films2015`
