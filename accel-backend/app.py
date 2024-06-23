from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

class Response(Resource):
    def get(self):
        return {'message': 'Hello, World!'}
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('message', type=str)
        parser.add_argument('history', type=list, location='json', required=True)
        parser.add_argument('quiz', type=bool, required=True)
        args = parser.parse_args()
        message = args['message']
        quiz = args['quiz']
        history = args['history']

        # history is in the format:
        # [
        #     {
        #         'message': 'Hello, World!',
        #         'emotion': [[Emotion1, Percentage1], [Emotion2, Percentage2], ...] (or empty array if sent by text)
        #         'type': 'user
        #     },
        #     {
        #         'message': 'What is your name?',
        #         'type': 'model'
        #     },
        # ]
        # the most recent message is at the end of the list

        # message is in the format:
        # {
        #     'message': 'Hello, World!',
        #     'emotion': [[Emotion1, Percentage1], [Emotion2, Percentage2], ...] (or empty array if sent by text)
        #     'type': 'user'
        # }
        
        if quiz:
            if message:
                # the user has answered the question, or requested to go back to chat mode
                pass
            else:
                # the user just turned on quiz mode. return a question based on chat history
                pass
        else:
            # the user is in chat mode, or requested to go to quiz mode
            pass

        return {
            'quiz': False, # whether to TOGGLE quiz mode on/off (not the actual value of quiz mode)
            'message': 'Hello, World!', # the message to display to the user (can be empty if quiz is True) also please try to make it markdown formatted
        }

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5001")