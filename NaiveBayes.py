from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.datasets import fetch_20newsgroups

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="docs"
)
# print(mydb)
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM documents WHERE id<=2000")

myresult = mycursor.fetchall()
train=[]
train_label=[]

for x in myresult:
  train.append(x[4])
  train_label.append(x[2])
  # print(x[2])
mycursor.execute("SELECT * FROM documents WHERE id>2000")

myresult = mycursor.fetchall()
test=[]
test_label=[]
for x in myresult:
  test.append(x[4])
  test_label.append(x[2])
text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB()),
                     ])

text_clf.fit(train, train_label)
predicted = text_clf.predict(test)
print(metrics.classification_report(test_label, predicted))
