const fs = require('fs')
const fse = require('fs-extra');
const http = require('http');
const path = require('path');

const downloadJson = (config) => {
    const promise = new Promise(function (resolve, reject) {
        http.get({

            host: config.domain,
            path: config.submissions_api_path,
            auth: `${config.user}:${config.pass}`
        }, (res) => {
            const statusCode = res.statusCode;
            const contentType = res.headers['content-type'];

            let error;
            if (statusCode !== 200) {
                error = new Error(`Request Failed.\n` +
                    `Status Code: ${statusCode}`);
            } else if (!/^application\/json/.test(contentType)) {
                error = new Error(`Invalid content-type.\n` +
                    `Expected application/json but received ${contentType}`);
            }
            if (error) {
                console.log(error);
                // consume response data to free up memory
                res.resume();
                return;
            }

            const file = path.join(config.submission_dir, 'submissions.json');
            const stream = fs.createWriteStream(file);
            stream.cork();

            res.on('data', function (chunk) {
                stream.write(chunk)
            });
            res.on('end', function () {
                stream.uncork();
                stream.end();

                resolve(fs.readdirSync(SUBMISSIONS_DIR))
            });
        }).on('error', (e) => {
            console.log(`Got error: ${e.message}`, e);
            throw e
        })
    });

    return promise;
};

module.exports = {
    downloadJson
}
