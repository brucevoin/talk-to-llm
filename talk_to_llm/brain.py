'''
Description: 
Author: haichun feng
Date: 2024-03-22 14:21:58
LastEditor: haichun feng
LastEditTime: 2024-03-26 11:11:41
'''


from llama_index.llms.ollama import Ollama
from llama_index.core import Settings

from voice_clone import voice

class Brain:
    def __init__(args):
        # setting up the llm
        self.llm = llm = Ollama(model="gemma:2b", request_timeout=60.0) 
        
    def think(input):
        output = llm.complete(input)
        print(output.text)
        return output.text

    def attention(asr_input):
        asr_text = str.strip(asr_text)
        if str == '':
            return