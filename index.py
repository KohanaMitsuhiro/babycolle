
import streamlit as st
from streamlit_chat import message
import openai
import os

CHAT_GPT_APIKEY = os.getenv('CHATGPT_API_KEY')
openai.api_key = CHAT_GPT_APIKEY


def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.past.append(user_input)
    res_GPT = do_question(user_input)
    st.session_state.generated.append(res_GPT)
    res_keywords = do_keyword(res_GPT)
    st.session_state.keyword.append(res_keywords)


def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]


def do_question(question):
    question = f"あなたは子供服の専門家です。以下の条件で子供に着せると良いコーディネートを２つ提案して下さい。{question}。\
                提案では４つのアイテムを組合せて下さい。\
                各アイテムにはそれぞれ理由も５０文字程度で付け加えて下さい"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": question},
        ],
    )
    answer = response.choices[0]["message"]["content"].strip().replace(" ","")
    return answer

def do_keyword(question):
    question = f"{question}　この２つの提案から４つのアイテム毎にキーワードを３つ以上抽出して下さい。。"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": question},
        ],
    )
    answer = response.choices[0]["message"]["content"].strip().replace(" ","")
    return answer


def main():
    if "generated" not in st.session_state:
        st.session_state.generated = []
    if "past" not in st.session_state:
        st.session_state.past = []
    if "keyword" not in st.session_state:
        st.session_state.keyword = []

    st.title("babycolle")

    chat_placeholder = st.empty()

    with chat_placeholder.container():
        message("こんにちは！\n赤ちゃんにぴったりな服を探すよ。\n・月齢\n・着て行く日\n・イベント内容\n・好み\n・悩んでいること\nなどを教えてね！")

        if st.session_state['generated']:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state['past'][i], is_user=True, key=str(i) + "_user")
                message(st.session_state['generated'][i], key=str(i))
                message(st.session_state['keyword'][i], key=str(i)+"_keyword")

        with st.container():
            st.text_input("入力してね",on_change=on_input_change, key="user_input")


if __name__ == "__main__":
    main()  