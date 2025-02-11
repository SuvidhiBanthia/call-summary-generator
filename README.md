# Call Summary Generator

## Features
- Accepts an audio file and generates a summary of the conversation.
- Identifies key points and suggests 3 potential titles for the meeting.

## Setup Instructions
1. Clone the repository
2. Install requirements: pip install -r requirements.txt
3. Run python manage.py runserver
4. Use Postman or curl to send a POST request to the correct endpoint: http://127.0.0.1:8000/api/generate-summary/ and attach an audio file to the request to generate transcript, summary and titles.
