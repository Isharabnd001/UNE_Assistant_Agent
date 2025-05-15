#This util was developed to anonymyze user queries to remove sensitive information like name, email etc.
# Presidio analyzer is used for this task

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def anonymize_query(text):
    #anonymizing the input text
    results = analyzer.analyze(text=text, language='en', entities=[])
    return anonymizer.anonymize(text=text, analyzer_results=results).text
