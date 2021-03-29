import time
import redis
from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)
cache = redis.Redis(host='redis-lb', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def get_my_ip():
    return request.remote_addr


@app.route('/')

def hit():
    ip = get_my_ip()
    count = get_hit_count()
    return 'User Address : %s .' %ip + 'Hits: %s .\n'% int(count)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

