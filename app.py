from flask import Flask, jsonify
import docker

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'



@app.route('/containers')
def get_containers():
    client = docker.from_env()
    containers = client.containers.list()

    container_info = [
        {
            "id": c.short_id,
            "name": c.name,
            "status": c.status,
            "image": c.image.tags
        }
        for c in containers
    ]

    return jsonify(container_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)