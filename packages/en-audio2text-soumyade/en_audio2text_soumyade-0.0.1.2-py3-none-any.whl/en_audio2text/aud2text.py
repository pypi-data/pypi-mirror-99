import speech_recognition
import os
from en_audio2text.text_rules import TextConvRules


class SpeechRecognizer:
    """
    Speech Recognition module developed using the speech_recognition package and it uses
    google's speech_to_text api. Input can be accept directly from microphone or from saved
    audio_files.
    """
    
    def __init__(self, src='mic', debug = False):
        """
        The constructor is used to set some initial configurations. 
        Settings include:
        * source ----- 'mic'/'file' to set source of the speech
                        mic - source is set to device microphone
                        file - source is set to device harddrive
        * debug ----- boolean (True/False)
                      True - to see all the transcribed text & 
                      their probabilities return by the api 
        
        """
        self.recog_obj = speech_recognition.Recognizer() #setting the recognizer object (a instance of Recognizer module of speech_recognition package)
        self.mic_obj = speech_recognition.Microphone() #setting the microphone object (a instance of Microphone module of speech_recognition package)
        self.debug = debug #debug option
        self.src = src #source option
        self.tcr = TextConvRules() #instance Text conversion module that can later used to define conversion rule in the text such as punctuation
    
    def act(self, audio_file=None):
        """
        This method takes a file name as argument if source is set file while object construction
        While transcription it also checks for consistencies or throws warning otherwise.
        
        """
        #file as source
        if self.src == 'file':
            if audio_file is None:
                raise ValueError("Please provide a audio_file")
                return None
            elif not os.path.exists(audio_file):
                raise FileNotFoundError("Specified file not found")
                return None
            else:
                file = speech_recognition.AudioFile(audio_file)
                with file:
                    speech = self.recog_obj.record(file)
        
        #mic as source
        elif self.src == 'mic':
            if audio_file is not None:
                print("WARNING: source is set to device microphone. Audio file will be ignored\n")
            
            try:
                with self.mic_obj:
                    print("Speak into the mic....\n")
                    self.recog_obj.adjust_for_ambient_noise(self.mic_obj)
                    speech = self.recog_obj.listen(self.mic_obj)
            #if microphone is not detected
            except OSError:
                print("Error: Microphone not detected")
                return None
                
        
        try:
            print("Please wait while we transcribe...\n")
            text = self.recog_obj.recognize_google(speech, language='en', show_all=self.debug)
            
        #if audio is not detected
        except speech_recognition.UnknownValueError:
            print("Error: Sorry audio not detected by device microphone")
            return None
        
        #if there is connection issue or api issue
        except speech_recognition.RequestError:
            print("Error: API for transcription is not reachable. There may be some connection issue or server side issue")
            return None
        
        #for imposing various rules to text 
        #But if debug mode is enabled, transcript variable will store a dictionary of various transcriptions 
        #along with their confidence probabilities, so conversion rules are disabled meanwhile 
        transcript = self.tcr.deconcat(text) if not self.debug else text
        return transcript