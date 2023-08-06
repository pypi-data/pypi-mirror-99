# en_audio2text

Small module build with the help of speech_recognition package
Can be used for getting english transcription from audio via microphone or audio file

The code is written in Python 3

Installation
------------

Fast install:

::

    pip install en-audio2text-soumyade

For a manual install get this package:

::

    wget https://github.com/cssoumyade/en_audio2text/archive/master.zip
    unzip master.zip
    rm master.zip
    cd en_audio2text-master

Install the package:

::

    python setup.py install  

  

Example
--------

.. code:: python

    from en_audio2text.aud2text import SpeechRecognizer
    
    #use audio file
    sr = SpeechRecognizer(src='file')
    sr.act('sample_audio_2.wav')
    
    #use microphone
    sr = SpeechRecognizer()
    sr.act()
    
    
  Here is the sample ouput:
  
  Please wait while we transcribe...
  
  'you can not fix the thing that you have made wrong intentionally in the past'