'''
Description:
Author: haichun feng
Date: 2024-03-26 16:14:31
LastEditor: haichun feng
LastEditTime: 2024-03-29 11:29:28
'''
#import unittest
import pytest
from talk_to_llm import config_reader

def test_config():
    config = config_reader.ConfigManager('../talk_to_llm/config.yml')
    directory =config.get_config('AUDIO_FILES_DIRECTORY')
    assert directory == 'test_data'

# class TestConfig(unittest.TestCase):
    # def test_CircleQueue(self):
    #     circle = asr.CircularQueue(10)
    #     for item in range(0,5):
    #         segment = asr.Segment(text=f'{item}', start = 0, end = 0, no_speech_prob=0)
    #         circle.enqueue(item= segment)

    #     self.assertTrue(circle.last_item.text=='4')
    #     self.assertEqual(circle.dequeue_all(),'01234')

    # def test_is_break(self):
    #     config = config_reader.ConfigManager('talk_to_llm/config.yml')
    #     asr_instance = asr.ASR(config= config)

    #     segment1 = asr.Segment(text="1", start = 0, end = 3, no_speech_prob=0)
    #     asr_instance.queue.enqueue(segment1)

    #     segment2 = asr.Segment(text="2", start = 4, end = 5, no_speech_prob=0)
    #     self.assertTrue(asr_instance.is_a_break(segment2))


    # def test_is_break2(self):
    #     config = config_reader.ConfigManager('talk_to_llm/config.yml')
    #     asr_instance = asr.ASR(config= config)

    #     segment1 = asr.Segment(text="你好 请问明天", start = 0.0, end = 5.0, no_speech_prob=0.05024284869432449)
    #     asr_instance.queue.enqueue(segment1)

    #     segment2 = asr.Segment(text="会下雨吗", start = 0.0, end = 2.0, no_speech_prob=0.24193963408470154)

    #     print(segment2.no_speech_prob)
    #     print((segment2.start) + (5-asr_instance.queue.last_item.end))
    #     self.assertFalse(asr_instance.is_a_break(segment2))


# if __name__ == '__main__':
#     # unittest.main()
