import streamlit as st
import datetime
import json
from streamlit_js_eval import streamlit_js_eval, set_cookie, get_cookie

# ---------------------------------------------------------
# 1. 페이지 설정 및 Custom CSS (남색 배경 및 흰색 라운드 버튼)
# ---------------------------------------------------------
st.set_page_config(
    page_title="기프티콘 알리미",
    page_icon="🎁",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* 구글 폰트 적용 (동글동글한 Gowun Dodum) */
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Gowun Dodum', sans-serif !important;
        background-color: #1b263b !important; /* 남색 배경 */
        color: #FFFFFF !important;
    }

    /* 시작 화면 타이틀 (남색 배경에 동글동글하고 두꺼운 흰색 글씨) */
    .title-text {
        font-size: 2.8rem;
        font-weight: 800;
        color: #FFFFFF;
        text-align: center;
        margin-top: 40px;
        margin-bottom: 40px;
        letter-spacing: -1px;
    }

    /* 버튼 스타일 (아기자기하고 얇은 느낌의 흰색 버튼) */
    .stButton > button {
        width: 100%;
        background-color: #FFFFFF !important;
        color: #1b263b !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        border-radius: 20px !important;
        border: none !important;
        padding: 12px 20px !important;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.2s ease-in-out !important;
    }

    .stButton > button:hover {
        background-color: #F0F4F8 !important;
        transform: translateY(-2px);
    }

    /* 카드 형태 카드 레이아웃 */
    .gifticon-card {
        background-color: #2b3a55;
        border-radius: 15px;
        padding: 18px;
        margin-bottom: 12px;
        border-left: 5px solid #4A90E2;
    }

    .gifticon-card.urgent {
        border-left: 5px solid #FF6B6B;
    }

    /* 라디오 버튼 및 입력 필드 흰색 텍스트 보장 */
    label, .stRadio p, .stSelectbox p {
        color: #FFFFFF !important;
        font-size: 1.05rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. LocalStorage 연동 및 Session State 초기화
# ---------------------------------------------------------

# 브라우저의 localStorage에서 기프티콘 데이터와 알림 설정 가져오기
stored_gifticons = streamlit_js_eval(js_expressions='localStorage.getItem("gifticons")', key='get_gifticons')
stored_notify_days = streamlit_js_eval(js_expressions='localStorage.getItem("notify_days")', key='get_notify')

if 'gifticons' not in st.session_state:
    if stored_gifticons and stored_gifticons != "null":
        st.session_state.gifticons = json.loads(stored_gifticons)
    else:
        st.session_state.gifticons = []

if 'notify_days' not in st.session_state:
    if stored_notify_days and stored_notify_days != "null":
        st.session_state.notify_days = int(stored_notify_days)
    else:
        st.session_state.notify_days = 7  # 기본값: 일주일 전 (7일)

if 'current_page' not in st.session_state:
    st.session_state.current_page = "start"

# 데이터를 LocalStorage에 저장하는 함수
def save_to_local_storage():
    data_json = json.dumps(st.session_state.gifticons)
    streamlit_js_eval(js_expressions=f'localStorage.setItem("gifticons", JSON.dumps({data_json}))')
    streamlit_js_eval(js_expressions=f'localStorage.setItem("notify_days", {st.session_state.notify_days})')

def set_page(page_name):
    st.session_state.current_page = page_name

# ---------------------------------------------------------
# 3. 화면별 구현
# ---------------------------------------------------------

# ===== [시작 화면] =====
if st.session_state.current_page == "start":
    st.markdown("<div class='title-text'>기프티콘 알리미</div>", unsafe_allow_html=True)
    st.write("")
    st.write("")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("새 기프티콘 추가"):
            set_page("add")
            st.rerun()
    with col2:
        if st.button("내 기프티콘"):
            set_page("list")
            st.rerun()
    with col3:
        if st.button("알림 설정"):
            set_page("settings")
            st.rerun()

# ===== [새 기프티콘 추가 화면] =====
elif st.session_state.current_page == "add":
    st.markdown("<h2 style='text-align: center; color: white;'>새 기프티콘 추가</h2>", unsafe_allow_html=True)
    st.write("")

    st.write("**종류**")
    category = st.radio("종류 선택", ["식당", "디저트", "카페", "편의점", "기타"], horizontal=True, label_visibility="collapsed")
    
    st.write("**메뉴**")
    menu = st.text_input("메뉴 입력", placeholder="메뉴 이름을 입력하세요", label_visibility="collapsed")
    
    st.write("**가격**")
    price = st.text_input("가격 입력", placeholder="예: 5000", label_visibility="collapsed")
    
    st.write("**사용 기간**")
    today = datetime.date.today()
    col_y, col_m, col_d = st.columns(3)
    
    with col_y:
        year = st.selectbox("연도", list(range(today.year, today.year + 6)), index=0)
    with col_m:
        month = st.selectbox("월", list(range(1, 13)), index=today.month - 1)
    with col_d:
        day = st.selectbox("일", list(range(1, 32)), index=min(today.day - 1, 30))

    st.write("")
    if st.button("저장"):
        if not menu.strip():
            st.error("메뉴 이름을 입력해주세요.")
        elif not price.isdigit():
            st.error("가격은 숫자로만 입력해주세요.")
        else:
            try:
                expiry_date = datetime.date(year, month, day)
                new_item = {
                    "category": category,
                    "menu": menu,
                    "price": int(price),
                    "expiry": expiry_date.strftime("%Y-%m-%d")
                }
                st.session_state.gifticons.append(new_item)
                save_to_local_storage()
                st.success("기프티콘이 저장되었습니다!")
                set_page("list")
                st.rerun()
            except ValueError:
                st.error("유효하지 않은 날짜입니다. 연/월/일을 다시 확인해주세요.")

    st.write("")
    if st.button("돌아가기"):
        set_page("start")
        st.rerun()

# ===== [내 기프티콘 화면] =====
elif st.session_state.current_page == "list":
    st.markdown("<h2 style='text-align: center; color: white;'>내 기프티콘 목록</h2>", unsafe_allow_html=True)
    st.write("")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("종류별"):
            st.session_state.filter_mode = "category"
    with col_btn2:
        if st.button("날짜순"):
            st.session_state.filter_mode = "date"

    if 'filter_mode' not in st.session_state:
        st.session_state.filter_mode = "date"

    today = datetime.date.today()
    display_list = st.session_state.gifticons.copy()

    # 날짜순 정렬
    if st.session_state.filter_mode == "date":
        display_list.sort(key=lambda x: datetime.datetime.strptime(x["expiry"], "%Y-%m-%d").date())

    # 종류별 필터링
    elif st.session_state.filter_mode == "category":
        st.write("")
        st.write("**카테고리 선택**")
        selected_cat = st.radio("카테고리 선택", ["식당", "디저트", "카페", "편의점", "기타"], horizontal=True, label_visibility="collapsed")
        display_list = [item for item in display_list if item["category"] == selected_cat]

    st.write("---")

    if not display_list:
        st.info("등록된 기프티콘이 없습니다.")
    else:
        for item in display_list:
            exp_date = datetime.datetime.strptime(item["expiry"], "%Y-%m-%d").date()
            d_day = (exp_date - today).days

            is_urgent = d_day <= st.session_state.notify_days
            card_class = "gifticon-card urgent" if is_urgent else "gifticon-card"

            if d_day > 0:
                d_day_str = f"D-{d_day}"
            elif d_day == 0:
                d_day_str = "D-Day (오늘 만료!)"
            else:
                d_day_str = f"만료됨 ({abs(d_day)}일 경과)"

            st.markdown(f"""
                <div class="{card_class}">
                    <h3 style='margin:0; color:#FFFFFF;'>[{item['category']}] {item['menu']}</h3>
                    <p style='margin:5px 0 0 0; color:#E0E0E0;'>
                        <b>가격:</b> {item['price']:,}원 | <b>사용 기간:</b> {item['expiry']} ({d_day_str})
                    </p>
                </div>
            """, unsafe_allow_html=True)

            if is_urgent and d_day >= 0:
                st.warning(f"⚠️ 설정한 알림 기준({st.session_state.notify_days}일 전)보다 만료가 임박했습니다!")

    st.write("")
    if st.button("돌아가기"):
        set_page("start")
        st.rerun()

# ===== [알림 설정 화면] =====
elif st.session_state.current_page == "settings":
    st.markdown("<h2 style='text-align: center; color: white;'>알림 설정</h2>", unsafe_allow_html=True)
    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("한 달 전"):
            st.session_state.notify_days = 30
            save_to_local_storage()
            st.success("한 달 전 알림으로 설정되었습니다.")

    with col2:
        if st.button("보름 전"):
            st.session_state.notify_days = 15
            save_to_local_storage()
            st.success("보름 전(15일 전) 알림으로 설정되었습니다.")

    with col3:
        if st.button("일주일 전"):
            st.session_state.notify_days = 7
            save_to_local_storage()
            st.success("일주일 전 알림으로 설정되었습니다.")

    st.write("---")
    st.info(f"현재 알림 설정: 사용 기간 만료 **{st.session_state.notify_days}일 전** 알림 표시")

    st.write("")
    if st.button("돌아가기"):
        set_page("start")
        st.rerun()
