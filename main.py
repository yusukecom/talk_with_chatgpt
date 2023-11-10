import keyboard
import os
import tempfile

import numpy as np
import openai
import sounddevice as sd
import soundfile as sf
from serpapi import GoogleSearch

from elevenlabs import generate, play, set_api_key
from langchain.agents import initialize_agent, load_tools, Tool
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.tools import BaseTool
from langchain.utilities import SerpAPIWrapper

from dotenv import load_dotenv
load_dotenv()


openai.api_key = os.environ.get('OPENAI_API_KEY')
serpapi_api_key = os.environ.get('SERPAPI_API_KEY')

# Set recording parameters
duration = 5  # duration of each recording in seconds
fs = 44100  # sample rate
channels = 1  # number of channels


def record_audio(duration, fs, channels):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()
    print("Finished recording.")
    return recording


def transcribe_audio(recording, fs):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        sf.write(temp_audio.name, recording, fs)
        temp_audio.close()
        with open(temp_audio.name, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        os.remove(temp_audio.name)
    return transcript["text"].strip()


def play_generated_audio(text, voice="Bella", model="eleven_monolingual_v1"):
    audio = generate(text=text, voice=voice, model=model)
    play(audio)



if __name__ == '__main__':

    llm = OpenAI(temperature=0)
    memory = ConversationBufferMemory(memory_key="chat_history")

    search = SerpAPIWrapper(serpapi_api_key = os.environ.get('SERPAPI_API_KEY'))
    tools = [
        Tool(
            name = "Current Search",
            func=search.run,
            description="useful for when you need to answer questions about current events or the current state of the world"
        ),
    ]

    agent = initialize_agent(tools, llm, memory=memory, agent="conversational-react-description", verbose=True)

    while True:
        print("Press spacebar to start recording.")
        keyboard.wait("space")  # wait for spacebar to be pressed
        recorded_audio = record_audio(duration, fs, channels)
        message = transcribe_audio(recorded_audio, fs)
        print(f"You: {message}")
        assistant_message = agent.run(message)
        play_generated_audio(assistant_message)
