from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.datasets import fetch_20newsgroups
from sklearn.metrics import accuracy_score
import mysql.connector
import numpy as np

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
print(len(train))

randnums = np.random.randint(1, 1999, 200)
randnums.sort()
# print("randnum len is: ",len(randnums))
validation=[]
validation_label=[]
new_train=[]
new_train_label=[]
print(randnums)
print(len(train))
for x in range(1,200):
    randnums[x]-=x
print(randnums)
for x in randnums:
    # print(x)
    validation.append(train[x])
    train.pop(x)
    validation_label.append(train_label[x])
    train_label.pop(x)

print("len is:",len(train))
new_train=train
new_train_label=train_label
c=[0.25,0.5,0.75,1,1.25,1.5,1.75,2]
final_c=0
accuracy=0
for x in c:
    text_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', LinearSVC(C=x)),
                         ])

    text_clf.fit(new_train, new_train_label)
    predicted = text_clf.predict(validation)
    print("result for k=",x)
    print(metrics.classification_report(validation_label, predicted))
    # accuracy=accuracy_score(validation_label,predicted)
    if(accuracy<accuracy_score(validation_label,predicted)):
        accuracy=accuracy_score(validation_label,predicted)
        final_c = x
        print("k is: ",final_c,"acc is: ",accuracy)
mycursor.execute("SELECT * FROM documents WHERE id>2000")
print("final c is: ",final_c)
myresult = mycursor.fetchall()
test=[]
test_label=[]
for x in myresult:
  test.append(x[4])
  test_label.append(x[2])
text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', LinearSVC(C=final_c)),
                     ])

text_clf.fit(train, train_label)
predicted = text_clf.predict(test)
print(metrics.classification_report(test_label, predicted))