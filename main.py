import streamlit as st
import datetime
import json
from streamlit_js_eval import streamlit_js_eval

# ---------------------------------------------------------
# 1. 페이지 설정 및 커스텀 CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="기프티콘 알리미",
    page_icon="🎁",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Jua&display=swap');
    
    /* 전체 배경: 따뜻하고 부드러운 크림 브라운/아이보리 톤 */
    html, body, [class*="css"], .stApp {
        font-family: 'Gowun Dodum', sans-serif !important;
        background-color: #FAF8F5 !important;
        color: #4A403A !important;
    }

    /* 메인 타이틀 */
    .title-text {
        font-family: 'Jua', sans-serif !important;
        font-size: 3rem;
        color: #5C4B43;
        text-align: center;
        margin-top: 25px;
        margin-bottom: 20px;
        letter-spacing: 1px;
    }

    /* 서브 타이틀 헤더 */
    .section-title {
        font-family: 'Jua', sans-serif !important;
        font-size: 1.8rem;
        color: #5C4B43;
        text-align: center;
        margin-bottom: 20px;
    }

    /* 시작 화면 알림 요약 상자 */
    .home-alert-box {
        background-color: #FFF2F2;
        border: 2px solid #FFB3BA;
        border-radius: 20px;
        padding: 18px 22px;
        margin-bottom: 25px;
        box-shadow: 0px 4px 12px rgba(255, 179, 186, 0.25);
    }
    .home-alert-title {
        font-family: 'Jua', sans-serif;
        font-size: 1.25rem;
        color: #FF5252;
        margin-bottom: 8px;
    }
    .home-alert-item {
        font-size: 0.98rem;
        color: #5C4B43;
        margin: 6px 0;
    }

    /* 버튼 스타일 */
    .stButton > button {
        width: 100%;
        background-color: #FFFFFF !important;
        color: #5C4B43 !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        border-radius: 18px !important;
        border: 2px solid #EFEAE4 !important;
        padding: 12px 20px !important;
        box-shadow: 0px 4px 12px rgba(160, 140, 125, 0.08) !important;
        transition: all 0.2s ease-in-out !important;
    }

    .stButton > button:hover {
        background-color: #FFFDF9 !important;
        border-color: #FFB3BA !important;
        color: #FF7B89 !important;
        transform: translateY(-2px);
    }

    /* 기프티콘 카드 */
    .gifticon-card {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 12px;
        border: 2px solid #F2ECE4;
        box-shadow: 0px 6px 15px rgba(210, 195, 180, 0.12);
        position: relative;
    }

    .gifticon-card.urgent {
        border: 2px solid #FFB3BA;
        background-color: #FFF9F9;
    }

    /* 카테고리 뱃지 */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .badge-restaurant { background-color: #FFDFBA; color: #8F5513; }
    .badge-dessert { background-color: #FFB3BA; color: #8E2A37; }
    .badge-cafe { background-color: #E2F0CB; color: #3E6613; }
    .badge-cvs { background-color: #BAE1FF; color: #18507A; }
    .badge-etc { background-color: #E8DFF5; color: #533B78; }

    /* D-Day 뱃지 */
    .d-day-badge {
        float: right;
        font-family: 'Jua', sans-serif;
        font-size: 1.1rem;
        color: #FF6B6B;
        background-color: #FFE3E3;
        padding: 4px 12px;
        border-radius: 12px;
    }

    .d-day-normal {
        float: right;
        font-family: 'Jua', sans-serif;
        font-size: 1.1rem;
        color: #70A1FF;
        background-color: #E8F0FE;
        padding: 4px 12px;
        border-radius: 12px;
    }

    label, p, span, .stRadio p, .stCheckbox p {
        color: #5C4B43 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. LocalStorage 연동 및 Session State 초기화
# ---------------------------------------------------------

stored_gifticons = streamlit_js_eval(js_expressions='localStorage.getItem("gifticons")', key='get_gifticons')
stored_notify_options = streamlit_js_eval(js_expressions='localStorage.getItem("notify_options")', key='get_notify')

if 'gifticons' not in st.session_state:
    if stored_gifticons and stored_gifticons != "null":
        st.session_state.gifticons = json.loads(stored_gifticons)
    else:
        st.session_state.gifticons = []

if 'notify_options' not in st.session_state:
    if stored_notify_options and stored_notify_options != "null":
        st.session_state.notify_options = json.loads(stored_notify_options)
    else:
        st.session_state.notify_options = ["일주일 전"]

if 'current_page' not in st.session_state:
    st.session_state.current_page = "start"

if 'editing_index' not in st.session_state:
    st.session_state.editing_index = None

def save_to_local_storage():
    data_json = json.dumps(st.session_state.gifticons)
    notify_json = json.dumps(st.session_state.notify_options)
    streamlit_js_eval(js_expressions=f'localStorage.setItem("gifticons", JSON.dumps({data_json}))')
    streamlit_js_eval(js_expressions=f'localStorage.setItem("notify_options", JSON.dumps({notify_json}))')

def set_page(page_name):
    st.session_state.current_page = page_name
    st.session_state.editing_index = None

def get_notify_days(options):
    days = []
    if "한 달 전" in options:
        days.append(30)
    if "보름 전" in options:
        days.append(15)
    if "일주일 전" in options:
        days.append(7)
    return days

# ---------------------------------------------------------
# 3. 화면별 구현
# ---------------------------------------------------------

# ===== [시작 화면] =====
if st.session_state.current_page == "start":
    st.markdown("<div class='title-text'>🎁 기프티콘 알리미</div>", unsafe_allow_html=True)
    
    today = datetime.date.today()
    notify_days_list = get_notify_days(st.session_state.notify_options)
    
    urgent_items = []
    for item in st.session_state.gifticons:
        exp_date = datetime.datetime.strptime(item["expiry"], "%Y-%m-%d").date()
        d_day = (exp_date - today).days
        
        matched = []
        if 30 in notify_days_list and d_day <= 30:
            matched.append("한 달 전")
        if 15 in notify_days_list and d_day <= 15:
            matched.append("보름 전")
        if 7 in notify_days_list and d_day <= 7:
            matched.append("일주일 전")
            
        if len(matched) > 0 and d_day >= 0:
            urgent_items.append((item, d_day))

    # 시작 화면 알림창 (알림 대상 항목 전체 출력)
    if urgent_items:
        urgent_items.sort(key=lambda x: x[1])
        
        items_html = ""
        for item, d_day in urgent_items:
            d_day_str = "오늘 만료!" if d_day == 0 else f"D-{d_day}"
            items_html += f"<div class='home-alert-item'>• <b>[{item['category']}] {item['menu']}</b> — <span style='color:#FF5252; font-weight:bold;'>{d_day_str}</span></div>"

        st.markdown(f"""
            <div class="home-alert-box">
                <div class="home-alert-title">⏰ 만료 임박 기프티콘 알림 ({len(urgent_items)}건)</div>
                {items_html}
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✨ 새 기프티콘 추가"):
            set_page("add")
            st.rerun()
    with col2:
        if st.button("📜 내 기프티콘"):
            set_page("list")
            st.rerun()
    with col3:
        if st.button("🔔 알림 설정"):
            set_page("settings")
            st.rerun()

# ===== [새 기프티콘 추가 화면] =====
elif st.session_state.current_page == "add":
    st.markdown("<div class='section-title'>✨ 새 기프티콘 추가</div>", unsafe_allow_html=True)

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
    if st.button("💾 저장하기"):
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
                st.success("기프티콘이 성공적으로 저장되었습니다! 🎉")
                set_page("list")
                st.rerun()
            except ValueError:
                st.error("유효하지 않은 날짜입니다. 연/월/일을 다시 확인해주세요.")

    st.write("")
    if st.button("← 돌아가기"):
        set_page("start")
        st.rerun()

# ===== [내 기프티콘 화면] =====
elif st.session_state.current_page == "list":
    st.markdown("<div class='section-title'>📜 내 기프티콘 목록</div>", unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🏷️ 종류별"):
            st.session_state.filter_mode = "category"
    with col_btn2:
        if st.button("📅 날짜순"):
            st.session_state.filter_mode = "date"

    if 'filter_mode' not in st.session_state:
        st.session_state.filter_mode = "date"

    today = datetime.date.today()
    indexed_gifticons = list(enumerate(st.session_state.gifticons))

    if st.session_state.filter_mode == "date":
        indexed_gifticons.sort(key=lambda x: datetime.datetime.strptime(x[1]["expiry"], "%Y-%m-%d").date())

    elif st.session_state.filter_mode == "category":
        st.write("")
        st.write("**카테고리 선택**")
        selected_cat = st.radio("카테고리 선택", ["식당", "디저트", "카페", "편의점", "기타"], horizontal=True, label_visibility="collapsed")
        indexed_gifticons = [x for x in indexed_gifticons if x[1]["category"] == selected_cat]

    st.write("---")

    notify_days_list = get_notify_days(st.session_state.notify_options)

    if not indexed_gifticons:
        st.info("등록된 기프티콘이 없어요 🎈")
    else:
        badge_map = {
            "식당": "badge-restaurant",
            "디저트": "badge-dessert",
            "카페": "badge-cafe",
            "편의점": "badge-cvs",
            "기타": "badge-etc"
        }

        for real_idx, item in indexed_gifticons:
            exp_date = datetime.datetime.strptime(item["expiry"], "%Y-%m-%d").date()
            d_day = (exp_date - today).days

            matched_notifs = []
            if 30 in notify_days_list and d_day <= 30:
                matched_notifs.append("한 달 전")
            if 15 in notify_days_list and d_day <= 15:
                matched_notifs.append("보름 전")
            if 7 in notify_days_list and d_day <= 7:
                matched_notifs.append("일주일 전")

            is_urgent = len(matched_notifs) > 0
            card_class = "gifticon-card urgent" if is_urgent else "gifticon-card"

            if d_day > 0:
                d_day_html = f"<span class='d-day-badge'>D-{d_day}</span>" if is_urgent else f"<span class='d-day-normal'>D-{d_day}</span>"
            elif d_day == 0:
                d_day_html = "<span class='d-day-badge'>D-Day!</span>"
            else:
                d_day_html = f"<span class='d-day-badge' style='background:#E0E0E0; color:#666;'>만료됨</span>"

            cat_class = badge_map.get(item['category'], 'badge-etc')

            st.markdown(f"""
                <div class="{card_class}">
                    {d_day_html}
                    <span class="badge {cat_class}">{item['category']}</span>
                    <h3 style='margin:4px 0 8px 0; color:#5C4B43; font-size: 1.3rem;'>{item['menu']}</h3>
                    <p style='margin:0; color:#8C7A6B; font-size:0.95rem;'>
                        💵 <b>{item['price']:,}원</b> &nbsp;|&nbsp; 📆 ~{item['expiry']}까지
                    </p>
                </div>
            """, unsafe_allow_html=True)

            if is_urgent and d_day >= 0:
                highest_notif = matched_notifs[0]
                st.warning(f"⏰ [{highest_notif}] 알림 기준 범위 내에 있어요! (만료까지 {d_day}일 남음)")

            col_edit, col_del = st.columns([1, 1])
            with col_edit:
                if st.button("✏️ 수정", key=f"edit_btn_{real_idx}"):
                    if st.session_state.editing_index == real_idx:
                        st.session_state.editing_index = None
                    else:
                        st.session_state.editing_index = real_idx
                    st.rerun()

            with col_del:
                if st.button("🗑️ 삭제", key=f"del_btn_{real_idx}"):
                    st.session_state.gifticons.pop(real_idx)
                    save_to_local_storage()
                    st.session_state.editing_index = None
                    st.success(f"'{item['menu']}' 기프티콘이 삭제되었습니다.")
                    st.rerun()

            if st.session_state.editing_index == real_idx:
                with st.expander("📝 정보 수정하기", expanded=True):
                    categories = ["식당", "디저트", "카페", "편의점", "기타"]
                    cat_idx = categories.index(item["category"]) if item["category"] in categories else 0
                    
                    edit_category = st.radio("종류", categories, index=cat_idx, key=f"edit_cat_{real_idx}", horizontal=True)
                    edit_menu = st.text_input("메뉴명", value=item["menu"], key=f"edit_menu_{real_idx}")
                    edit_price = st.text_input("가격", value=str(item["price"]), key=f"edit_price_{real_idx}")

                    curr_date = datetime.datetime.strptime(item["expiry"], "%Y-%m-%d").date()
                    col_ey, col_em, col_ed = st.columns(3)
                    with col_ey:
                        edit_y = st.selectbox("연도", list(range(today.year, today.year + 6)), index=max(0, curr_date.year - today.year), key=f"ey_{real_idx}")
                    with col_em:
                        edit_m = st.selectbox("월", list(range(1, 13)), index=curr_date.month - 1, key=f"em_{real_idx}")
                    with col_ed:
                        edit_d = st.selectbox("일", list(range(1, 32)), index=min(curr_date.day - 1, 30), key=f"ed_{real_idx}")

                    col_save_edit, col_cancel_edit = st.columns(2)
                    with col_save_edit:
                        if st.button("💾 수정 완료", key=f"save_edit_{real_idx}"):
                            if not edit_menu.strip():
                                st.error("메뉴 이름을 입력해주세요.")
                            elif not str(edit_price).isdigit():
                                st.error("가격은 숫자로만 입력해주세요.")
                            else:
                                try:
                                    new_exp = datetime.date(edit_y, edit_m, edit_d).strftime("%Y-%m-%d")
                                    st.session_state.gifticons[real_idx] = {
                                        "category": edit_category,
                                        "menu": edit_menu,
                                        "price": int(edit_price),
                                        "expiry": new_exp
                                    }
                                    save_to_local_storage()
                                    st.session_state.editing_index = None
                                    st.success("수정되었습니다!")
                                    st.rerun()
                                except ValueError:
                                    st.error("유효하지 않은 날짜입니다.")

                    with col_cancel_edit:
                        if st.button("❌ 취소", key=f"cancel_edit_{real_idx}"):
                            st.session_state.editing_index = None
                            st.rerun()

            st.write("")

    st.write("")
    if st.button("← 돌아가기"):
        set_page("start")
        st.rerun()

# ===== [알림 설정 화면] =====
elif st.session_state.current_page == "settings":
    st.markdown("<div class='section-title'>🔔 알림 설정</div>", unsafe_allow_html=True)
    st.write("<p style='text-align: center; color: #8C7A6B;'>알림을 받고 싶은 시기를 체크해 주세요 (중복 가능)</p>", unsafe_allow_html=True)
    st.write("")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        check_month = st.checkbox("한 달 전 (30일)", value="한 달 전" in st.session_state.notify_options)
    with col2:
        check_half = st.checkbox("보름 전 (15일)", value="보름 전" in st.session_state.notify_options)
    with col3:
        check_week = st.checkbox("일주일 전 (7일)", value="일주일 전" in st.session_state.notify_options)

    selected_options = []
    if check_month:
        selected_options.append("한 달 전")
    if check_half:
        selected_options.append("보름 전")
    if check_week:
        selected_options.append("일주일 전")

    st.session_state.notify_options = selected_options

    st.write("")
    if st.button("💾 설정 저장"):
        save_to_local_storage()
        st.success("알림 설정이 저장되었습니다!")

    st.write("---")
    if selected_options:
        st.info(f"선택된 알림 시기: **{', '.join(selected_options)}**")
    else:
        st.warning("선택된 알림 시기가 없습니다.")

    st.write("")
    if st.button("← 돌아가기"):
        set_page("start")
        st.rerun()
