Development environment
-----------------------

1. Install [Docker](https://docs.docker.com/) and [docker-compose](https://docs.docker.com/compose/)

2. Don't forget to set DOCKER_HOST environmental variable or add yourself to group `docker`

3. Start web contatiner:

    docker-compose up web

4. DB provisioning (should be performed only once from another terminal):

    docker-compose run web syncdb --noinput

    docker-compose run web migrate

    docker-compose run web loaddata data.json

5. Visit http://127.0.0.1:8000/ in your web browser
