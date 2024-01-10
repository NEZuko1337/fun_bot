import gtts
import os
import random
from bot.constants import  UPDATE1


def convert_text_to_speech(text, language_code='ru'):
   output_filepath = os.path.join("AUDIO", f"{random.randint(0, 1000000000)}.opus")
   tts = gtts.gTTS(text=text, lang=language_code)
   tts.save(output_filepath)
   return output_filepath


def update_info(text=UPDATE1, language_code='ru'):
   output_filepath = os.path.join("AUDIO", "update.opus")
   tts = gtts.gTTS(text=text, lang=language_code)
   tts.save(output_filepath)
   return output_filepath
