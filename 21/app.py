import os

from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)
app = Flask(__name__)
def get_openai_response(message):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an excellent call center operator."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""
                        # message
                        {message}

                        Please respond to the above message briefly.
                        """
                    }
                ]
            }
        ],
        max_tokens=300
    )
    result = response.choices[0].message.content

    return result


@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Handle incoming call and gather speech input"""
    response = VoiceResponse()

    # Gather speech input from the user
    gather = Gather(input='speech', action='/process_speech', speechTimeout='auto', language='en-US')
    gather.say("Hello, How's it going?", language="en-US")

    response.append(gather)
    response.say("Input could not be verified. Good-bye.", language="en-US")

    return Response(str(response), mimetype="application/xml")

@app.route("/process_speech", methods=['GET', 'POST'])
def process_speech():
    """Process the gathered speech input and respond using GPT-4o-mini"""
    response = VoiceResponse()

    # Get the transcribed speech from Twilio
    speech_result = request.form.get('SpeechResult')

    if speech_result:
        # Get GPT-4 response
        gpt_response = get_openai_response(speech_result)

        # Respond with the GPT-4 generated text
        response.say(gpt_response, language="en-US")

        # Loop back to the /voice endpoint to continue the conversation
        gather = Gather(input='speech', action='/process_speech', speechTimeout='auto', language='en-US')
        response.append(gather)
    else:
        response.say("Input could not be verified. Good-bye.", language="en-US")

    return Response(str(response), mimetype="application/xml")

if __name__ == "__main__":
    # On the latest Mac, port 5000 is occupied, so we'll use port 8000.
    app.run(port=8000, debug=True)