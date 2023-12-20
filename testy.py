'''
import re

dob = re.compile(r'(?:\bbirth\b|\bbirth(?:day|date)).{0,20}\n? \b((?:(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?\s+(?:of\s+)?(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)|(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)\s+(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?)(?:\,)?\s*(?:\d{4})?|\b[0-3]?\d[-\./][0-3]?\d[-\./]\d{2,4})\b',re.IGNORECASE | re.MULTILINE)

data = " Hi This is Goku and my birthday is on 25th July 1976 but to be clear it is on 1994-08-06."

l = dob.findall(data)

print(l)
'''

from . import svm

svm.svm_implementation()