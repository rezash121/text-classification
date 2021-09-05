from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.neighbors import KNeighborsClassifier
import mysql.connector
from sklearn.naive_bayes import MultinomialNB

while 1==1:
    val=input("Choose algorithm:\n1.Naive Bayes\n2.KNN\n3.Rocchio\n4.SVM\n")
    # print(val)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="docs"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM documents WHERE id<=2000")

    myresult = mycursor.fetchall()
    train = []
    train_label = []

    for x in myresult:
        train.append(x[4])
        train_label.append(x[2])
    mycursor.execute("SELECT * FROM documents WHERE id>2000")

    myresult = mycursor.fetchall()
    test = []
    test_label = []
    for x in myresult:
        test.append(x[4])
        test_label.append(x[2])
    if eval(val)==1:
        text_clf = Pipeline([('vect', CountVectorizer()),
                             ('tfidf', TfidfTransformer()),
                             ('clf', MultinomialNB()),
                             ])

        text_clf.fit(train, train_label)
        predicted = text_clf.predict(test)
        inputs = input("choose measure for evaluation:\n1.Precision and Recall\n2.Accuracy\n3.F1 measure\n")
        if eval(inputs) == 1:
            print("Recall        Precision       class")
            for x in range(0, 14):
                print(text_clf.classes_[x], "       ",
                      format(metrics.precision_recall_fscore_support(test_label, predicted)[0][x], '.2f')
                      , "        ", format(metrics.precision_recall_fscore_support(test_label, predicted)[1][x], '.2f'))
        if eval(inputs) == 2:
            print("Accuracy is: ", metrics.accuracy_score(test_label, predicted))
        if eval(inputs) == 3:
            print("F measure       class")
            for x in range(0, 14):
                print(text_clf.classes_[x], "       ",
                      format(metrics.precision_recall_fscore_support(test_label, predicted)[2][x], '.2f'))

    if eval(val)==2:
        text_clf = Pipeline([('vect', CountVectorizer()),
                             ('tfidf', TfidfTransformer()),
                             ('clf',KNeighborsClassifier(n_neighbors=10)),
                             ])

        text_clf.fit(train, train_label)
        predicted = text_clf.predict(test)
        inputs = input("choose measure for evaluation:\n1.Precision and Recall\n2.Accuracy\n3.F1 measure\n")
        if eval(inputs) == 1:
            print("Recall        Precision       class")
            for x in range(0, 14):
                print(text_clf.classes_[x], "       ",
                      format(metrics.precision_recall_fscore_support(test_label, predicted)[0][x], '.2f')
                      , "        ", format(metrics.precision_recall_fscore_support(test_label, predicted)[1][x], '.2f'))
        if eval(inputs) == 2:
            print("Accuracy is: ", metrics.accuracy_score(test_label, predicted))
        if eval(inputs) == 3:
            print("F measure       class")
            for x in range(0, 14):
                print(text_clf.classes_[x], "       ",
                      format(metrics.precision_recall_fscore_support(test_label, predicted)[2][x], '.2f'))

    if eval(val)==3:
        text_clf = Pipeline([('vect', CountVectorizer()),
                             ('tfidf', TfidfTransformer()),
                             ('clf',NearestCentroid()),
                             ])

        text_clf.fit(train, train_label)
        predicted = text_clf.predict(test)
        inputs = input("choose measure for evaluation:\n1.Precision and Recall\n2.Accuracy\n3.F1 measure\n")
        if eval(inputs) == 1:
            print("Recall        Precision       class")
            for x in range(0, 14):
                print(text_clf.classes_[x], "       ",
                      format(metrics.precision_recall_fscore_support(test_label, predicted)[0][x], '.2f')
                      , "        ", format(metrics.precision_recall_fscore_support(test_label, predicted)[1][x], '.2f'))
        if eval(inputs) == 2:
            print("Accuracy is: ", metrics.accuracy_score(test_label, predicted))
        if eval(inputs) == 3:
            print("F measure       class")
            for x in range(0, 14):
                print(text_clf.classes_[x], "       ",
                      format(metrics.precision_recall_fscore_support(test_label, predicted)[2][x], '.2f'))

    if eval(val)==4:
        text_clf = Pipeline([('vect', CountVectorizer()),
                             ('tfidf', TfidfTransformer()),
                             ('clf', LinearSVC(C=1)),
                             ])

        text_clf.fit(train, train_label)
        predicted = text_clf.predict(test)
        inputs = input("choose measure for evaluation:\n1.Precision and Recall\n2.Accuracy\n3.F1 measure\n")
        if eval(inputs)==1:
            print("Recall        Precision       class")
            for x in range(0,14):
                print(text_clf.classes_[x],"       ", format(metrics.precision_recall_fscore_support(test_label, predicted)[0][x],'.2f')
                  ,"        ",format(metrics.precision_recall_fscore_support(test_label, predicted)[1][x],'.2f'))
        if eval(inputs)==2:
            print("Accuracy is: ", metrics.accuracy_score(test_label, predicted))
        if eval(inputs)==3:
            print("F measure       class")
            for x in range(0,14):
                print(text_clf.classes_[x],"       ", format(metrics.precision_recall_fscore_support(test_label, predicted)[2][x],'.2f'))
