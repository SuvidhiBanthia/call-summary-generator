import os
from django.shortcuts import render
from tempfile import NamedTemporaryFile
from pydub import AudioSegment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .serializers import SummarySerializer
from transformers import pipeline

# Initialize AI pipelines
transcriber = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-base-960h")
#summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
#transcriber = pipeline("automatic-speech-recognition", model="facebook/hubert-base-ls960")
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

class GenerateSummaryView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        # Step 1: Handle uploaded audio file
        audio_file = request.FILES.get('audio')
        if not audio_file:
            return Response({"error": "No audio file provided"}, status=400)

        try:
            # Step 2: Convert audio to WAV format (required by the transcriber)
            audio = AudioSegment.from_file(audio_file)
            audio = audio.set_channels(1).set_frame_rate(16000)

            # Define a custom temporary directory
            CUSTOM_TEMP_DIR = "C:/temp"  
            os.makedirs(CUSTOM_TEMP_DIR, exist_ok=True)

            # Use the custom directory for temporary files
            with NamedTemporaryFile(dir=CUSTOM_TEMP_DIR, suffix=".wav", delete=False) as temp_wav:
                audio.export(temp_wav.name, format="wav")

                # Step 3: Transcribe the audio
                transcription = transcriber(temp_wav.name)["text"]

            # Clean up the temporary file
            os.unlink(temp_wav.name)

        except Exception as e:
            return Response({"error": f"Audio processing failed: {str(e)}"}, status=500)

        # Step 4: Summarize the transcription
        summary = summarizer(transcription, max_length=150, min_length=30, do_sample=False)[0]['summary_text']

        # Step 5: Suggest titles
        suggested_titles = self.generate_titles(summary)

        # Step 6: Serialize the response
        serializer = SummarySerializer({
            "summary": summary,
            "suggested_titles": suggested_titles,
            "transcription": transcription
        })

        # Return the serialized data
        return Response(serializer.data)

    def generate_titles(self, summary):
        # Use a simple heuristic to suggest titles
        words = summary.split()
        title1 = " ".join(words[:5]) + "..."
        title2 = "Meeting Summary: " + " ".join(words[5:10]) + "..."
        title3 = "Key Points: " + " ".join(words[10:15]) + "..."
        return [title1, title2, title3]



