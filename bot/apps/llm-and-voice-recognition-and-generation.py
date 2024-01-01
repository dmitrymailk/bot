import torch
import gradio as gr
import numpy as np
from functools import partial
import requests
from bot.speech_recognition import SpeechRecognitionV1
from bot.speech_generation import SpeechGenerationV1
from bot.text_generation import llm_chat_v1
from fastapi import FastAPI

CUSTOM_PATH = "/"

app = FastAPI()


# @app.get("/")
# def read_main():
#     return {"message": "This is your main app"}


def transcribe_v1(
    audio,
    speech_recognition: SpeechRecognitionV1 = None,
    speech_generation=None,
):
    sr, y = audio
    y = y.astype(np.float32)
    y /= np.max(np.abs(y))
    sample = {"sampling_rate": sr, "y": y}
    print(sample)
    speech_text = speech_recognition(
        sampling_rate=sr,
        y=y,
    )
    llm_response = llm_chat_v1(user_text=speech_text)
    sample_rate, generated_audio = speech_generation(
        text=llm_response,
    )

    return [
        gr.Markdown(
            f"**Распознанная речь:**\n{speech_text}\n\n**Сгенерированный ответ:**\n{llm_response}"
        ),
        gr.Audio(
            value=(sample_rate, generated_audio.numpy()),
            autoplay=True,
        ),
    ]


# if __name__ == "__main__":
stt_model = SpeechRecognitionV1()
tts_model = SpeechGenerationV1()


markdown = gr.Markdown()
audio = gr.Audio()
demo = gr.Interface(
    partial(
        transcribe_v1,
        speech_recognition=stt_model,
        speech_generation=tts_model,
    ),
    inputs=gr.Audio(sources=["microphone"]),
    outputs=[markdown, audio],
)
try:
    demo = gr.mount_gradio_app(
        app,
        demo.queue(),
        path=CUSTOM_PATH,
    )

except KeyboardInterrupt:
    demo.close()
except Exception as e:
    print(e)
    demo.close()