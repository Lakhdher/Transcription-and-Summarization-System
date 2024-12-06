import whisper

def transcribe_video(video_path):
    model = whisper.load_model("base")
    result = model.transcribe(video_path, verbose=True)
    transcription = result["text"]

    with open("files/input/transcription.txt", "w") as f:
        f.write(transcription)

    print("Transcription terminée et sauvegardée dans 'transcription.txt'")