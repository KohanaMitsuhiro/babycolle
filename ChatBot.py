
import streamlit as st
from streamlit_chat import message
import openai
import os
import ast
import requests
import json
import time

# CHAT_GPT_APIKEY = os.getenv('CHATGPT_API_KEY')
CHAT_GPT_APIKEY = st.secrets.CHAT_GPT.APIKEY
openai.api_key = CHAT_GPT_APIKEY

TEIANS = ["提案1","提案2"]
# TEIANS = ["提案1",]
COORDS = ["コーデ1","コーデ2","コーデ3","コーデ4"]
KEYWORDS = ["キーワード1","キーワード2","キーワード3"]

# <<<<<<<<<< ChatBot関数 <<<<<<<<<<
def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.past.append(user_input)
    res_GPT = do_question(user_input)
    st.session_state.generated.append(res_GPT)

    res_keywords = do_keyword(res_GPT)
    dict_keywords = convert_to_dict(res_keywords)
    ans = rakuten(dict_keywords)
    st.session_state.keyword.append(rakuten_URL(ans,dict_keywords))

    # テキスト入力を空にする
    st.session_state.user_input = ""


def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]

# <<<<<<<<<< ChatGPT関数 <<<<<<<<<<
def do_question(question):
    form = "回答は以下のような形式でお願いします。\
        提案1:\
        　・アイテム名：50文字程度の提案した理由。\
          ・アイテム名：50文字程度の提案した理由。\
        　・アイテム名：50文字程度の提案した理由。\
          ・アイテム名：50文字程度の提案した理由。\
       提案2:\
        　・アイテム名：50文字程度の提案した理由。\
          ・アイテム名：50文字程度の提案した理由。\
        　・アイテム名：50文字程度の提案した理由。\
          ・アイテム名：50文字程度の提案した理由。"
    question = f"あなたは子供服の専門家です。以下の条件で子供に着せると良いコーディネートを２つ提案して下さい。{question}。\
                提案では４つのアイテムを組合せて下さい。\
                提案したアイテム毎にそれぞれ50文字程度で理由を付けて下さい\
                アイテム名には色などは加えず、カテゴリやジャンルの呼び名にして下さい{form}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {  "role": "user", "content": question},
        ],
        temperature=0,
    )
    answer = response.choices[0]["message"]["content"].strip()
    return answer

def do_keyword(question):
    form = "回答には次のような辞書型でお願いします'\
    {'提案1':\
        {'コーデ1':{'アイテム':'ロンパース','キーワード1':'白い','キーワード2':'清潔感','キーワード3':'可愛さ','キーワード4':'お食い初め'},\
        'コーデ2':{'アイテム':'ロンパース','キーワード1':'白い','キーワード2':'清潔感','キーワード3':'可愛さ','キーワード4':'お食い初め'},\
        'コーデ3':{'アイテム':'ロンパース','キーワード1':'白い','キーワード2':'清潔感','キーワード3':'可愛さ','キーワード4':'お食い初め'},\
        'コーデ4':{'アイテム':'ロンパース','キーワード1':'白い','キーワード2':'清潔感','キーワード3':'可愛さ','キーワード4':'お食い初め'}},\
     '提案2':\
        {'コーデ1':{'アイテム':'ロンパース','キーワード1':'白い','キーワード2':'清潔感','キーワード3':'可愛さ','キーワード4':'お食い初め'},\
        'コーデ2':{'アイテム':'ロンパース','キーワード1':'白い','キーワード2':'清潔感','キーワード3':'可愛さ','キーワード4':'お食い初め'},\
        'コーデ3':{'アイテム':'ロンパース','キーワード1':'白い','キーワード2':'清潔感','キーワード3':'可愛さ','キーワード4':'お食い初め'},\
        'コーデ4':{'アイテム':'ロンパース','キーワード1':'白い','キーワード2':'清潔感','キーワード3':'可愛さ','キーワード4':'お食い初め'}},\
    }'"
    question = f"{question}　この２つの提案から４つのアイテム毎に、アイテム名とWeb上で検索する為のキーワードを単語で３つ以上抽出して下さい。{form}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": question},
        ],
        temperature=0,
    )
    answer = response.choices[0]["message"]["content"].strip()
    
    return answer

def convert_to_dict(GPT_ans):
    try:
        # シングルクォーテーションをダブルクォーテーションに変換
        GPT_ans = GPT_ans.replace("'", "\"")

        # 文字列を辞書型に変換
        return ast.literal_eval(GPT_ans)
    except Exception as e:
        print("変換エラー:", e)
        return None    
    
# <<<<<<<<<< 楽天アフィリ系関数 <<<<<<<<<<
def find_smallest_non_zero_value(lst):
    # ゼロを除外してリスト内の非ゼロの最小値を取得
    non_zero_values = [x for x in lst if x != 0]
    
    # 非ゼロの最小値を取得
    min_non_zero_value = min(non_zero_values)

    # 最小値のインデックスを取得
    index_of_min_non_zero_value = lst.index(min_non_zero_value)

    return index_of_min_non_zero_value    

def find_max_value(lst):
    # 最大値を取得
    max_value = max(lst)

    # 最大値のインデックスを取得
    index_of_max_value = lst.index(max_value)

    return index_of_max_value

def rakuten_API(keywords):
    
    # 楽天市場商品検索APIのURL
    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
    # URLのパラメータ
    param = {
        # 前手順で取得したアプリIDを設定する
        "applicationId" : "1098909885514131418",
        "affiliateId" : "340fd0f3.76baf9d5.00000000.deb18cc6",
        "format" : "json",
        "keyword" : keywords,
        "genreId" : 100533,
        "sort":"-reviewAverage"
    }

    # APIを実行して結果を取得する
    result = requests.get(url, param)
    # jsonにでコード     
    result = result.json()

    return result


def rakuten(dict_GPT_ans):    
    # アイテム名＋キーワードで検索数を調査
    hits_nums_taian = []
    for teian in TEIANS:
        # コーデ事
        hits_nums_coord = []    
        for coord in COORDS:
            # キーワード毎             
            hits_nums_keyword = []  
            for i in range(0,3):    
                param_keyword = f"{dict_GPT_ans[teian][coord]['アイテム']} {dict_GPT_ans[teian][coord][KEYWORDS[i]]}"
                result = rakuten_API(param_keyword)
                hits_nums_keyword.append(result["count"])
                time.sleep(0.5)
                
            hits_nums_coord.append(hits_nums_keyword)
        hits_nums_taian.append(hits_nums_coord)

        
    # 検索アイテムの絞込み
    Final_result = {TEIANS[0]:{},TEIANS[1]:{}}
    # Final_result = {TEIANS[0]:{},TEIANS[1]:{},TEIANS[2]:{}}
    for teian_No,teian in enumerate(TEIANS):
        for coord_No,coord in enumerate(COORDS):
            min_index = find_smallest_non_zero_value(hits_nums_taian[teian_No][coord_No])
            max_index = find_max_value(hits_nums_taian[teian_No][coord_No])
            
            finish_flag = 1
            keyword_cnt = 1
            while finish_flag:
                if keyword_cnt == 1:
                    param_keyword = f"{dict_GPT_ans[teian][coord]['アイテム']} {dict_GPT_ans[teian][coord][KEYWORDS[0]]} {dict_GPT_ans[teian][coord][KEYWORDS[1]]} {dict_GPT_ans[teian][coord][KEYWORDS[2]]}"
                elif keyword_cnt == 2:
                    param_keyword = f"{dict_GPT_ans[teian][coord]['アイテム']} {dict_GPT_ans[teian][coord][KEYWORDS[min_index]]} {dict_GPT_ans[teian][coord][KEYWORDS[max_index]]}"
                elif keyword_cnt == 3:
                    param_keyword = f"{dict_GPT_ans[teian][coord]['アイテム']} {dict_GPT_ans[teian][coord][KEYWORDS[min_index]]}"
                else:
                    param_keyword = f"{dict_GPT_ans[teian][coord]['アイテム']}"
                    finish_flag = 0
                    
                result = rakuten_API(param_keyword)
                if result["count"] != 0:
                    finish_flag = 0
                time.sleep(0.5)
                keyword_cnt = keyword_cnt + 1
                Final_result[teian][coord] = result
                
    return Final_result

def rakuten_URL(result,dict_GPT_ans):
    display_text = []
    for teian in TEIANS:
        display_text.append(f"■{teian}")
        for coord in COORDS:
            ITEM_NAME = dict_GPT_ans[teian][coord]['アイテム']
            ITEM_PRICE = result[teian][coord]["Items"][0]["Item"]['itemPrice']
            AFFILI_URL = result[teian][coord]["Items"][0]["Item"]['affiliateUrl']
            # ITEM_IMG = result[teian][coord]["Items"][0]["Item"]['mediumImageUrls'][0]["imageUrl"]
            text = f"{ITEM_NAME}({ITEM_PRICE}円) \n {AFFILI_URL} \n"
            display_text.append(text)

    # 改行で繋げる
    result = "\n".join(display_text)

    return result

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

        # if st.button("もう一度相談する"):
        #     st.experimental_rerun()

if __name__ == "__main__":
    main()  