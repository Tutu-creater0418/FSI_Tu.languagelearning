import streamlit as st
import streamlit.components.v1 as components
from srs_logic import fsi_coach

st.set_page_config(page_title="免費版 FSI 教練", page_icon="🎤")

st.title("🎤 FSI 高強度教練 ")
st.caption("使用瀏覽器內建語音引擎，不消耗任何 API 點數")

# 獲取當前練習語塊
current_data = fsi_coach.get_next_chunk()
phrase = current_data["phrase"]
ipa = current_data["ipa"]

# 介面顯示區
st.info(f"### 當前句型：{phrase}")
st.write(f"**音標：** {ipa}")

st.markdown("---")
st.subheader("點擊按鈕開始 3 秒挑戰")

speech_js = f"""
<script>
    const msg = new SpeechSynthesisUtterance("{phrase}");
    const recognition = new (window.webkitSpeechRecognition || window.SpeechRecognition)();
    recognition.lang = 'en-US';
    
    function startDrill() {{
        window.speechSynthesis.speak(msg);
        
        msg.onend = () => {{
            recognition.start();
            let timer = setTimeout(() => {{
                recognition.stop();
                alert("太慢了！加快速度！");
            }}, 3000);

            recognition.onresult = (event) => {{
                clearTimeout(timer);
                const result = event.results[0][0].transcript;
                alert("你說了: " + result);
            }};
        }};
    }}
</script>
<button onclick="startDrill()" style="padding: 15px 30px; font-size: 20px; cursor: pointer;">
    開始訓練 (Substitution Drill)
</button>
"""

# 使用 iframe 方式嵌入語音引擎
st.iframe(f"data:text/html;charset=utf-8,{speech_js}", height=200)

st.sidebar.write("### 練習狀態")
st.sidebar.write(f"目前箱子：箱子 1")