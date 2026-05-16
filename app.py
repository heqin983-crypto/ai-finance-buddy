import os
from http import HTTPStatus

import streamlit as st
from dashscope import Application


# =========================
# 基础配置
# =========================

APP_ID = "98f52639c9a2420faf6160a840227c43"  # 替换成你的百炼应用 ID
API_KEY = "sk-835f1ccc946440248a15393924838e98"


st.set_page_config(
    page_title="AI理财搭子",
    page_icon="💰",
    layout="centered"
)


# =========================
# 页面样式
# =========================

st.markdown(
    """
    <style>
    .main-title {
        font-size: 34px;
        font-weight: 800;
        color: #0b2f5b;
        margin-bottom: 6px;
    }
    .subtitle {
        font-size: 16px;
        color: #5b6b7f;
        margin-bottom: 20px;
    }
    .intro-box {
        background: #f6f9ff;
        border: 1px solid #dbe7ff;
        border-radius: 16px;
        padding: 18px 20px;
        margin-bottom: 20px;
        line-height: 1.8;
        color: #26364a;
    }
    .tag {
        display: inline-block;
        background: #fff3e8;
        color: #e56a28;
        border-radius: 999px;
        padding: 4px 10px;
        margin-right: 6px;
        font-size: 13px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# 标题与开场白
# =========================

st.markdown('<div class="main-title">💰 AI理财搭子</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">面向大学生的轻量化、陪伴式、非营销型理财助手</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="intro-box">
    嗨，我是你的 <b>AI理财搭子</b> 👋<br>
    我不是来推销理财产品的，也不会让你去做高风险投资。<br><br>
    我可以帮你：
    <br>✅ 分析消费习惯，看看钱都花去哪了
    <br>✅ 制定适合大学生的攒钱计划
    <br>✅ 用聊天方式讲清楚基础理财知识
    <br>✅ 提醒你识别冲动消费和情绪消费
    <br>✅ 陪你一起养成长期存钱习惯
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <span class="tag">消费分析</span>
    <span class="tag">攒钱计划</span>
    <span class="tag">理财启蒙</span>
    <span class="tag">情绪消费提醒</span>
    <span class="tag">长期陪伴</span>
    """,
    unsafe_allow_html=True
)


# =========================
# 快捷问题
# =========================

st.divider()

st.subheader("你可以先试试这些问题")

quick_questions = [
    "我每月生活费2000元，想每月存500元，怎么安排？",
    "我总是情绪不好就想买东西，怎么办？",
    "大学生应该怎么开始理财？",
    "我不懂基金、余额宝、银行理财，它们有什么区别？",
    "帮我复盘一下：我这个月外卖花了600元，奶茶花了300元，社交聚餐花了800元。",
]

selected_question = st.selectbox(
    "选择一个问题快速体验：",
    [""] + quick_questions
)


# =========================
# 会话状态
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "欢迎来到 AI理财搭子～你可以告诉我你的生活费、消费习惯或存钱目标，我来帮你一起规划。"
        }
    ]


# =========================
# 调用百炼智能体
# =========================

def call_agent(user_prompt: str) -> str:
    if not API_KEY:
        return "未检测到 DASHSCOPE_API_KEY，请先在环境变量中配置你的百炼 API Key。"

    try:
        response = Application.call(
            api_key=API_KEY,
            app_id=APP_ID,
            prompt=user_prompt
        )

        if response.status_code != HTTPStatus.OK:
            return (
                f"调用失败：\n\n"
                f"request_id: {response.request_id}\n\n"
                f"code: {response.status_code}\n\n"
                f"message: {response.message}"
            )

        return response.output.text

    except Exception as e:
        return f"调用智能体时出现错误：{e}"


# =========================
# 展示历史对话
# =========================

st.divider()
st.subheader("开始和 AI理财搭子聊天")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# =========================
# 用户输入
# =========================

user_input = st.chat_input("输入你的问题，比如：我总是存不下钱怎么办？")

if selected_question and not user_input:
    user_input = selected_question


if user_input:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("AI理财搭子正在帮你分析..."):
            answer = call_agent(user_input)
            st.write(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# =========================
# 侧边栏
# =========================

with st.sidebar:
    st.title("💡 使用说明")
    st.write("这个 Demo 用于展示大学生 AI理财搭子的核心能力。")

    st.markdown("""
    **核心能力：**
    - 消费分析
    - 存钱计划
    - 理财知识讲解
    - 情绪消费提醒
    - 陪伴式监督
    """)

    st.divider()

    if st.button("清空对话"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "对话已清空～我们重新开始吧。你现在最大的理财困扰是什么？"
            }
        ]
        st.rerun()