'''
Description: 
Author: haichun feng
Date: 2024-03-26 16:14:31
LastEditor: haichun feng
LastEditTime: 2024-03-27 16:38:01
'''
import unittest
import importlib

asr = importlib.import_module('talk_to_llm.asr')
config_reader = importlib.import_module('talk_to_llm.config_reader')


class TestConfig(unittest.TestCase):
    def test_CircleQueue(self):
        circle = asr.CircularQueue(10)
        for item in range(0,5):
            segment = asr.Segment(text=f'{item}', start = 0, end = 0, no_speech_prob=0)
            circle.enqueue(item= segment)

        self.assertTrue(circle.last_item.text=='4')
        self.assertEqual(circle.dequeue_all(),'01234')

    def test_is_break(self):
        config = config_reader.ConfigManager('talk_to_llm/config.yml')
        asr_instance = asr.ASR(config= config)

        segment1 = asr.Segment(text="1", start = 0, end = 3, no_speech_prob=0)
        asr_instance.queue.enqueue(segment1)

        segment2 = asr.Segment(text="2", start = 4, end = 5, no_speech_prob=0)
        self.assertTrue(asr_instance.is_a_break(segment2))

        


            

if __name__ == '__main__':
    unittest.main()
