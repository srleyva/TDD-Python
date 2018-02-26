'''The Maintanance API '''
import logging

from flask import Flask

from maintenance_api import v1


class localFlask(Flask):
    def process_response(self, response):
        # Clear out the server line announcing the version info.
        response.headers['server'] = None
        return(response)


app = localFlask(__name__)
app.config['ERROR_404_HELP'] = False
app.config['DATABASE'] = 'db.json'
app.register_blueprint(v1.blueprint)


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)-6s %(message)s')
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    main()
