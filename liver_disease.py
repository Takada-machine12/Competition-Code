# -*- coding: utf-8 -*-
"""Liver_Disease.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1d_dAo9Q0Pe8Ff5h4uqJPYcWzWodSPOZk
"""

#import Library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import roc_auc_score, roc_curve, classification_report

#import Dataset
path = "/content/drive/MyDrive/SIGNATEコンペ/肝疾患予測（分類）v2/"
train = pd.read_csv(path + "train.csv")
test = pd.read_csv(path + "test.csv")

#Dataset
train.shape, test.shape

#Dataset infomation
train.info()

test.info()

train.head(10)

"""# **前処理**"""

#Gender transform int
train["Gender"] = train["Gender"].replace({"Male":0, "Female":1}).astype(int)
test["Gender"] = test["Gender"].replace({"Male":0, "Female":1}).astype(int)

train.info()

test.info()

"""**性別別の罹患率**"""

#性別別の罹患率
#女性
women = train.loc[train.Gender == 1]["disease"]
rate_women = sum(women)/len(women)

print(f"% of women who disease: {rate_women}")

#性別別の罹患率
#男性
men = train.loc[train.Gender == 0]["disease"]
rate_men = sum(men)/len(men)

print(f"% of women who disease: {rate_men}")

"""**年代別の罹患率**"""

#年代別のカラムを新規に作成
def age_group(age):
    if age < 20:
        return 10
    elif age < 30:
        return 20
    elif age < 40:
        return 30
    elif age < 50:
        return 40
    elif age < 60:
        return 50
    elif age < 70:
        return 60
    else:
        return 70

train["AgeGroup"] = train["Age"].apply(age_group)
train[["Age", "AgeGroup"]]

#年代別の罹患率
#20代
age20 = train.loc[train.AgeGroup == 20]["disease"]
age20_rate = sum(age20)/len(age20)
print(f"age20_rate: {age20_rate}")

#年代別の罹患率
#30代
age30 = train.loc[train.AgeGroup == 30]["disease"]
age30_rate = sum(age30)/len(age30)
print(f"age30_rate: {age30_rate}")

#年代別の罹患率
#40代
age40 = train.loc[train.AgeGroup == 40]["disease"]
age40_rate = sum(age40)/len(age40)
print(f"age40_rate: {age40_rate}")

#年代別の罹患率
#50代
age50 = train.loc[train.AgeGroup == 50]["disease"]
age50_rate = sum(age50)/len(age50)
print(f"age50_rate: {age50_rate}")

#年代別の罹患率
#60代
age60 = train.loc[train.AgeGroup == 60]["disease"]
age60_rate = sum(age60)/len(age60)
print(f"age60_rate: {age60_rate}")

#年代別の罹患率
#70代
age70 = train.loc[train.AgeGroup == 70]["disease"]
age70_rate = sum(age70)/len(age70)
print(f"age70_rate: {age70_rate}")

"""**30代男性と女性の罹患率**"""

#年代別の罹患率
#30代男性
age30 = train.loc[train.AgeGroup == 30][train.Gender == 0]["disease"]
age30_rate = sum(age30)/len(age30)
print(f"age30_rate: {age30_rate}")

#年代別の罹患率
#30代女性
age30 = train.loc[train.AgeGroup == 30][train.Gender == 1]["disease"]
age30_rate = sum(age30)/len(age30)
print(f"age30_rate: {age30_rate}")

#年代別の罹患率
#70代男性
age70 = train.loc[train.AgeGroup == 70][train.Gender == 0]["disease"]
age70_rate = sum(age70)/len(age70)
print(f"age70_rate: {age70_rate}")

#年代別の罹患率
#70代女性
age70 = train.loc[train.AgeGroup == 70][train.Gender == 1]["disease"]
age70_rate = sum(age70)/len(age70)
print(f"age70_rate: {age70_rate}")

#性別の罹患率をグラフで表示
plt.figure(figsize=(10, 8))
genders = ["Men", "Women"]
rates = [rate_men, rate_women]

plt.bar(genders, rates, color=["blue", "pink"])
plt.title("Disease Rate by Gender")
plt.xlabel("Gender")
plt.ylabel("Disease Rate")

#%をグラフに表示
for i, v in enumerate(rates):
    plt.text(i, v, f"{v:.2%}", ha="center", va="bottom")

plt.ylim(0, 1)

plt.show()

#各年代の罹患率を再度計算し、それをグラフで表示
def caluclate_rate(train, age_group):
    age_data = train.loc[train.AgeGroup == age_group]["disease"]
    return sum(age_data)/len(age_data) if len(age_data) > 0 else 0

#各年代の罹患率を計算
age_groups = [20, 30, 40, 50, 60, 70]
rates = [caluclate_rate(train, age) for age in age_groups]

#グラフ作成
plt.figure(figsize=(10, 8))
plt.bar(age_groups, rates, color="skyblue")
plt.title("Disease Rate by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Disease")

#x軸ラベルの設定
plt.xticks(age_groups, [f"{age}s" for age in age_groups])

#%表示
for i, v in enumerate(rates):
    plt.text(age_groups[i], v, f"{v:.2%}", ha="center", va="bottom")

plt.ylim(0, 1)
plt.show()

#statistical infomation
train.describe()

#箱ひげ図で統計情報を確認
#分析対象の検査項目
lab_tests = ["Age", "T_Bil", "D_Bil", "ALP", "ALT_GPT", "AST_GOT", "TP", "Alb", "AG_ratio"]

#データ準備
melted_data = pd.melt(train[lab_tests], var_name="Test", value_name="Value")

#箱ひげ図作成
plt.figure(figsize=(10, 8))
sns.boxplot(x="Test", y="Value", data=melted_data)

#グラフ装飾
plt.title("Distribution of Lab Test Results", fontsize=20)
plt.xlabel("Lab Tests", fontsize=15)
plt.ylabel("Values", fontsize=15)
plt.xticks(rotation=45)

#y軸の範囲調整（外れ値が多い場合）
plt.ylim(0, 500)

#レイアウト調整
plt.tight_layout()

plt.show()

"""# **データセット作成**"""

#訓練データ
x = train[["Gender", "T_Bil", "D_Bil", "ALP", "ALT_GPT", "AST_GOT", "TP", "AG_ratio"]]
#テストデータ
y = train["disease"]
#推論データ
x_test = test[["Gender", "T_Bil", "D_Bil", "ALP", "ALT_GPT", "AST_GOT", "TP", "AG_ratio"]]

#データ分割(ホールドアウト)
x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, random_state=0, stratify=y)

"""# **モデル作成・学習・推論**"""

#LightGBMで学習
import lightgbm as lgb

#lightgbm用のデータセット作成
train_data = lgb.Dataset(x_train, label=y_train)
test_data = lgb.Dataset(x_val, label=y_val, reference=train_data)

#パラメータ設定
params = {
    "objective":"binary",
    "metric":"auc",
    "boosting_type":"gbdt",
    "num_leaves":63,
    "learning_rate":0.05,
    "feature_fraction":0.9,
    "bagging_fraction":0.8,
    "bagging_freq":5,
    "verbose":-1
}

#モデル学習
model = lgb.train(
    params,
    train_data,
    num_boost_round=100,
    valid_sets=[test_data],
    callbacks=[lgb.early_stopping(stopping_rounds=100)],
)

#検証用データで推論
y_pred = model.predict(x_val, num_iteration=model.best_iteration)
auc_score = roc_auc_score(y_val, y_pred)

#モデル評価
print(f"AUC Score: {auc_score}" )

#テスト用データで推論
y_pred_proba = model.predict(x_test, num_iteration=model.best_iteration)

#提出用データセット作成
output = pd.DataFrame({"id":test.index, "disease":y_pred_proba})
output.to_csv("y_pred_pro_5.csv", index=False, header=None)
