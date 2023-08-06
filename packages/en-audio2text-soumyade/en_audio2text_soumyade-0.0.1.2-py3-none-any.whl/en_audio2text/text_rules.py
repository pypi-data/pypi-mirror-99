import re

class TextConvRules:
    """
    This class can be used for preprocessing text just by adding required conversion rules
    One such rule deconcat has been provided as an example which performs deconcatenation.
    Any defined function should be able to accept a string and after processing should be
    able to return in a string format
    """
    def __init__(self):
        """
        Does nothing. But kept for future use for initialization purpose
        """
        return
    
    def deconcat(self, text):
        """
        This function is defined to pre-process a given text by decontracting various phrase 
        in english language such as converting can't to cannot.
        This funtion is not required explicitly but it is provided as an example to add more 
        rules in future.
        """
        # performing decontractions
        text = re.sub(r"won\'t", "will not", text)
        text = re.sub(r"can\'t", "can not", text)
        text = re.sub(r"don\'t", "do not", text)
        return text