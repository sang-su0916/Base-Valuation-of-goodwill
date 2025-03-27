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

# 홈 페이지
def home_page():
    st.title("영업권 평가 시스템에 오신 것을 환영합니다")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.expander("영업권이란?", expanded=False):
            st.markdown("""
            영업권은 기업의 순자산가치를 초과하는 가치로, 기업의 브랜드, 고객 관계, 기술력 등 무형의 가치를 포함합니다.
            기업 인수합병(M&A) 및 법인전환 과정에서 영업권의 가치 평가가 필수적입니다.
            """)
        
        with st.expander("주요 평가 방법", expanded=False):
            st.markdown("""
            - **초과이익법**: 정상이익을 초과하는 이익을 계산하여 영업권 가치를 평가
            - **현금흐름할인법(DCF)**: 미래 예상 현금흐름을 현재가치화하여 평가
            - **시장가치비교법**: 유사 기업 비교를 통한 가치 산출
            """)
        
        with st.expander("사용 방법", expanded=False):
            st.markdown("""
            1. 왼쪽 사이드바에서 원하는 평가 방법을 선택하세요.
            2. 기업 정보와 재무 데이터를 입력하세요.
            3. 평가 매개변수를 설정하고 계산하세요.
            4. 결과를 확인하고 보고서를 다운로드하세요.
            """)
        
        st.markdown("""
        ## 영업권 가치 평가의 중요성

        영업권 가치 평가는 기업의 현재와 미래 가치를 정확히 파악하는 데 필수적입니다.
        이 시스템은 다양한 평가 방법론을 통해 객관적이고 전문적인 영업권 가치 평가를 제공합니다.
        """)
        
        if st.button("시작하기", key="start_button"):
            st.session_state.current_page = 'company_info'
            st.rerun()
    
    with col2:
        with st.expander("영업권 평가가 필요한 경우", expanded=False):
            st.markdown("""
            - 기업 인수합병(M&A)
            - 법인 전환
            - 회계 목적의 자산 재평가
            - 세무 신고 및 세금 계획
            - 투자 유치 및 기업 가치 증명
            """)

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
    
    # 초과이익법 설명 (숨김 기능)
    with st.expander("초과이익법 설명", expanded=False):
        st.markdown("""
        ## 초과이익법 개요
        
        초과이익법은 기업의 자산이 정상적으로 얻을 수 있는 이익을 초과하여 발생하는 이익을 기준으로 영업권을 평가하는 방법입니다.
        
        ### 주요 단계:
        1. 평가 대상 기업의 평균 이익 산출
        2. 기업 자산의 정상 수익률 결정
        3. 정상이익 계산 (자산 × 정상 수익률)
        4. 초과이익 계산 (평균이익 - 정상이익)
        5. 초과이익의 현재가치 합계 산출
        
        ### 고려사항:
        - 정상 수익률의 적정성
        - 초과이익 인정 기간의 설정
        - 업종별 특성 반영
        """)
    
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
    
    # 기업 데이터 확인
    if st.session_state.company_data.get('name') == '':
        st.warning("기업 정보가 입력되지 않았습니다. 먼저 기업 정보를 입력해주세요.")
        if st.button("기업 정보 입력으로 이동"):
            st.session_state.current_page = 'company_info'
            st.rerun()
        return
    
    st.subheader(f"{st.session_state.company_data.get('name')} - 현금흐름할인법 평가")
    
    # DCF 파라미터 설정
    with st.form("dcf_params"):
        st.subheader("평가 매개변수 설정")
        
        col1, col2 = st.columns(2)
        
        with col1:
            growth_rate = st.slider("영업이익 성장률 (%)", min_value=0.0, max_value=30.0, value=5.0, step=0.5)
            forecast_years = st.number_input("예측 기간 (년)", min_value=1, max_value=10, value=5)
        
        with col2:
            discount_rate = st.slider("할인율 (%)", min_value=5.0, max_value=30.0, value=15.0, step=0.5)
            terminal_growth = st.slider("영구 성장률 (%)", min_value=0.0, max_value=5.0, value=1.0, step=0.1)
        
        # 고급 설정
        with st.expander("고급 설정"):
            risk_premium = st.slider("위험 프리미엄 (%)", min_value=0.0, max_value=10.0, value=3.0, step=0.5)
            tax_rate = st.slider("법인세율 (%)", min_value=0.0, max_value=30.0, value=22.0, step=0.5)
        
        calculate_button = st.form_submit_button("평가 계산")
        
        if calculate_button:
            try:
                # 데이터 가져오기
                df = st.session_state.company_data.get('financial_data')
                
                # 기준 영업이익 (최근 연도)
                if 'operating_profit' in df.columns or '영업이익' in df.columns:
                    col_name = 'operating_profit' if 'operating_profit' in df.columns else '영업이익'
                    base_operating_profit = df[col_name].iloc[0]  # 최신 연도
                else:
                    # 영업이익 컬럼이 없는 경우 가상의 영업이익 계산
                    base_operating_profit = df['당기순이익'].iloc[0] * 1.25  # 당기순이익의 125%로 가정
                
                # 미래 현금흐름 예측
                cash_flows = []
                for year in range(1, forecast_years + 1):
                    cf = base_operating_profit * (1 + growth_rate/100) ** year
                    # 세금 적용
                    cf = cf * (1 - tax_rate/100)
                    cash_flows.append(cf)
                
                # 현재가치 계산
                present_values = []
                for i, cf in enumerate(cash_flows):
                    discount_factor = 1 / ((1 + (discount_rate + risk_premium)/100) ** (i+1))
                    pv = cf * discount_factor
                    present_values.append(pv)
                
                # 잔존가치(Terminal Value) 계산
                terminal_value = cash_flows[-1] * (1 + terminal_growth/100) / ((discount_rate + risk_premium)/100 - terminal_growth/100)
                terminal_value_pv = terminal_value / ((1 + (discount_rate + risk_premium)/100) ** forecast_years)
                
                # 총 현재가치
                total_present_value = sum(present_values) + terminal_value_pv
                
                # 자본가치 조정
                if 'total_assets' in df.columns or '총자산' in df.columns:
                    asset_col = 'total_assets' if 'total_assets' in df.columns else '총자산'
                    debt_col = 'total_debt' if 'total_debt' in df.columns else '총부채'
                    total_assets = df[asset_col].iloc[0]
                    total_debt = df[debt_col].iloc[0] if debt_col in df.columns else total_assets * 0.4  # 부채 데이터가 없으면 자산의 40%로 가정
                    
                    # 영업권 = 기업가치 - 순자산
                    enterprise_value = total_present_value
                    net_asset_value = total_assets - total_debt
                    goodwill_value = enterprise_value - net_asset_value
                else:
                    # 자산/부채 데이터가 없는 경우 전체 현재가치의 60%를 영업권으로 가정
                    goodwill_value = total_present_value * 0.6
                
                # 결과 저장
                st.session_state.valuation_results['dcf'] = {
                    'method': '현금흐름할인법(DCF)',
                    'value': goodwill_value,
                    'parameters': {
                        'growth_rate': growth_rate,
                        'forecast_years': forecast_years,
                        'discount_rate': discount_rate,
                        'terminal_growth': terminal_growth,
                        'risk_premium': risk_premium,
                        'tax_rate': tax_rate
                    },
                    'details': {
                        'base_operating_profit': base_operating_profit,
                        'cash_flows': cash_flows,
                        'present_values': present_values,
                        'terminal_value': terminal_value,
                        'terminal_value_pv': terminal_value_pv,
                        'total_present_value': total_present_value
                    }
                }
                
                st.success("현금흐름할인법 평가가 완료되었습니다!")
                
            except Exception as e:
                st.error(f"계산 중 오류가 발생했습니다: {e}")
    
    # 계산 결과 표시 (이미 계산된 경우)
    if 'dcf' in st.session_state.valuation_results:
        result = st.session_state.valuation_results['dcf']
        
        st.divider()
        st.subheader("평가 결과")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("영업권 평가액", f"{result['value']:,.0f}원")
            
            st.subheader("주요 매개변수")
            params_df = pd.DataFrame({
                '매개변수': ['영업이익 성장률', '예측 기간', '할인율', '영구 성장률', '위험 프리미엄', '법인세율'],
                '값': [
                    f"{result['parameters']['growth_rate']}%",
                    f"{result['parameters']['forecast_years']}년",
                    f"{result['parameters']['discount_rate']}%",
                    f"{result['parameters']['terminal_growth']}%",
                    f"{result['parameters']['risk_premium']}%",
                    f"{result['parameters']['tax_rate']}%"
                ]
            })
            st.dataframe(params_df, hide_index=True)
        
        with col2:
            # 계산 과정 표시
            with st.expander("상세 계산 과정", expanded=True):
                st.markdown(f"""
                #### 1. 기초 데이터
                - 기준 영업이익: {result['details']['base_operating_profit']:,.0f}원
                
                #### 2. 미래 현금흐름 예측
                - 영업이익 성장률: {result['parameters']['growth_rate']}%
                - 예측 기간: {result['parameters']['forecast_years']}년
                - 법인세율: {result['parameters']['tax_rate']}%
                
                #### 3. 현재가치 계산
                - 할인율: {result['parameters']['discount_rate']}% + 위험 프리미엄 {result['parameters']['risk_premium']}%
                
                #### 4. 잔존가치 계산
                - 영구 성장률: {result['parameters']['terminal_growth']}%
                - 잔존가치: {result['details']['terminal_value']:,.0f}원
                - 잔존가치의 현재가치: {result['details']['terminal_value_pv']:,.0f}원
                
                #### 5. 총 현재가치
                - 미래 현금흐름의 현재가치 합산: {sum(result['details']['present_values']):,.0f}원
                - 잔존가치의 현재가치: {result['details']['terminal_value_pv']:,.0f}원
                - 총 현재가치: {result['details']['total_present_value']:,.0f}원
                
                #### 최종 영업권 가치
                - **{result['value']:,.0f}원**
                """)
            
            # 현금흐름 차트
            years = list(range(1, result['parameters']['forecast_years'] + 1))
            
            # 현금흐름 및 현재가치 데이터프레임
            df_chart = pd.DataFrame({
                '연도': [f'{year}년차' for year in years],
                '미래 현금흐름': result['details']['cash_flows'],
                '현재가치': result['details']['present_values']
            })
            
            # 차트
            fig = px.bar(
                df_chart,
                x='연도',
                y=['미래 현금흐름', '현재가치'],
                barmode='group',
                title='연도별 현금흐름과 현재가치 비교'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # 결과 페이지로 이동 버튼
        if st.button("종합 결과 페이지로 이동"):
            st.session_state.current_page = 'results'
            st.rerun()
    else:
        with st.expander("현금흐름할인법 설명", expanded=False):
            st.markdown("""
            ## 현금흐름할인법(DCF) 개요
            
            현금흐름할인법은 기업이 미래에 창출할 것으로 예상되는 현금흐름을 추정하고, 이를 적절한 할인율로 할인하여 현재가치를 산출하는 방법입니다.
            
            ### 주요 단계:
            1. 향후 5~10년간의 영업이익 예측
            2. 세금 등 조정 후 순현금흐름 계산
            3. 적절한 할인율 적용하여 현재가치 계산
            4. 영구가치(Terminal Value) 계산 및 할인
            5. 모든 현재가치의 합산
            
            ### 고려사항:
            - 성장률 가정의 현실성
            - 할인율 설정의 적정성
            - 영구가치 산정 방식
            """)

# 시장가치비교법 페이지 (간소화된 버전)
def market_comparison_page():
    st.title("시장가치비교법 평가")
    
    # 기업 데이터 확인
    if st.session_state.company_data.get('name') == '':
        st.warning("기업 정보가 입력되지 않았습니다. 먼저 기업 정보를 입력해주세요.")
        if st.button("기업 정보 입력으로 이동"):
            st.session_state.current_page = 'company_info'
            st.rerun()
        return
    
    st.subheader(f"{st.session_state.company_data.get('name')} - 시장가치비교법 평가")
    
    # 시장가치비교법 파라미터 설정
    with st.form("market_comparison_params"):
        st.subheader("평가 매개변수 설정")
        
        col1, col2 = st.columns(2)
        
        with col1:
            multiple_type = st.selectbox(
                "적용 배수 유형", 
                ["P/E (주가수익비율)", "EV/EBITDA (기업가치/EBITDA)", "P/S (주가매출비율)", "P/B (주가장부가치비율)"],
                index=0
            )
            
            industry = st.session_state.company_data.get('industry')
            industry_multiple = get_industry_multiple(industry, multiple_type)
            
            custom_multiple = st.number_input(
                "배수 직접 입력", 
                min_value=0.1, 
                max_value=50.0, 
                value=industry_multiple,
                step=0.1
            )
        
        with col2:
            comparable_companies = st.multiselect(
                "비교 기업 선택", 
                ["업종 평균", "대기업 평균", "중소기업 평균", "산업 상위 25% 기업", "최근 M&A 사례"],
                default=["업종 평균"]
            )
            
            adjustment_factor = st.slider(
                "조정 계수", 
                min_value=0.5, 
                max_value=1.5, 
                value=1.0, 
                step=0.1,
                help="기업 특성을 고려한 조정 계수 (1.0 = 조정 없음)"
            )
        
        # 고급 설정
        with st.expander("고급 설정"):
            premium_discount = st.slider(
                "프리미엄/할인율 (%)", 
                min_value=-30.0, 
                max_value=30.0, 
                value=0.0, 
                step=5.0,
                help="기업의 성장성, 리스크, 규모 등을 고려한 프리미엄 또는 할인율"
            )
            
            liquidity_discount = st.slider(
                "유동성 할인율 (%)", 
                min_value=0.0, 
                max_value=30.0, 
                value=10.0, 
                step=5.0,
                help="비상장사의 경우 적용되는 유동성 할인율"
            )
        
        calculate_button = st.form_submit_button("평가 계산")
        
        if calculate_button:
            try:
                # 데이터 가져오기
                df = st.session_state.company_data.get('financial_data')
                
                # 배수 적용 기준 값 계산
                if multiple_type == "P/E (주가수익비율)":
                    if '당기순이익' in df.columns:
                        base_value = df['당기순이익'].iloc[0]
                    else:
                        base_value = df['영업이익'].iloc[0] * 0.7  # 영업이익의 70%로 순이익 가정
                
                elif multiple_type == "EV/EBITDA (기업가치/EBITDA)":
                    if '영업이익' in df.columns:
                        # EBITDA = 영업이익 + 감가상각비 (간단한 추정)
                        base_value = df['영업이익'].iloc[0] * 1.2  # 감가상각비를 영업이익의 20%로 가정
                    else:
                        base_value = df['당기순이익'].iloc[0] * 1.5
                
                elif multiple_type == "P/S (주가매출비율)":
                    if '매출액' in df.columns:
                        base_value = df['매출액'].iloc[0]
                    else:
                        # 매출액 데이터가 없는 경우 영업이익의 10배로 가정
                        base_value = df['영업이익'].iloc[0] * 10
                
                else:  # P/B (주가장부가치비율)
                    if '자본' in df.columns:
                        base_value = df['자본'].iloc[0]
                    else:
                        # 자본 데이터가 없는 경우 총자산의 60%로 가정
                        base_value = df['총자산'].iloc[0] * 0.6
                
                # 기업 가치 계산
                enterprise_value = base_value * custom_multiple
                
                # 조정 계수 적용
                enterprise_value = enterprise_value * adjustment_factor
                
                # 프리미엄/할인율 적용
                enterprise_value = enterprise_value * (1 + premium_discount/100)
                
                # 유동성 할인율 적용
                enterprise_value = enterprise_value * (1 - liquidity_discount/100)
                
                # 영업권 계산 (기업가치 - 순자산가치)
                if '총자산' in df.columns and '총부채' in df.columns:
                    net_asset_value = df['총자산'].iloc[0] - df['총부채'].iloc[0]
                else:
                    # 순자산 가치를 기업가치의 40%로 가정
                    net_asset_value = enterprise_value * 0.4
                
                goodwill_value = enterprise_value - net_asset_value
                
                # 결과 저장
                st.session_state.valuation_results['market_comparison'] = {
                    'method': '시장가치비교법',
                    'value': goodwill_value,
                    'parameters': {
                        'multiple_type': multiple_type,
                        'custom_multiple': custom_multiple,
                        'comparable_companies': comparable_companies,
                        'adjustment_factor': adjustment_factor,
                        'premium_discount': premium_discount,
                        'liquidity_discount': liquidity_discount
                    },
                    'details': {
                        'base_value': base_value,
                        'enterprise_value': enterprise_value,
                        'net_asset_value': net_asset_value
                    }
                }
                
                st.success("시장가치비교법 평가가 완료되었습니다!")
                
            except Exception as e:
                st.error(f"계산 중 오류가 발생했습니다: {e}")
    
    # 계산 결과 표시 (이미 계산된 경우)
    if 'market_comparison' in st.session_state.valuation_results:
        result = st.session_state.valuation_results['market_comparison']
        
        st.divider()
        st.subheader("평가 결과")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("영업권 평가액", f"{result['value']:,.0f}원")
            
            st.subheader("주요 매개변수")
            params_df = pd.DataFrame({
                '매개변수': ['적용 배수 유형', '적용 배수', '조정 계수', '프리미엄/할인율', '유동성 할인율'],
                '값': [
                    f"{result['parameters']['multiple_type']}",
                    f"{result['parameters']['custom_multiple']:.1f}",
                    f"{result['parameters']['adjustment_factor']:.1f}",
                    f"{result['parameters']['premium_discount']}%",
                    f"{result['parameters']['liquidity_discount']}%"
                ]
            })
            st.dataframe(params_df, hide_index=True)
            
            # 비교 기업 목록
            st.subheader("비교 기업")
            st.write(", ".join(result['parameters']['comparable_companies']))
        
        with col2:
            # 계산 과정 표시
            with st.expander("상세 계산 과정", expanded=True):
                st.markdown(f"""
                #### 1. 기초 데이터
                - 적용 배수 유형: {result['parameters']['multiple_type']}
                - 기준 값: {result['details']['base_value']:,.0f}원
                - 적용 배수: {result['parameters']['custom_multiple']:.1f}
                
                #### 2. 기업 가치 계산
                - 기준 값 × 적용 배수 = {result['details']['base_value']:,.0f} × {result['parameters']['custom_multiple']:.1f} = {result['details']['base_value'] * result['parameters']['custom_multiple']:,.0f}원
                
                #### 3. 조정 계수 적용
                - 조정 계수: {result['parameters']['adjustment_factor']:.1f}
                - 조정 후 기업가치: {result['details']['base_value'] * result['parameters']['custom_multiple']:,.0f} × {result['parameters']['adjustment_factor']:.1f} = {result['details']['base_value'] * result['parameters']['custom_multiple'] * result['parameters']['adjustment_factor']:,.0f}원
                
                #### 4. 프리미엄/할인율 적용
                - 프리미엄/할인율: {result['parameters']['premium_discount']}%
                - 적용 후 기업가치: {result['details']['enterprise_value']:,.0f}원
                
                #### 5. 순자산가치 차감
                - 순자산가치: {result['details']['net_asset_value']:,.0f}원
                - 영업권 = 기업가치 - 순자산가치 = {result['details']['enterprise_value']:,.0f} - {result['details']['net_asset_value']:,.0f} = {result['value']:,.0f}원
                
                #### 최종 영업권 가치
                - **{result['value']:,.0f}원**
                """)
            
            # 시각화 - 영업권 구성 파이 차트
            labels = ['순자산가치', '영업권']
            values = [result['details']['net_asset_value'], result['value']]
            
            fig = px.pie(
                values=values,
                names=labels,
                title='기업 총가치 구성',
                color_discrete_sequence=['#636EFA', '#EF553B']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # 결과 페이지로 이동 버튼
        if st.button("종합 결과 페이지로 이동"):
            st.session_state.current_page = 'results'
            st.rerun()
    else:
        with st.expander("시장가치비교법 설명", expanded=False):
            st.markdown("""
            ## 시장가치비교법 개요
            
            시장가치비교법은 유사한 기업의 주가 배수(P/E, EV/EBITDA 등)를 사용하여 기업의 가치를 평가하는 방법입니다.
            
            ### 주요 단계:
            1. 적절한 배수 지표 선택 (P/E, EV/EBITDA, P/S, P/B 등)
            2. 비교 가능한 기업 또는 업종 평균 배수 확인
            3. 대상 기업의 재무지표에 해당 배수를 적용
            4. 기업 특성에 맞는 프리미엄/할인 적용
            5. 순자산가치를 차감하여 영업권 계산
            
            ### 고려사항:
            - 비교 기업의 적절성
            - 배수 적용의 타당성
            - 기업 간 규모/성장성 차이 반영
            """)

# 업종별 배수 반환 함수 (실제로는 데이터베이스나 외부 API 연동 필요)
def get_industry_multiple(industry, multiple_type):
    # 간단한 예시 데이터 (실제로는 더 정교한 데이터베이스 필요)
    multiples = {
        "제조업": {"P/E (주가수익비율)": 12.5, "EV/EBITDA (기업가치/EBITDA)": 8.2, "P/S (주가매출비율)": 1.2, "P/B (주가장부가치비율)": 1.5},
        "서비스업": {"P/E (주가수익비율)": 15.8, "EV/EBITDA (기업가치/EBITDA)": 10.5, "P/S (주가매출비율)": 2.1, "P/B (주가장부가치비율)": 2.2},
        "도소매업": {"P/E (주가수익비율)": 14.2, "EV/EBITDA (기업가치/EBITDA)": 7.8, "P/S (주가매출비율)": 0.8, "P/B (주가장부가치비율)": 1.7},
        "IT/소프트웨어": {"P/E (주가수익비율)": 22.5, "EV/EBITDA (기업가치/EBITDA)": 15.2, "P/S (주가매출비율)": 4.5, "P/B (주가장부가치비율)": 3.8},
        "금융업": {"P/E (주가수익비율)": 10.2, "EV/EBITDA (기업가치/EBITDA)": 9.0, "P/S (주가매출비율)": 2.5, "P/B (주가장부가치비율)": 1.0},
        "건설업": {"P/E (주가수익비율)": 11.8, "EV/EBITDA (기업가치/EBITDA)": 6.5, "P/S (주가매출비율)": 0.6, "P/B (주가장부가치비율)": 1.2},
        "기타": {"P/E (주가수익비율)": 13.5, "EV/EBITDA (기업가치/EBITDA)": 9.0, "P/S (주가매출비율)": 1.5, "P/B (주가장부가치비율)": 1.8}
    }
    
    # 업종이 목록에 없으면 기본값 반환
    if industry not in multiples:
        return multiples["기타"][multiple_type]
    
    return multiples[industry][multiple_type]

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
