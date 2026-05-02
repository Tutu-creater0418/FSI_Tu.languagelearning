# app.py
import streamlit as st
import random
from srs_logic import fsi_coach

st.set_page_config(page_title="FSI 西語教練", page_icon="🎤")

# --- 初始化狀態 ---
if "active" not in st.session_state:
    st.session_state.active = False
if "current_chunk" not in st.session_state:
    st.session_state.current_chunk = None
if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = None

st.title("🎤 FSI 高強度西語教練")
st.caption("示範句播放後，請在 5 秒內完成替換句子")

# --- 按鈕控制區 ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 開始練習 / 下一題", use_container_width=True):
        st.session_state.active = True
        chunk = fsi_coach.get_next_chunk()
        st.session_state.current_chunk = chunk
        st.session_state.current_prompt = random.choice(chunk["prompts"])
        st.rerun()
with col2:
    if st.button("⏹️ 結束練習", use_container_width=True, type="primary"):
        st.session_state.active = False
        st.session_state.current_chunk = None
        st.rerun()

st.markdown("---")

if st.session_state.active and st.session_state.current_chunk:
    chunk = st.session_state.current_chunk
    prompt_data = st.session_state.current_prompt
    # 組合正確答案
    full_answer = chunk['phrase'].replace("...", "") + " " + prompt_data['word']

    # 1. 顯示練習資訊 (含中文意思)
    st.info(f"### 當前句型：{chunk['phrase']}\n**意思：{chunk['meaning']}**")
    st.write(f"**音標：** {chunk['ipa']}")
    st.warning(f"**🔥 請替換為：{prompt_data['word']} ({prompt_data['meaning']})**")

    # 2. JavaScript 語音流程
    # 流程：唸示範句 -> 結束後唸提示詞 -> 啟動錄音並開始 5 秒倒數
    speech_js = f"""
    <script>
        const demoMsg = new SpeechSynthesisUtterance("{chunk['phrase']}");
        const promptMsg = new SpeechSynthesisUtterance("{prompt_data['word']}");
        demoMsg.lang = promptMsg.lang = 'es-ES';
        
        const recognition = new (window.webkitSpeechRecognition || window.SpeechRecognition)();
        recognition.lang = 'es-ES';
        
        function startDrill() {{
            // 第一步：唸示範句
            window.speechSynthesis.speak(demoMsg);
            
            demoMsg.onend = () => {{
                // 第二步：示範完，唸提示詞
                window.speechSynthesis.speak(promptMsg);
                
                promptMsg.onend = () => {{
                    // 第三步：提示詞唸完，開始辨識與 5 秒倒數
                    recognition.start();
                    let timer = setTimeout(() => {{
                        recognition.stop();
                        alert("超過五秒了！！\\n正確答案是：{full_answer}");
                    }}, 5000);

                    recognition.onresult = (event) => {{
                        clearTimeout(timer);
                        const result = event.results[0][0].transcript;
                        alert("完成！\\n妳說： " + result + "\\n答案：{full_answer}");
                    }};
                }};
            }};
        }}
    </script>
    <button onclick="startDrill()" style="padding: 20px; font-size: 20px; border-radius: 10px; cursor: pointer; width: 100%; background-color: #f0f2f6; border: 2px solid #e0e0e0;">
        🎤 聽示範並開始挑戰 (5 秒內回答)
    </button>
    """
    st.iframe(f"data:text/html;charset=utf-8,{speech_js}", height=120)

    # 3. 答案與繼續按鈕區
    with st.expander("💡 點擊查看正確答案與下一題"):
        st.success(f"完整正確句子：{full_answer}")
        if st.button("➡️ 繼續 (下一題)"):
            # 點擊按鈕重抽題目並重整
            chunk = fsi_coach.get_next_chunk()
            st.session_state.current_chunk = chunk
            st.session_state.current_prompt = random.choice(chunk["prompts"])
            st.rerun()

else:
    st.write("教練待命中... 請點擊上方「開始練習」按鈕。")