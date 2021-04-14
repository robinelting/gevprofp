import unittest
import finalproject

class test_tokenizer(unittest.TestCase):
    def test_tokenizer(self):
        '''Checks if function returns a clean and lowercased sentence'''
        sentence = finalproject.tokenizer('My mama always said life was like a box of chocolates. You never know what you\'re gonna get.')
        self.assertEqual(sentence, 'my mama always said life was like a box of chocolates  you never know what you re gonna get ')


class tagger(unittest.TestCase):
    def test_tagger(self):
        '''Checks if function returns a list with the first element
    being the tag and the second element being the script text.'''
        sentence = finalproject.tagger(['                          KLAUE', '                All of it? I took a tiny piece of it. They have a mountain full of it. They\'ve been mining it for thousands of years and still haven\'t scratched the surface.', '     IN THE SEATING AREA'])
        self.assertEqual(sentence, [['C', '                          KLAUE'],
 ['D',
  '                All of it? I took a tiny piece of it. They have a mountain '
  "full of it. They've been mining it for thousands of years and still haven't "
  'scratched the surface.'],
 ['M', '     IN THE SEATING AREA']])

    def test_value(self):
        '''Checks if the function will raise a TypeError when necessary, and checks if the value is a list'''
        sentence = finalproject.tagger(['                          KLAUE', '                All of it? I took a tiny piece of it. They have a mountain full of it. They\'ve been mining it for thousands of years and still haven\'t scratched the surface.', '     IN THE SEATING AREA'])
        self.assertRaises(TypeError, finalproject.tagger, -2)
        self.assertRaises(TypeError, finalproject.tagger, True)
        self.assertIsInstance(sentence, list, msg=None)


class test_script_aligner(unittest.TestCase):
    def test_script_aligner(self):
        '''Checks if the function raise a TypeError when necessary, and checks if the value is a list'''
        tagged_sentences = finalproject.script_aligner([['C', '                          OKOYE', 'D', '                Where is Agent Ross? ']], ['the apology from', 'where is'], ['01:44:24,308 --> 01:44:27,895', '01:45:24,308 --> 01:44:27,895'])

        self.assertIsInstance(tagged_sentences, list, msg=None)
        self.assertRaises(TypeError, finalproject.tagger, -2)
        self.assertRaises(TypeError, finalproject.tagger, True)


if __name__ == '__main__':
    unittest.main()
