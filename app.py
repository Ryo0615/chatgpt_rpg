import g4f
import streamlit as st
import requests

system_message = """
あなたはRPGのゲームマスター専用チャットボットです。
チャットを通じて、ユーザーに楽しい本格ファンタジーRPG体験を提供します。

制約条件
* チャットボットはゲームマスター（以下GM）です。
* 人間のユーザーは、プレイヤーをロールプレイします。
* GMは、ゲーム内に登場するNPCのロールプレイも担当します。
* 各NPCはそれぞれの利害や目的を持ち、ユーザーに協力的とは限りません。
* GMは、必要に応じてユーザーの行動に難易度を示し、アクションを実行する場合には、2D6ダイスロールによる目標判定を行なってください。
* GMは、ユーザーが楽しめるよう、適度な難関を提供してください（不条理なものは禁止です）。
* GMは、ユーザーが無理な展開を要求した場合、その行為を拒否したり、失敗させることができます。
* GMは内部パラメーターとして「盛り上がり度」を持ちます。GMはゲーム展開が退屈だと判断した場合、盛り上がる展開を起こしてください。
* ゲームのスタート地点は、「王との謁見室」です。
* ゲームのクエスト内容は「自動設定」です。
* ダメージなどにより、ユーザーが行動不能になったら、ゲームオーバーです。

まずはじめに、ユーザーと一緒にキャラメイキングを行いましょう。
名前、種族、職業、特技、弱点をユーザーに聞いてください。
その後に、プロフィールに従って能力値（HP, MP, STR, VIT, AGI, DEX, INT, LUK）を決めてください。"
"""


def generate_g4f_response(messages: list) -> str:
    try:
        response_stream = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True
        )

        response = "".join([message for message in response_stream])
    except requests.HTTPError as e:
        st.markdown(f"{e} - {e.response.text}")
        return ""
    return response

def display_chat_message_from_assistant(messages):
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        for char in generate_g4f_response(messages):
            full_response += char
            message_placeholder.markdown(full_response + "❙")

        message_placeholder.markdown(full_response)

        return full_response

def main():
    st.title("-ˋˏ ChatGPT RPG ˎˊ- ")
    st.markdown("チャットを通じて、楽しくて本格的なファンタジーRPGを体験しよう！\n\nあなただけのキャラクターを作成し、冒険の旅に出かけましょう！")

    # Session state for first run
    if 'messages' not in st.session_state:
        # Input system message
        st.session_state.messages = [{"role": "system", "content": system_message}]

        # Display chat message from assistant
        full_response = display_chat_message_from_assistant([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages])
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Display chat messages from history on app rerun
    else:
        for message in st.session_state.messages:
            if message["role"] == "assistant" or message["role"] == "user":
                with st.chat_message(message["role"]):
                    st.markdown(f"{message['content']}")

    # Input for the user message
    user_message = st.chat_input("Your Message")

    if user_message:
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(f"{user_message}")
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_message})

        # Display chat message from assistant
        full_response = display_chat_message_from_assistant([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages])
        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()
