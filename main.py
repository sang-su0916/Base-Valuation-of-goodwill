import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="영업권 평가 시스템",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'company_data' not in st.session_state:
    st.session_state.company_data = {
        'name': '',
        'industry': '',
        'business_number': '',
        'financial_data': pd.DataFrame()
    }
if 'valuation_results' not in st.session_state:
    st.session_state.valuation_results = {}

# 사이드바 함수
def render_sidebar():
    with st.sidebar:
        st.image("https://via.placeholder.com/150x150.png?text=로고", width=150)
        st.title("영업권 평가 시스템")
        
        # 네비게이션 메뉴
        pages = {
            'home': '🏠 홈',
            'company_info': '📝 기업 정보 입력',
            'excess_earnings': '📊 초과이익법',
            'dcf': '💹 현금흐름할인법',
            'market_comparison': '🔍 시장가치비교법',
            'results': '📈 종합 결과',
            'report': '📑 보고서'
        }
        
        for page_id, page_name in pages.items():
            if st.button(page_name, key=f"nav_{page_id}"):
                st.session_state.current_page = page_id
                st.rerun()
        
        st.divider()
        st.caption("© 2023 영업권 평가 시스템")

# 홈 페이지
def home_page():
    st.title("영업권 평가 시스템에 오신 것을 환영합니다")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## 영업권이란?
        영업권은 기업의 순자산가치를 초과하는 가치로, 기업의 브랜드, 고객 관계, 기술력 등 무형의 가치를 포함합니다.
        기업 인수합병(M&A) 및 법인전환 과정에서 영업권의 가치 평가가 필수적입니다.
        
        ## 주요 평가 방법
        - **초과이익법**: 정상이익을 초과하는 이익을 계산하여 영업권 가치를 평가
        - **현금흐름할인법(DCF)**: 미래 예상 현금흐름을 현재가치화하여 평가
        - **시장가치비교법**: 유사 기업 비교를 통한 가치 산출
        
        ## 사용 방법
        1. 왼쪽 사이드바에서 원하는 평가 방법을 선택하세요.
        2. 기업 정보와 재무 데이터를 입력하세요.
        3. 평가 매개변수를 설정하고 계산하세요.
        4. 결과를 확인하고 보고서를 다운로드하세요.
        """)
        
        if st.button("시작하기", key="start_button"):
            st.session_state.current_page = 'company_info'
            st.rerun()
    
    with col2:
        st.image("https://via.placeholder.com/300x400.png?text=영업권+평가+예시", width=300)
        
        st.info("영업권 가치 평가는 기업의 현재와 미래 가치를 정확히 파악하는 데 중요합니다.")

# 기업 정보 입력 페이지
def company_info_page():
    st.title("기업 정보 입력")
    
    with st.form("company_info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("회사명", value=st.session_state.company_data.get('name', ''))
            business_number = st.text_input("사업자등록번호", value=st.session_state.company_data.get('business_number', ''))
        
        with col2:
            industries = ["제조업", "서비스업", "도소매업", "IT/소프트웨어", "금융업", "건설업", "기타"]
            industry = st.selectbox("산업군", options=industries, index=0 if not st.session_state.company_data.get('industry') else industries.index(st.session_state.company_data.get('industry')))
        
        st.subheader("재무 데이터 입력")
        
        # 샘플 데이터 생성 또는 기존 데이터 불러오기
        if not isinstance(st.session_state.company_data.get('financial_data'), pd.DataFrame) or st.session_state.company_data.get('financial_data').empty:
            years = [datetime.now().year - i for i in range(1, 6)]
            sample_data = {
                '연도': years,
                '매출액': [0] * 5,
                '영업이익': [0] * 5,
                '당기순이익': [0] * 5,
                '총자산': [0] * 5,
                '총부채': [0] * 5,
                '자본': [0] * 5
            }
            financial_data = pd.DataFrame(sample_data)
        else:
            financial_data = st.session_state.company_data.get('financial_data')
        
        # 편집 가능한 데이터프레임 (단순화된 버전)
        edited_df = st.data_editor(financial_data, use_container_width=True)
        
        submit_button = st.form_submit_button("저장")
        
        if submit_button:
            # 데이터 유효성 검사
            if not company_name:
                st.warning("회사명을 입력해주세요.")
            else:
                # 데이터 저장
                st.session_state.company_data = {
                    'name': company_name,
                    'industry': industry,
                    'business_number': business_number,
                    'financial_data': edited_df
                }
                st.success("기업 정보가 저장되었습니다!")
    
    # 데이터 업로드/다운로드 기능
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("데이터 업로드")
        uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.dataframe(df.head())
                if st.button("이 데이터로 사용하기"):
                    st.session_state.company_data['financial_data'] = df
                    st.success("데이터가 성공적으로 로드되었습니다!")
                    st.rerun()
            except Exception as e:
                st.error(f"파일 로딩 중 오류 발생: {e}")
    
    with col2:
        st.subheader("데이터 다운로드")
        if not st.session_state.company_data.get('financial_data').empty:
            csv = st.session_state.company_data.get('financial_data').to_csv(index=False)
            st.download_button(
                label="CSV로 다운로드",
                data=csv,
                file_name=f"{st.session_state.company_data.get('name', 'company')}_financial_data.csv",
                mime='text/csv'
            )

# 초과이익법 페이지
def excess_earnings_page():
    st.title("초과이익법 평가")
    
    # 기업 데이터 확인
    if st.session_state.company_data.get('name') == '':
        st.warning("기업 정보가 입력되지 않았습니다. 먼저 기업 정보를 입력해주세요.")
        if st.button("기업 정보 입력으로 이동"):
            st.session_state.current_page = 'company_info'
            st.rerun()
        return
    
    st.subheader(f"{st.session_state.company_data.get('name')} - 초과이익법 평가")
    
    # 초과이익법 파라미터 설정
    with st.form("excess_earnings_params"):
        st.subheader("평가 매개변수 설정")
        
        col1, col2 = st.columns(2)
        
        with col1:
            normal_roi = st.number_input("정상 자본수익률 (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
            excess_years = st.number_input("초과이익 인정연수", min_value=1, max_value=10, value=5)
        
        with col2:
            discount_rate = st.slider("할인율 (%)", min_value=5.0, max_value=30.0, value=12.0, step=0.5)
            weight_recent = st.checkbox("최근 연도에 가중치 부여", value=True)
        
        # 고급 설정
        with st.expander("고급 설정"):
            adjustment_factor = st.slider("조정 계수", min_value=0.5, max_value=1.5, value=1.0, step=0.1)
            industry_premium = st.number_input("산업 프리미엄 (%)", min_value=0.0, max_value=10.0, value=2.0, step=0.5)
        
        calculate_button = st.form_submit_button("평가 계산")
        
        if calculate_button:
            try:
                # 데이터 가져오기
                df = st.session_state.company_data.get('financial_data')
                
                # 계산 로직 (간단한 예시)
                avg_earnings = df['당기순이익'].mean()
                total_assets = df['총자산'].iloc[0]  # 최신 연도 사용
                
                normal_profit = total_assets * (normal_roi / 100)
                excess_profit = avg_earnings - normal_profit
                
                if excess_profit <= 0:
                    st.error("초과이익이 계산되지 않습니다. 평균 이익이 정상 이익보다 낮습니다.")
                    return
                
                # 현재가치 계산
                present_value = 0
                for year in range(1, excess_years + 1):
                    discount_factor = 1 / ((1 + discount_rate/100) ** year)
                    present_value += excess_profit * discount_factor
                
                # 조정
                present_value = present_value * adjustment_factor * (1 + industry_premium/100)
                
                # 결과 저장
                st.session_state.valuation_results['excess_earnings'] = {
                    'method': '초과이익법',
                    'value': present_value,
                    'parameters': {
                        'normal_roi': normal_roi,
                        'excess_years': excess_years,
                        'discount_rate': discount_rate,
                        'adjustment_factor': adjustment_factor,
                        'industry_premium': industry_premium
                    },
                    'details': {
                        'avg_earnings': avg_earnings,
                        'total_assets': total_assets,
                        'normal_profit': normal_profit,
                        'excess_profit': excess_profit
                    }
                }
                
                st.success("초과이익법 평가가 완료되었습니다!")
                
            except Exception as e:
                st.error(f"계산 중 오류가 발생했습니다: {e}")
    
    # 계산 결과 표시 (이미 계산된 경우)
    if 'excess_earnings' in st.session_state.valuation_results:
        result = st.session_state.valuation_results['excess_earnings']
        
        st.divider()
        st.subheader("평가 결과")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("영업권 평가액", f"{result['value']:,.0f}원")
            
            st.subheader("주요 매개변수")
            params_df = pd.DataFrame({
                '매개변수': ['정상 자본수익률', '초과이익 인정연수', '할인율', '조정 계수', '산업 프리미엄'],
                '값': [
                    f"{result['parameters']['normal_roi']}%",
                    f"{result['parameters']['excess_years']}년",
                    f"{result['parameters']['discount_rate']}%",
                    f"{result['parameters']['adjustment_factor']}",
                    f"{result['parameters']['industry_premium']}%"
                ]
            })
            st.dataframe(params_df, hide_index=True)
        
        with col2:
            # 계산 과정 표시
            with st.expander("상세 계산 과정", expanded=True):
                st.markdown(f"""
                #### 1. 기초 데이터
                - 평균 당기순이익: {result['details']['avg_earnings']:,.0f}원
                - 총자산: {result['details']['total_assets']:,.0f}원
                
                #### 2. 정상이익 계산
                - 정상이익 = 총자산 × 정상수익률
                - 정상이익 = {result['details']['total_assets']:,.0f} × {result['parameters']['normal_roi']}% = {result['details']['normal_profit']:,.0f}원
                
                #### 3. 초과이익 계산
                - 초과이익 = 평균이익 - 정상이익
                - 초과이익 = {result['details']['avg_earnings']:,.0f} - {result['details']['normal_profit']:,.0f} = {result['details']['excess_profit']:,.0f}원
                
                #### 4. 현재가치 계산
                - {result['parameters']['excess_years']}년 동안 초과이익의 현재가치 합계
                - 할인율: {result['parameters']['discount_rate']}%
                
                #### 5. 조정
                - 조정 계수: {result['parameters']['adjustment_factor']}
                - 산업 프리미엄: {result['parameters']['industry_premium']}%
                
                #### 최종 영업권 가치
                - **{result['value']:,.0f}원**
                """)
            
            # 간단한 차트
            years = list(range(1, result['parameters']['excess_years'] + 1))
            values = []
            for year in years:
                discount_factor = 1 / ((1 + result['parameters']['discount_rate']/100) ** year)
                value = result['details']['excess_profit'] * discount_factor
                values.append(value)
            
            fig = px.bar(
                x=years,
                y=values,
                labels={'x': '연도', 'y': '현재가치'},
                title='연도별 초과이익의 현재가치'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # 결과 페이지로 이동 버튼
        if st.button("종합 결과 페이지로 이동"):
            st.session_state.current_page = 'results'
            st.rerun()

# 현금흐름할인법 페이지 (간소화된 버전)
def dcf_page():
    st.title("현금흐름할인법(DCF) 평가")
    st.info("현금흐름할인법 평가 기능은 Phase 2에서 구현될 예정입니다.")
    
    # 기본 UI 표시
    st.subheader("예상 구현 기능")
    st.markdown("""
    - 향후 5개년 현금흐름 예측 입력
    - 적정 할인율 설정
    - 영구성장률 기반 잔존가치 계산
    - 단계별 계산 과정 표시
    """)

# 시장가치비교법 페이지 (간소화된 버전)
def market_comparison_page():
    st.title("시장가치비교법 평가")
    st.info("시장가치비교법 평가 기능은 Phase 2에서 구현될 예정입니다.")
    
    # 기본 UI 표시
    st.subheader("예상 구현 기능")
    st.markdown("""
    - 업종별 평균 배수 데이터베이스
    - 다양한 배수(P/E, EV/EBITDA 등) 선택 옵션
    - 동종 업계 기업과 비교 분석
    - 최근 M&A 사례 참조
    """)

# 종합 결과 페이지
def results_page():
    st.title("종합 평가 결과")
    
    # 결과가 없는 경우
    if not st.session_state.valuation_results:
        st.warning("아직 평가된 결과가 없습니다. 먼저 평가 방법을 선택하여 계산해주세요.")
        return
    
    # 회사 정보 표시
    st.subheader(f"{st.session_state.company_data.get('name')} 영업권 평가 결과")
    st.caption(f"산업: {st.session_state.company_data.get('industry')} | 평가일: {datetime.now().strftime('%Y-%m-%d')}")
    
    # 결과 요약
    methods = list(st.session_state.valuation_results.keys())
    values = [st.session_state.valuation_results[method]['value'] for method in methods]
    methods_names = [st.session_state.valuation_results[method]['method'] for method in methods]
    
    # 차트로 결과 표시
    fig = px.bar(
        x=methods_names,
        y=values,
        labels={'x': '평가 방법', 'y': '영업권 가치'},
        title='평가 방법별 영업권 가치 비교'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 결과 테이블
    results_df = pd.DataFrame({
        '평가 방법': methods_names,
        '영업권 가치(원)': [f"{value:,.0f}" for value in values]
    })
    st.dataframe(results_df, hide_index=True, use_container_width=True)
    
    # 가중평균 계산 (방법이 2개 이상인 경우)
    if len(methods) > 1:
        st.subheader("가중평균 영업권 가치")
        
        col1, col2 = st.columns(2)
        
        with col1:
            weights = {}
            for method in methods:
                weights[method] = st.slider(
                    f"{st.session_state.valuation_results[method]['method']} 가중치",
                    min_value=0.0,
                    max_value=1.0,
                    value=1.0/len(methods),
                    step=0.05,
                    key=f"weight_{method}"
                )
            
            # 가중치 정규화
            total_weight = sum(weights.values())
            if total_weight > 0:
                for method in weights:
                    weights[method] = weights[method] / total_weight
            
            # 가중평균 계산
            weighted_value = sum(st.session_state.valuation_results[method]['value'] * weights[method] for method in methods)
            
            st.metric("최종 영업권 가치", f"{weighted_value:,.0f}원")
        
        with col2:
            # 가중치 파이 차트
            fig = px.pie(
                names=methods_names,
                values=list(weights.values()),
                title='평가 방법 가중치'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # 보고서 페이지로 이동
    if st.button("보고서 생성하기"):
        st.session_state.current_page = 'report'
        st.rerun()

# 보고서 페이지 (간소화된 버전)
def report_page():
    st.title("평가 보고서")
    
    if not st.session_state.valuation_results:
        st.warning("아직 평가된 결과가 없습니다. 먼저 평가 방법을 선택하여 계산해주세요.")
        return
    
    st.info("PDF 보고서 생성 기능은 Phase 3에서 구현될 예정입니다.")
    
    # 간단한 미리보기
    st.subheader("보고서 미리보기")
    
    # 회사 정보
    st.markdown(f"""
    ## 영업권 가치 평가 보고서
    
    **회사명**: {st.session_state.company_data.get('name')}  
    **산업**: {st.session_state.company_data.get('industry')}  
    **사업자등록번호**: {st.session_state.company_data.get('business_number')}  
    **평가일**: {datetime.now().strftime('%Y-%m-%d')}
    
    ### 평가 결과 요약
    """)
    
    # 결과 테이블
    methods = list(st.session_state.valuation_results.keys())
    values = [st.session_state.valuation_results[method]['value'] for method in methods]
    methods_names = [st.session_state.valuation_results[method]['method'] for method in methods]
    
    results_df = pd.DataFrame({
        '평가 방법': methods_names,
        '영업권 가치(원)': [f"{value:,.0f}" for value in values]
    })
    st.dataframe(results_df, hide_index=True, use_container_width=True)
    
    # 차트
    fig = px.bar(
        x=methods_names,
        y=values,
        labels={'x': '평가 방법', 'y': '영업권 가치'},
        title='평가 방법별 영업권 가치 비교'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 다운로드 버튼 (실제로는 아직 기능 없음)
    st.download_button(
        label="PDF 보고서 다운로드",
        data="샘플 PDF 데이터",  # 실제로는 PDF 파일 생성 필요
        file_name=f"{st.session_state.company_data.get('name')}_영업권평가보고서.pdf",
        mime="application/pdf",
        disabled=True  # Phase 3에서 활성화 예정
    )

# 메인 함수
def main():
    # 사이드바 렌더링
    render_sidebar()
    
    # 현재 페이지에 따라 다른 함수 호출
    if st.session_state.current_page == 'home':
        home_page()
    elif st.session_state.current_page == 'company_info':
        company_info_page()
    elif st.session_state.current_page == 'excess_earnings':
        excess_earnings_page()
    elif st.session_state.current_page == 'dcf':
        dcf_page()
    elif st.session_state.current_page == 'market_comparison':
        market_comparison_page()
    elif st.session_state.current_page == 'results':
        results_page()
    elif st.session_state.current_page == 'report':
        report_page()

if __name__ == "__main__":
    main() 