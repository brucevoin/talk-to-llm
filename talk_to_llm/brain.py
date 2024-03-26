'''
Description: 
Author: haichun feng
Date: 2024-03-22 14:21:58
LastEditor: haichun feng
LastEditTime: 2024-03-26 16:41:50
'''


from llama_index.llms.ollama import Ollama
from llama_index.core import Settings


class Brain:
    def __init__(self):
        # setting up the llm
        self.llm = llm = Ollama(model="gemma:2b", request_timeout=60.0) 
        
    def think(self,input):
        output = self.llm.complete(input)
        print(output.text)
        return output.text

    def attention(self, asr_input):
        asr_text = str.strip(asr_text)
        if str == '':
            return

# Just for Test
if __name__ == "__main__":
    brain = Brain()
    brain.think('你好')
