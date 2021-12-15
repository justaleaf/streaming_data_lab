import json
import argparse

from datetime import datetime
from os.path import join
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

parser = argparse.ArgumentParser(description='github_events')
parser.add_argument('--host', type=str, default='localhost')
parser.add_argument('--port', type=int, default=9999)
parser.add_argument('--rate', type=float, default=1.0)

args = parser.parse_args()

# type, user.id, user.bot
base_path = join('data', 'sim', f'rate_{args.rate}')
continuous_log = join(base_path, 'real', 'log')
window_events_log = join(base_path, 'window_events', 'log')
window_pr_log = join(base_path, 'pr', 'log')

# data = list(map(lambda x: json.loads(x.strip()).get('created_at'), data))
if __name__ == "__main__":
    sc = SparkContext(appName="DataProcessing")
    sc.setLogLevel('ERROR')
    streaming_sc = StreamingContext(sc, 1)
    streaming_sc.checkpoint('checkpoint')

    lines = streaming_sc.socketTextStream(args.host, args.port)
    json_stream = lines.flatMap(lambda data: data.splitlines()).map(json.loads)
    data_stream = json_stream \
        .map(lambda x: (x.get('type'), x.get('actor').get('login')))

    pr_window_stream = json_stream \
        .filter(lambda x: x.get('type') == 'PullRequestReviewCommentEvent') \
        .map(lambda x: (x.get('actor').get('login'), len(x.get('payload').get('pull_request').get('requested_reviewers', [])))) \
        .window(20, 20) \
        .repartition(1)

    windowed_data = data_stream \
        .countByValueAndWindow(10, 10) \
        .repartition(1)

    data_stream.saveAsTextFiles(continuous_log)
    windowed_data.saveAsTextFiles(window_events_log)
    pr_window_stream.saveAsTextFiles(window_pr_log)

    streaming_sc.start()
    streaming_sc.awaitTermination()
