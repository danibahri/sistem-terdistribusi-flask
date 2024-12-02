from flask import Flask, request, jsonify
from transformers import pipeline
import pika
import json
import threading
import logging
import sys

# Setup Logging
logging.basicConfig(level=logging.INFO)

# Flask app for Master Node
app = Flask(__name__)

# Global Model (Pre-trained Sentiment Analysis)
sentiment_model = pipeline("sentiment-analysis")

# RabbitMQ Configuration
rabbitmq_host = "localhost"
queue_name = "sentiment_tasks"
result_queue = "sentiment_results"

# Shared results list
results = []


@app.route('/distribute', methods=['POST'])
def distribute_tasks():
    data = request.json
    comments = data.get('comments', [])

    if not comments:
        return jsonify({"error": "No comments provided."}), 400

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)

        for comment in comments:
            channel.basic_publish(exchange='',
                                  routing_key=queue_name,
                                  body=json.dumps({"comment": comment}))
            logging.info(f"Task distributed: {comment}")

        connection.close()
        return jsonify({"message": "Tasks distributed successfully."}), 200

    except Exception as e:
        logging.error(f"Error distributing tasks: {str(e)}")
        return jsonify({"error": "Failed to distribute tasks."}), 500

# Result Aggregator (runs in a separate thread)
def consume_results():
    def callback(ch, method, properties, body):
        result = json.loads(body)
        results.append(result)
        logging.info(f"Result received: {result}")

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
        channel = connection.channel()
        channel.queue_declare(queue=result_queue)
        channel.basic_consume(queue=result_queue, on_message_callback=callback, auto_ack=True)
        logging.info("Result Aggregator is running...")
        channel.start_consuming()

    except Exception as e:
        logging.error(f"Error in result aggregation: {str(e)}")
        sys.exit(1)

# Start result consumer in background thread
threading.Thread(target=consume_results, daemon=True).start()

# Endpoint to get the results
@app.route('/results', methods=['GET'])
def get_results():
    return jsonify(results), 200

# Worker Node - Consumes tasks from RabbitMQ queue and processes them
def worker_node():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        channel.queue_declare(queue=result_queue)

        def process_task(ch, method, properties, body):
            task = json.loads(body)
            comment = task['comment']
            sentiment = sentiment_model(comment)[0]
            channel.basic_publish(exchange='',
                                  routing_key=result_queue,
                                  body=json.dumps({"comment": comment, "sentiment": sentiment}))

            logging.info(f"Processed comment: {comment} -> Sentiment: {sentiment}")

        channel.basic_consume(queue=queue_name, on_message_callback=process_task, auto_ack=True)
        logging.info("Worker Node is running...")
        channel.start_consuming()

    except Exception as e:
        logging.error(f"Error in worker node: {str(e)}")
        sys.exit(1)

# Entry point to run either Master or Worker Node
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Distributed Sentiment Analysis")
    parser.add_argument('--mode', choices=['master', 'worker'], required=True, help="Run as master or worker node")
    args = parser.parse_args()

    if args.mode == 'master':
        app.run(host="0.0.0.0", port=5000)
    elif args.mode == 'worker':
        worker_node()
