import streamlit as st
import random  
from srs_logic import fsi_coach

st.set_page_config(page_title="FSI 西語教練", page_icon="🎤")

# 初始化會話狀態 [cite: 136]
if "active" not in st.session_state:
    st.session_state.active = False

st.title("🎤 FSI 高強度西語教練")
st.caption("Substitution Drill：請在教練說完提示詞後 3 秒內完成句子")

# 啟動與結束按鈕控制 [cite: 136]
col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 開始練習", use_container_width=True):
        st.session_state.active = True
        st.rerun()
with col2:
    if st.button("⏹️ 結束/重置", use_container_width=True, type="primary"):
        st.session_state.active = False
        st.rerun()

st.markdown("---")

if st.session_state.active:
    # 2. 獲取資料並隨機挑選提示詞 [cite: 305, 312]
    current_data = fsi_coach.get_next_chunk()
    phrase = current_data["phrase"]
    ipa = current_data["ipa"]
    
    # 從資料庫的 prompts 清單中隨機選一個
    current_prompt = random.choice(current_data["prompts"]) 

    st.info(f"### 核心句型：{phrase}")
    st.write(f"**音標 (IPA)：** {ipa}")
    st.warning(f"**🔥 請替換此詞彙：{current_prompt}**") # 在畫面上顯示提示詞

    # 3. 更新 JavaScript：教練先唸提示詞，再聽妳回答 
    speech_js = f"""
    <script>
        const coachMsg = new SpeechSynthesisUtterance("{current_prompt}"); 
        coachMsg.lang = 'es-ES';
        
        const recognition = new (window.webkitSpeechRecognition || window.SpeechRecognition)();
        recognition.lang = 'es-ES';
        
        function startDrill() {{
            // 第一步：教練唸出提示詞 (例如: "abre hoy")
            window.speechSynthesis.speak(coachMsg);
            
            coachMsg.onend = () => {{
                // 第二步：唸完後立刻啟動辨識並開始 3 秒倒數 [cite: 11, 312]
                recognition.start();
                
                let timer = setTimeout(() => {{
                    recognition.stop();
                    alert("¡Demasiado lento! (太慢了！)");
                }}, 3000);

                recognition.onresult = (event) => {{
                    clearTimeout(timer);
                    const result = event.results[0][0].transcript;
                    alert("妳完成了句子：{phrase} " + result);
                }};
            }};
        }}
    </script>
    <button onclick="startDrill()" style="padding: 20px; font-size: 20px; border-radius: 10px; cursor: pointer; width: 100%; background-color: #f0f2f6;">
        🎤 點擊聽提示並挑戰 (3 秒內回答)
    </button>
    """
    
    st.iframe(f"data:text/html;charset=utf-8,{speech_js}", height=150)
    
    st.sidebar.markdown("### 練習狀態")
    st.sidebar.text("影子練習輔導：")
    st.sidebar.info(f"節奏：{phrase[:10]}...")
else:
    st.write("教練待命中... 請點擊上方「開始練習」按鈕。")