import logging
import sys
import time

from flask import Flask, jsonify, request
from waitress import serve

try:
    from config import APP_CONFIG, REQUIRED_FEATURES, SCHEMA
    from worker import Worker
except ImportError:
    from app.config import APP_CONFIG, REQUIRED_FEATURES, SCHEMA
    from app.worker import Worker


# Setup logging
logger = logging.getLogger("waitress")
debug = APP_CONFIG["DEBUG"]
logger_level = logging.DEBUG if debug else logging.INFO
logging.basicConfig(stream=sys.stdout, level=logger_level, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize servable app
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

# Initialize the worker
worker = Worker()


@app.errorhandler(400)
def bad_request_error_handler(error):
    logger.error(f"{error}\n{request.remote_addr} - {request.method} - {request.path}")
    return jsonify({"error": "400 Bad Request"}), 400


@app.errorhandler(404)
def not_found_error_handler(error):
    logger.error(f'404 Not Found "{request.remote_addr} - {request.method} - {request.path}')
    return jsonify({"error": "404 Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed_error_handler(error):
    logger.error(f'405 Method Not Allowed "{request.remote_addr} - {request.method} - {request.path}')
    return jsonify({"error": "405 Method Not Allowed"}), 405


@app.errorhandler(500)
def server_error_handler(error):
    logger.error(error)
    return jsonify({"error": f"500 Internal Server Error - {str(error)}"}), 500


@app.route("/health", methods=["GET"])
def healthcheck():
    logger.debug("Checking health")

    start_ts = time.time()

    health_body = {
        "gender": "M",
        "age": 32,
        "marital_status": "MAR",
        "job_position": "SPC",
        "credit_sum": 100000,
        "credit_month": 12,
        "tariff_id": "1.6",
        "score_shk": 0.459589,
        "education": "GRD",
        "living_region": "КРАСНОДАРСКИЙ КРАЙ",
        "monthly_income": 45000,
        "credit_count": 2,
        "overdue_credit_count": 0,
    }

    response, error = worker.predict(health_body)

    logger.debug(f"Response:\n{response}")
    logger.debug(f"Error:\t{error}")

    end_ts = time.time()
    execution_time = end_ts - start_ts
    logger.debug(f"Execution time:\t{execution_time}")

    return jsonify({"execution_time": execution_time}), 200


@app.route("/predict", methods=["POST"])
def predict():
    status = 200
    logger.info(f"{request.remote_addr} - {request.method} - {request.path} - {request.args}")
    body_orig = request.json
    logger.debug(body_orig)

    # Check if all required features are present in request
    for feature in REQUIRED_FEATURES:
        if feature not in body_orig.keys():
            error = f"{feature} is required"
            return jsonify({"error": error}), 400

        if body_orig.get(feature) is None:
            error = f"{feature} is required"
            return jsonify({"error": error}), 400

    # Convert request according to schema
    body = {}
    for feature, (typ, default) in SCHEMA.items():
        value = body_orig.get(feature)

        # Set default value if not specified
        if value is None:
            value = default  # Required features are checked before

        # Make type conversion
        try:
            value = typ(value)
        except ValueError:
            error = f"Unable to convert {feature}={value} to {typ} type"
            return jsonify({"error": error}), 400

        body[feature] = value

    response, error = worker.predict(body)

    if error:
        status = 500
        logger.error(f"error: {error}")
        return jsonify({"error": error}), status

    logger.debug(response)
    return jsonify(response), status


if __name__ == "__main__":
    serve(app, host=APP_CONFIG["SERVER_HOST"], port=APP_CONFIG["SERVER_PORT"])
