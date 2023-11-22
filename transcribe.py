import io
from google.oauth2 import service_account
from google.cloud import speech

def transcribe(audio_file):
    client_file = "servcie_emotex.json"
    credentials = service_account.Credentials.from_service_account_file(client_file)
    client = speech.SpeechClient(credentials=credentials)

    audio_file = audio_file
    with io.open(audio_file, "rb") as f:
        content = f.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code = 'bn-BD'
    )

    response = client.recognize(config=config, audio=audio)
    # print(response.results[0].alternatives[0].transcript)
    return response.results[0].alternatives[0].transcript

# t = transcribe("G:/Capstone/Capstone-Project-Modified-TIM-Net_SER-master_gaziCuda/new bangla dataset/Audios/M_SAKIB_ANG_2.wav")