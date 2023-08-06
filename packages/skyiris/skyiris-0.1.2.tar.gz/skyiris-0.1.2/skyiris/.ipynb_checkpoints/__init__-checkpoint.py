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
        f_names = db.feautre_names
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