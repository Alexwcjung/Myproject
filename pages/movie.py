def speak_button(text, key):
    safe_text = text.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
    components.html(
        f"""
        <button 
            onclick="speak_{key}()"
            style="
                background:#facc15;
                color:#111827;
                border:none;
                border-radius:12px;
                padding:8px 14px;
                font-weight:900;
                cursor:pointer;
                margin:6px 0 10px 0;
            "
        >
            🔊 듣기
        </button>

        <script>
        function speak_{key}() {{
            const text = "{safe_text}";
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = "en-US";
            utterance.rate = 0.82;
            utterance.pitch = 1.0;
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(utterance);
        }}
        </script>
        """,
        height=55
    )
