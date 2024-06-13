import streamlit as st
import os
from fastai.vision.all import *
import pathlib
import sys

# 根据不同的操作系统设置正确的pathlib.Path
if sys.platform == "win32":
    temp = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath
else:
    temp = pathlib.WindowsPath
    pathlib.WindowsPath = pathlib.PosixPath

# 获取当前文件所在的文件夹路径
path = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(path, "joke.pkl")

# 加载模型
learn_inf = load_learner(model_path)

# 恢复pathlib.Path的原始值
if sys.platform == "win32":
    pathlib.PosixPath = temp
else:
    pathlib.WindowsPath = temp

# 加载笑话数据
def load_jokes(pkl_file):
    with open(pkl_file, 'rb') as file:
        jokes = pickle.load(file)
    return jokes

# Streamlit应用界面
st.title("笑话推荐系统")

import pandas as pd
import random
import streamlit as st

# 定义函数以从Excel文件加载笑话
def load_jokes_from_excel(filename):
    # 使用pandas的read_excel函数读取Excel文件
    df = pd.read_excel(filename)
    # 假设笑话存储在DataFrame的某个列中，例如'joke'
    jokes = df['joke'].tolist()
    return jokes

# 调用函数并传入文件名
jokes = load_jokes_from_excel('Dataset4JokeSet.xlsx')

# 随机显示3个笑话并获取评分
initial_jokes = random.sample(jokes, 3)

# 创建一个字典来存储每个笑话的评分
ratings = {}

# 遍历笑话并显示评分组件
for i, joke in enumerate(initial_jokes):
    st.write(f"{i+1}. {joke}")
    rating = st.slider(f"Rate this joke ({i+1})", 0, 5)
    ratings[joke] = rating

# 创建一个提交评分的按钮
if st.button("提交评分"):
    # 假设您想要在用户提交评分后推荐新的笑话
    # 这里我们简单地选择5个未被评分的笑话
    rated_jokes = set(initial_jokes)
    remaining_jokes = [joke for joke in jokes if joke not in rated_jokes]
    recommended_jokes = random.sample(remaining_jokes, 5)

    # 显示推荐的笑话并获取评分
    recommended_ratings = [st.slider(joke, 0, 5) for joke in recommended_jokes]

    # 计算并显示用户满意度
    satisfaction = sum(recommended_ratings) / len(recommended_ratings)
    st.write(f"本次推荐的满意度为: {satisfaction:.2f}/5")

# 创建一个提交推荐的评分的按钮
if st.button("提交推荐评分"):
    # 计算用户对推荐的笑话的平均评分
    avg_recommended_score = sum(ratings.values()) / len(ratings)

    # 计算百分比
    percentage_score = (avg_recommended_score / 5) * 100

    # 显示结果
    st.write(f"You rated the recommended jokes {percentage_score:.2f}% of the total possible score.")