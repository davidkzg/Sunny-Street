import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import pandas as pd
df = pd.read_csv("data.csv",encoding = 'utf8')
df = df[["Journal Entry", "Activity Date"]]
df = df.dropna()
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')
sent = df['Journal Entry'].values

res = []
for i in sent:
    i = i.replace('\n',' ')
    doc = nlp(i)
    res.append(doc._.polarity)

df['sent'] = res

df.to_csv("sent_Journal.csv")

