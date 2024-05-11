from flask import Flask, request, request, render_template
from predict import predict_sentiments
from youtube import get_video_comments
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

def get_video(video_id):
    if not video_id:
        return {"error": "video_id is required"}

    comments = get_video_comments(video_id)
    print(f'>>>>>>>>>>>>>>>VIDEO COMMENTS<<<<<<<<<<<<<<>>> {comments}')
    predictions = predict_sentiments(comments)

    positive = predictions.count("Positive")
    negative = predictions.count("Negative")

    summary = {
        "positive": positive,
        "negative": negative,
        "num_comments": len(comments),
        "rating": (positive / len(comments)) * 100
    }

    return {"predictions": predictions, "comments": comments, "summary": summary}

#####################################ORIGINAL###############################################################
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     summary = None
#     comments = []
#     if request.method == 'POST':
#         video_url = request.form.get('video_url')
#         video_id = video_url.split("v=")[1]
#         print(f'>>>>>>>>>>>>>>>VIDEO ID<<<<<<<<<<<<<<>>> {video_id}')
#         data = get_video(video_id)
#         print(f'>>>>>>>>>>>>>>>VIDEO DATA<<<<<<<<<<<<<<>>> {video_id} >>>data {data}')

#         summary = data['summary']
#         comments = list(zip(data['comments'], data['predictions']))
#     return render_template('index.html', summary=summary, comments=comments)

#########################################################################################################
# from urllib.parse import urlparse, parse_qs

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     summary = None
#     comments = []
#     if request.method == 'POST':
#         video_url = request.form.get('video_url')

#         # Parse the video_id using urllib.parse
#         parsed_url = urlparse(video_url)
#         video_id = parse_qs(parsed_url.query).get('v', [None])[0]

#         if video_id is None:
#             return {"error": "Invalid video URL"}

#         print(f'>>>>>>>>>>>>>>>VIDEO ID<<<<<<<<<<<<<<>>> {video_id}')
#         data = get_video(video_id)
#         print(f'>>>>>>>>>>>>>>>VIDEO DATA<<<<<<<<<<<<<<>>> {video_id} >>>data {data}')

#         summary = data['summary']
#         comments = list(zip(data['comments'], data['predictions']))
#     return render_template('index.html', summary=summary, comments=comments)
#########################################################################################################

import re

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    comments = []
    if request.method == 'POST':
        video_url = request.form.get('video_url')

        # Use regular expressions to extract video_id from different URL formats
        video_id_match = re.search(r'(?:youtu\.be/|youtube\.com/(?:[^/]+/./+)+|youtube\.com(?:[^/]+/+|/v/|.+v=))([^"&?/ ]{11})', video_url)

        if not video_id_match:
            return {"error": "Invalid video URL"}

        video_id = video_id_match.group(1)

        print(f'>>>>>>>>>>>>>>>VIDEO ID<<<<<<<<<<<<<<>>> {video_id}')
        data = get_video(video_id)
        print(f'>>>>>>>>>>>>>>>VIDEO DATA<<<<<<<<<<<<<<>>> {video_id} >>>data {data}')

        summary = data['summary']
        comments = list(zip(data['comments'], data['predictions']))
    return render_template('index.html', summary=summary, comments=comments)

if __name__ == '__main__':
    app.run(debug=True)
