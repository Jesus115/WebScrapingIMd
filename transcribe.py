import whisper

model = whisper.load_model("base")
result = model.transcribe("/Users/jesus/Downloads/audio.mp3", language="es")
print(result["text"])
