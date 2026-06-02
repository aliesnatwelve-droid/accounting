import streamlit as st
import time
import streamlit_calendar
# تنظیم صفحه - حذف سایدبار
st.set_page_config(page_title= "قشنگ ترینننمم", page_icon="🕯️", initial_sidebar_state="collapsed")

# مخفی کردن سایدبار با CSS
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="stSidebarCollapsedControl"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# مقداردهی اولیه
if "is_lit" not in st.session_state:
    st.session_state.is_lit = True
if "show_celebration" not in st.session_state:
    st.session_state.show_celebration = False
if "prev_state" not in st.session_state:
    st.session_state.prev_state = True
if "celebration_started" not in st.session_state:
    st.session_state.celebration_started = False

# بررسی تغییر وضعیت شمع
if st.session_state.is_lit != st.session_state.prev_state and not st.session_state.is_lit:
    st.session_state.show_celebration = True
    st.session_state.prev_state = st.session_state.is_lit
    st.session_state.celebration_started = True

# نمایش بادکنک‌ها و پنهان کردن همه چیز
if st.session_state.show_celebration and not st.session_state.is_lit:
    # پنهان کردن همه محتوا با CSS
    st.markdown("""
        <style>
            .main > div {
                display: none;
            }
            .celebration-message {
                display: block !important;
                text-align: center;
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 9999;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 40px 60px;
                border-radius: 30px;
                color: white;
                font-size: 36px;
                font-weight: bold;
                box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                animation: zoomIn 0.5s ease-out;
            }
            @keyframes zoomIn {
                from {
                    transform: translate(-50%, -50%) scale(0.3);
                    opacity: 0;
                }
                to {
                    transform: translate(-50%, -50%) scale(1);
                    opacity: 1;
                }
            }
            .balloon-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 10000;
            }
        </style>
        
        <div class="celebration-message">
            🎉تولد مبارک باشههههه عسلیییییی 🎉<br>

        </div>
    """, unsafe_allow_html=True)
    
    # نمایش بادکنک‌های متعدد
    for _ in range(5):
        st.balloons()
    
    time.sleep(20)
    st.session_state.show_celebration = False
    st.session_state.celebration_started = False
    st.rerun()

# فقط اگر جشن شروع نشده باشه، محتوا رو نشون بده
if not st.session_state.celebration_started:
    # نمایش عکس
    try:
        st.image('download.png')
    except:
    #     st.markdown("🎂"
        ''
    
    # سه ستون برای وسط‌چین شدن
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.session_state.is_lit:
            # شمع روشن با CSS ساده و هوور
            st.markdown("""
                <style>
                    .candle-container {
                        display: flex;
                        justify-content: center;
                        margin: 30px 0;
                    }
                    .candle {
                        position: relative;
                        width: 120px;
                        height: 170px;
                        transition: transform 0.3s ease;
                    }
                    .candle:hover {
                        transform: scale(1.05);
                    }
                    .candle-body {
                        width: 100%;
                        height: 100%;
                        background: linear-gradient(145deg, #fdf4e3, #f0e0c8);
                        border-radius: 35px 35px 15px 15px;
                        box-shadow: 0 0 40px 15px rgba(255, 120, 0, 0.6);
                        transition: box-shadow 0.3s ease;
                    }
                    .candle:hover .candle-body {
                        box-shadow: 0 0 60px 25px rgba(255, 120, 0, 0.8);
                    }
                    .candle-line {
                        width: 80%;
                        height: 2px;
                        background: #d4a574;
                        margin: 45px auto 0;
                        opacity: 0.5;
                    }
                    .candle-stars {
                        text-align: center;
                        padding-top: 35px;
                        font-size: 24px;
                        color: #c4956a;
                        opacity: 0.4;
                    }
                    .wick {
                        position: absolute;
                        bottom: 155px;
                        left: 58px;
                        width: 4px;
                        height: 15px;
                        background: #444;
                        border-radius: 2px;
                    }
                    .flame-outer {
                        position: absolute;
                        bottom: 175px;
                        left: 45px;
                        width: 30px;
                        height: 55px;
                        background: radial-gradient(ellipse, #ff6600, #ff3300);
                        border-radius: 50%;
                        filter: blur(3px);
                        animation: flicker 0.1s infinite;
                    }
                    .flame-middle {
                        position: absolute;
                        bottom: 178px;
                        left: 50px;
                        width: 20px;
                        height: 45px;
                        background: radial-gradient(ellipse, #ffcc00, #ff9900);
                        border-radius: 50%;
                        animation: flicker 0.12s infinite;
                    }
                    .flame-inner {
                        position: absolute;
                        bottom: 182px;
                        left: 55px;
                        width: 10px;
                        height: 30px;
                        background: radial-gradient(ellipse, white, #ffffaa);
                        border-radius: 50%;
                        animation: flicker 0.08s infinite;
                    }
                    @keyframes flicker {
                        0% { transform: scale(1); opacity: 1; }
                        50% { transform: scale(1.08); opacity: 0.9; }
                        100% { transform: scale(1); opacity: 1; }
                    }
                </style>
                
                <div class="candle-container">
                    <div class="candle">
                        <div class="candle-body">
                            <div class="candle-line"></div>
                            <div class="candle-stars">✦ ✦</div>
                        </div>
                        <div class="wick"></div>
                        <div class="flame-outer"></div>
                        <div class="flame-middle"></div>
                        <div class="flame-inner"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            
            if st.button("فوووووتتتتتت کنننن", use_container_width=True, type="primary"):
                st.session_state.is_lit = False
                st.rerun()
            
        else:
            # شمع خاموش با هوور
            st.markdown("""
                <style>
                    .candle-container {
                        display: flex;
                        justify-content: center;
                        margin: 30px 0;
                    }
                    .candle {
                        position: relative;
                        width: 120px;
                        height: 170px;
                        transition: transform 0.3s ease;
                    }
                    .candle:hover {
                        transform: scale(1.05);
                    }
                    .candle-body-off {
                        width: 100%;
                        height: 100%;
                        background: linear-gradient(145deg, #e8ddce, #d4c8b8);
                        border-radius: 35px 35px 15px 15px;
                        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                    }
                    .candle-line-off {
                        width: 80%;
                        height: 2px;
                        background: #b8a88a;
                        margin: 45px auto 0;
                        opacity: 0.5;
                    }
                    .candle-stars-off {
                        text-align: center;
                        padding-top: 35px;
                        font-size: 24px;
                        color: #a89878;
                        opacity: 0.4;
                    }
                    .wick-off {
                        position: absolute;
                        bottom: 158px;
                        left: 58px;
                        width: 4px;
                        height: 10px;
                        background: #333;
                        border-radius: 2px;
                    }
                    .smoke1 {
                        position: absolute;
                        bottom: 175px;
                        left: 56px;
                        width: 8px;
                        height: 8px;
                        background: rgba(150,150,150,0.4);
                        border-radius: 50%;
                        animation: smoke 3s infinite ease-out;
                    }
                    .smoke2 {
                        position: absolute;
                        bottom: 185px;
                        left: 55px;
                        width: 10px;
                        height: 10px;
                        background: rgba(150,150,150,0.25);
                        border-radius: 50%;
                        animation: smoke 3.5s infinite ease-out 1s;
                    }
                    @keyframes smoke {
                        0% {
                            transform: translateY(0) scale(1);
                            opacity: 0.5;
                        }
                        100% {
                            transform: translateY(-50px) scale(2.5);
                            opacity: 0;
                        }
                    }
                </style>
                
                <div class="candle-container">
                    <div class="candle">
                        <div class="candle-body-off">
                            <div class="candle-line-off"></div>
                            <div class="candle-stars-off">✦ ✦</div>
                        </div>
                        <div class="wick-off"></div>
                        <div class="smoke1"></div>
                        <div class="smoke2"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("فوووووتتتتتت کنننن", use_container_width=True, type="primary"):
                st.session_state.is_lit = True
                st.rerun()