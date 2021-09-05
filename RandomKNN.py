from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
from sklearn.metrics import accuracy_score
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
randnums = np.random.randint(1, 1999, 200)
randnums.sort()
# print("randnum len is: ",len(randnums))
validation=[]
validation_label=[]
new_train=[]
new_train_label=[]
i=1
print(randnums)
for x in range(1,200):
    randnums[x]-=x
print(randnums)
for x in randnums:
    # print(x)
    validation.append(train[x])
    train.pop(x)
    validation_label.append(train_label[x])
    train_label.pop(x)
    # print(randnums[i])
    # print(randnums[i]-1)
    # randnums[i]=randnums[i]-1
    # i+=1
  # print(x[2])
# find=False
# for x in range(0,2000):
#     for y in randnums:
#         if y==train[x]:
#             find=True
#             print(train[x],' is in ',y)
#     if find!=True:
#         new_train.append(train[x])
#         new_train_label.append(train_label[x])
#         find=False
    # train.pop(x)
    # train_label.pop(x)
print("len is:",len(train))
new_train=train
new_train_label=train_label
neighbor=[1,5,10]
final_K=0
accuracy=0
for x in neighbor:
    text_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', KNeighborsClassifier(n_neighbors=x)),
                         ])

    text_clf.fit(new_train, new_train_label)
    predicted = text_clf.predict(validation)
    print("result for k=",x)
    print(metrics.classification_report(validation_label, predicted))
    # accuracy=accuracy_score(validation_label,predicted)
    if(accuracy<accuracy_score(validation_label,predicted)):
        accuracy=accuracy_score(validation_label,predicted)
        final_K = x
        print("k is: ",final_K,"acc is: ",accuracy)

mycursor.execute("SELECT * FROM documents WHERE id>2000")
print("final k is: ",final_K)
myresult = mycursor.fetchall()
test=[]
test_label=[]
for x in myresult:
  test.append(x[4])
  test_label.append(x[2])


text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', KNeighborsClassifier(n_neighbors=final_K)),
                     ])

text_clf.fit(train, train_label)
predicted = text_clf.predict(test)
print(metrics.classification_report(test_label, predicted))
