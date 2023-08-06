def 데이터부르기(file):
    if file == 'iris':
        from sklearn.datasets import load_iris
        import pandas as pd
        iris_db = load_iris()
        f_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        iris_df1 = pd.DataFrame(iris_db.data, columns=f_names)
        iris_df2 = pd.DataFrame(iris_db.target)
        iris_df2.columns = ['sp']
        iris_df2.sp = iris_df2.sp.map({0:'setosa', 1:'versicolor', 2:'virginica'})
        iris_df = pd.concat([iris_df1, iris_df2], axis=1)
        iris_df.head()
        return iris_df
    elif file == 'boston':
        from sklearn.datasets import load_boston
        import pandas as pd
        db = load_boston()
        f_names = db.feature_names
        data_df1 = pd.DataFrame(db.data, columns=f_names)
        data_df2 = pd.DataFrame(db.target)
        data_df2.columns = ['avg_price']
        data_df = pd.concat([data_df1, data_df2], axis=1)
        data_df.head()
        return data_df
    else:
        print ('데이터를 불러오는데 실패했습니다. 데이터셋 이름을 입력해 주세요.')

def 산점도(file, x, y, user_color, save_parity):
    import matplotlib.pyplot as plt
    df = 데이터부르기(file)
    user_color = user_color
    x_str = x
    y_str = y
    plt.scatter(df[x_str], df[y_str], color=user_color)
    if save_parity == 1:
        plt.savefig('./graph1.png')
    plt.show()
    

def 상관관계도(file, user_color, save_parity):
    if file == 'iris':
        import seaborn as sns
        import matplotlib.pyplot as plt
        df = 데이터부르기(file)
        user_color = user_color
        corr_df = df.iloc[:,:4].corr()
        fig = plt.figure(figsize=(10,6))
        sns.heatmap(data=corr_df, annot=True, fmt='.2f', cmap=user_color)
        plt.xticks(rotation=60)
        plt.show()
        if save_parity == 1:
            fig.savefig('./graph2.png')
    elif file == 'boston':
        import seaborn as sns
        import matplotlib.pyplot as plt
        df = 데이터부르기(file)
        user_color = user_color
        corr_df = df.iloc[:,:].corr()
        fig = plt.figure(figsize=(10,6))
        sns.heatmap(data=corr_df, annot=True, fmt='.2f', cmap=user_color)
        plt.xticks(rotation=60)
        plt.show()
        if save_parity == 1:
            fig.savefig('./graph2.png')
    else:
        print ('데이터셋을 불러오는데 실패했습니다. 다시 시도해 주세요.')

def 교차도(file, save_parity):
    if file == 'iris':
        import seaborn as sns
        import matplotlib.pyplot as plt
        df = 데이터부르기(file)
        plt.figure(figsize=(10,6))
        sns.pairplot(data=df.iloc[:,:], hue='sp')
        if save_parity == 1:
            plt.savefig('./graph3.png')
        plt.show()
    elif file == 'boston':
        import seaborn as sns
        import matplotlib.pyplot as plt
        df = 데이터부르기(file)
        plt.figure(figsize=(10,6))
        sns.pairplot(data=df.iloc[:,:])
        if save_parity == 1:
            plt.savefig('./graph3.png')
        plt.show()
    else:
        print ('데이터셋을 불러오는데 실패했습니다. 다시 시도해 주세요.')

def 분류모델(df):
    df = df
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    m_list = []
    if type(y[0]) == str:
        from sklearn.utils.testing import all_estimators
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
        import warnings
        warnings.filterwarnings('ignore')
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)

        model = all_estimators(type_filter='classifier')

        for key, val in model:
            try:
                model = val()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                m_list.append(model)
                print ('============================[%s 분류 모델]============================\n'%key)
                print (key,'분류 모델의 정확도: ', accuracy_score(y_pred, y_test))
                print (key,'분류 모델의 오차행렬표\n', confusion_matrix(y_pred, y_test))
                print (key,'분류 모델의 정밀도, 재현도, f1-score \n', classification_report(y_pred, y_test))
            except:
                print ('=====================================================================\n')
                print (key, '분류 모델의 정확도를 계산할 수 없습니다.')
        return m_list
#         return X, y
    else:
        print ('분류 모델로 머신러닝할 수 없는 데이터셋입니다.')

def 회귀모델(df, list_tmp):
    if list_tmp != '':
        df = df
        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]

        if type(y[0]) != str:
            from sklearn.linear_model import LinearRegression
            from sklearn.model_selection import train_test_split
            import warnings
            warnings.filterwarnings('ignore')
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)

            model = LinearRegression()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            print ('============================회귀 모델 결과============================\n')
            print ('훈련 데이터의 정확도: ', model.score(X_train, y_train))
            print ('테스트 데이터의 정확도: ', model.score(X_test, y_test))
            try:
                print ('---------------------------------------------------------------------\n')
                print (list_tmp[0], '에 대한 예측결과: \n\n', model.predict(list_tmp))
            except:
                print ('---------------------------------------------------------------------\n')
                print ('회귀모델로 예측하고자 하는 데이터 타입이 달라서 예측하기 어렵습니다. 데이터를 점검해 주세요.')
        else:
            print ('회귀 모델에 적합한 데이터셋이 아닙니다.')
    else:
        df = df
        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]

        if type(y[0]) != str:
            from sklearn.linear_model import LinearRegression
            from sklearn.model_selection import train_test_split
            import warnings
            warnings.filterwarnings('ignore')
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)

            model = LinearRegression()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            print ('============================회귀 모델 결과============================\n')
            print ('훈련 데이터의 정확도: ', model.score(X_train, y_train))
            print ('테스트 데이터의 정확도: ', model.score(X_test, y_test))
        else:
            print ('회귀 모델에 적합한 데이터셋이 아닙니다.')
            
def 최적분류모델(df):
    df = df
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    i = 0
    m_list = []
    if type(y[0]) == str:
        
        from sklearn.utils.testing import all_estimators
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
        import warnings
        warnings.filterwarnings('ignore')
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)

        model = all_estimators(type_filter='classifier')

        for key, val in model:
            try:
                model = val()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                m_list.append(val)
                print ('============================[%d번 %s 분류 모델]============================\n'%(i, key))
                print (key,'분류 모델의 정확도: ', accuracy_score(y_pred, y_test))
                print (key,'분류 모델의 오차행렬표\n', confusion_matrix(y_pred, y_test))
                print (key,'분류 모델의 정밀도, 재현도, f1-score \n', classification_report(y_pred, y_test))
                i = i+1
            except:
                print ('=====================================================================\n')
                print (key, '분류 모델의 정확도를 계산할 수 없습니다.')
        return m_list
    else:
        print ('분류 모델로 머신러닝할 수 없는 데이터셋입니다.')

def 나의분류모델(df, my_model, list_tmp):
    df = df
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    if type(y[0]) == str:
        from sklearn.utils.testing import all_estimators
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
        import warnings
        warnings.filterwarnings('ignore')
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)

        model = all_estimators(type_filter='classifier')

        for key, val in model:
            try:
                if val == my_model:
                    model = val()
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)
                    print ('============================[%s 분류 모델]============================\n'%key)
                    print (key,'분류 모델의 정확도: ', accuracy_score(y_pred, y_test))
                    print (key,'분류 모델의 오차행렬표\n', confusion_matrix(y_pred, y_test))
                    print (key,'분류 모델의 정밀도, 재현도, f1-score \n', classification_report(y_pred, y_test))
                    try : 
                        print ('----------------------------------------------------------------------')
                        print (key,'분류 모델에 임의의 값 {}에 대한 예측은 {}와 같습니다.'.format(list_tmp[0], model.predict(list_tmp)))
                    except:
                        print (key,'분류 모델로 처리하기에 적합하지 않은 임의의 데이터입니다. 데이터 형식을 점검해 주세요.')
                    break
            except:
                print (my_model, '분류 모델로 학습할 수 없습니다.')
                break
    else:
        print ('분류 모델로 머신러닝할 수 없는 데이터셋입니다.')