from flask import Flask
from flask_restful import Resource, Api, reqparse
import QuizUtil, RagUtil

app = Flask(__name__)
api = Api(app)

CHEMISTRY_KB_ID = "AYP1IY3IUL"
CONTEXT_NUM = 5
prevQuestion = ""


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
        turnQuizOn = False
        justEnabledQuiz = False

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
        print(message)
        didEnableQuiz = QuizUtil.predictQuiz(message)
        print("didEnableQuiz", didEnableQuiz, type(didEnableQuiz))
        if ("True" in didEnableQuiz):
            turnQuizOn = True
            justEnabledQuiz = True
        else:
            turnQuizOn = False
        
        if turnQuizOn:
            print("1")
            if not justEnabledQuiz: # the user has answered the question, or requested to go back to chat mode
                response = QuizUtil.check_answer(prevQuestion, message)
                justEnabledQuiz = False


            else: # the user just turned on quiz mode. return a question based on chat history
                response = QuizUtil.generate_question(history)

        else:
            print("2")

            # the user is in chat mode, or requested to go to quiz mode
            response = RagUtil.get_context(message, CHEMISTRY_KB_ID, CONTEXT_NUM)

            #TODO: instead of returning response, send it as context + message to send to model and retrieve response



        # print("got to return")
        # print(response)
        return {
            'highlight': -1, # 0 if no highlight, 1 for green, 2 for red.
            'message': response, # the message to display to the user (can be empty if quiz is True) also please try to make it markdown formatted
        }
    
class Response2(Resource):
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
        
        # history will now be in the format:
        # [
        #     {
        #         'message': 'Hello, World!',
        #         'emotion': [[Emotion1, Percentage1], [Emotion2, Percentage2], ...] (or empty array if sent by text)
        #         'type': 'user,
        #         'highlight': 0, (0 if no highlight, 1 for green, 2 for red)
        #     },
        #     {
        #         'message': 'What is your name?',
        #         'type': 'model'
        #     },  'quiz': False (determines if bot message is fancy-styled or not)
        #     },
        # ]

        if quiz:
            if message:
                # grade user's answer based on previous question (history[-2])
                return {
                    'highlight': 1, # 1 if correct, 2 if wrong
                    'message': "FEEDBACK"
                }
            else:
                # generate a new question
                return {
                    'highlight': 0,
                    'message': "QUESTION"
                }
        else:
            # generate a response
            return {
                'highlight': 0,
                'message': "RESPONSE"
            }

api.add_resource(Response, '/response')
api.add_resource(Response2, '/response2')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5001")