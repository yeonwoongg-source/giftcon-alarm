streamlit
google-genai

gifticon-notifier/
├── .streamlit/
│   └── config.toml      # 남색 배경 theme 설정
├── app.py               # Streamlit 메인 앱 코드
├── requirements.txt     # 필요 라이브러리 목록
└── README.md            # 프로젝트 설명서

streamlit>=1.28.0
streamlit-local-storage>=0.0.1

[theme]
primaryColor = "#4A90E2"
backgroundColor = "#1E2A38"       # 남색 배경
secondaryBackgroundColor = "#2C3E50"
textColor = "#FFFFFF"            # 흰색 글씨
font = "sans serif"

import streamlit as st
import datetime

# 페이지 기본 설정
st.set_page_config(page_title="기프티콘 알리미", page_icon="🎁", layout="centered")

# Custom CSS 적용 (동글동글한 흰색 폰트 및 스타일링)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Gowun Dodum', sans-serif;
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: bold;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #FFFFFF;
        color: #1E2A38;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #F0F0F0;
        color: #1E2A38;
    }
    </style>
""", unsafe_allow_html=True)

# Session State 초기화 (로컬 데이터 유지)
if 'gifticons' not in st.session_state:
    st.session_state.gifticons = []
if 'notify_days' not in st.session_state:
    st.session_state.notify_days = 7
if 'page' not in st.session_state:
    st.session_state.page = "home"

# 네비게이션 함수
def go_to(page_name):
    st.session_state.page = page_name

# 1. 시작 화면
if st.session_state.page == "home":
    st.markdown("<div class='main-title'>기프티콘 알리미</div>", unsafe_allow_html=True)
    st.write("")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕ 새 기프티콘 추가"):
            go_to("add")
            st.rerun()
    with col2:
        if st.button("📜 내 기프티콘"):
            go_to("list")
            st.rerun()
    with col3:
        if st.button("🔔 알림 설정"):
            go_to("settings")
            st.rerun()

# 2. 새 기프티콘 추가 화면
elif st.session_state.page == "add":
    st.subheader("➕ 새 기프티콘 추가")
    
    category = st.selectbox("종류", ["식당", "디저트", "카페", "편의점", "기타"])
    menu = st.text_input("메뉴")
    price = st.number_input("가격", min_value=0, step=100)
    expiry_date = st.date_input("사용 기간", min_value=datetime.date.today())
    
    if st.button("저장하기"):
        if menu:
            new_item = {
                "category": category,
                "menu": menu,
                "price": price,
                "expiry": expiry_date
            }
            st.session_state.gifticons.append(new_item)
            st.success("기프티콘이 저장되었습니다!")
            go_to("list")
            st.rerun()
        else:
            st.warning("메뉴 이름을 입력해주세요.")
            
    if st.button("← 돌아가기"):
        go_to("home")
        st.rerun()

# 3. 내 기프티콘 화면
elif st.session_state.page == "list":
    st.subheader("📜 내 기프티콘 목록")
    
    sort_type = st.radio("정렬 방식", ["날짜순", "종류별"], horizontal=True)
    
    items = st.session_state.gifticons.copy()
    today = datetime.date.today()
    
    if sort_type == "날짜순":
        items.sort(key=lambda x: x["expiry"])
    elif sort_type == "종류별":
        selected_cat = st.selectbox("카테고리 선택", ["식당", "디저트", "카페", "편의점", "기타"])
        items = [item for item in items if item["category"] == selected_cat]
        
    st.write("---")
    
    if not items:
        st.info("등록된 기프티콘이 없습니다.")
    else:
        for idx, item in enumerate(items):
            d_day = (item["expiry"] - today).days
            
            # 알림 조건 체크
            is_warning = d_day <= st.session_state.notify_days
            status_text = f"D-{d_day}" if d_day > 0 else "D-Day (오늘 만료)" if d_day == 0 else "만료됨"
            
            with st.container():
                st.write(f"**[{item['category']}] {item['menu']}**")
                st.write(f"가격: {item['price']:,}원 | 만료일: {item['expiry']} ({status_text})")
                if is_warning and d_day >= 0:
                    st.warning(f"⚠️ 만료까지 {d_day}일 남았습니다!")
                st.write("---")
                
    if st.button("← 돌아가기"):
        go_to("home")
        st.rerun()

# 4. 알림 설정 화면
elif st.session_state.page == "settings":
    st.subheader("🔔 알림 설정")
    st.write("사용 기간이 얼마나 남았을 때 경고 표시를 할지 설정하세요.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("한 달 전 (30일)"):
            st.session_state.notify_days = 30
            st.success("알림 기준이 30일 전으로 설정되었습니다.")
    with col2:
        if st.button("보름 전 (15일)"):
            st.session_state.notify_days = 15
            st.success("알림 기준이 15일 전으로 설정되었습니다.")
    with col3:
        if st.button("일주일 전 (7일)"):
            st.session_state.notify_days = 7
            st.success("알림 기준이 7일 전으로 설정되었습니다.")
            
    st.info(f"현재 설정: 만료 **{st.session_state.notify_days}일 전** 알림")
    
    if st.button("← 돌아가기"):
        go_to("home")
        st.rerun()
