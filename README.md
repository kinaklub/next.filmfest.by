Our process
-----------

We welcome all contributors and enhancements that help to make
an awesome tool for festival. Feel free to jump in and help with
things to your liking.

* Chat - https://vector.im/beta/#/room/#cpm-dev:matrix.org
* Board of Chaos- https://trello.com/b/6S00yyl1/next-filmfest-by-public
* Meeting Follow Ups (notes, sources for Trello)
  - https://github.com/kinaklub/docs/blob/master/MFU_2016_07_19_filmfest.by.md
  - https://github.com/kinaklub/docs/blob/master/MFU_2016_07_21_filmfest.by.md

[![Travis](https://img.shields.io/travis/kinaklub/next.filmfest.by.svg?maxAge=2592000)](https://travis-ci.org/kinaklub/next.filmfest.by)

Development environment
-----------------------

1. Install [Docker](https://docs.docker.com/) and [docker-compose](https://docs.docker.com/compose/)

2. Don't forget to set DOCKER_HOST environmental variable or add yourself to group `docker`

3. Start web contatiner:

    docker-compose up web

4. DB provisioning (should be performed only once from another terminal):

    docker-compose run web migrate

    docker-compose run web update_index

    docker-compose run web createsuperuser

5. Visit http://127.0.0.1:8000/ in your web browser
