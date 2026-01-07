# https://ddtrace.readthedocs.io/en/stable/integrations.html#flask
import logging
import os
import socket
import sys

import json_log_formatter
from flask import Flask, jsonify, request

# Sets logs to JSON format when running in a container
root = logging.getLogger()
if os.environ.get('DD_AGENT_HOST') is not None:
    json_handler = logging.StreamHandler(sys.stdout)
    json_handler.setFormatter(json_log_formatter.JSONFormatter())

    root.handlers.clear()
    root.addHandler(json_handler)

logger = logging.getLogger('app-python')
logger.setLevel(logging.INFO)

app = Flask(__name__)

@app.route('/health')
def hello():
    return '', 204

@app.route('/env/<env_var>')
def get_env_var(env_var):
    value = os.environ.get(env_var)
    if value is None:
        return jsonify({'error': f'Environment variable {env_var} not found'}), 404
    return jsonify({'variable': env_var, 'value': value})

@app.route('/info')
def get_info():
    return jsonify({
        'pod_name': os.environ.get('HOSTNAME', 'unknown'),
        'client_ip': request.remote_addr
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
