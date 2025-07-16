import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==============================================================================
# Äáº¢M Báº¢O FILE 'a04ecaf1_1dae_4c90_8081_086cd7c7b725.py' Náº°NG CÃ™NG THÆ¯ Má»¤C
# HOáº¶C THAY THáº¾ TÃŠN FILE Náº¾U Báº N ÄÃƒ Äá»”I TÃŠN NÃ“.
# ==============================================================================
from a04ecaf1_1dae_4c90_8081_086cd7c7b725 import (
    setup_paths, load_raw_data, read_configs,
    apply_filters, export_report, export_pdf_report,
    apply_comparison_filters, export_comparison_report, export_comparison_pdf_report
)
# ==============================================================================

script_dir = os.path.dirname(__file__)
csv_file_path = os.path.join(script_dir, "invited_emails.csv")

# Gá»i hÃ m setup_paths ngay tá»« Ä‘áº§u Ä‘á»ƒ path_dict cÃ³ sáºµn
path_dict = setup_paths()

# ==============================================================================
# KHá»žI Táº O CÃC BIáº¾N TRáº NG THÃI PHIÃŠN (SESSION STATE VARIABLES)
# ==============================================================================
if 'comparison_mode' not in st.session_state:
    st.session_state.comparison_mode = "So SÃ¡nh Dá»± Ãn Trong Má»™t ThÃ¡ng" # Hoáº·c giÃ¡ trá»‹ máº·c Ä‘á»‹nh phÃ¹ há»£p

if 'comparison_selected_years' not in st.session_state:
    st.session_state.comparison_selected_years = [datetime.now().year] # Hoáº·c giÃ¡ trá»‹ máº·c Ä‘á»‹nh phÃ¹ há»£p

if 'comparison_selected_months' not in st.session_state:
    st.session_state.comparison_selected_months = [] # Hoáº·c giÃ¡ trá»‹ máº·c Ä‘á»‹nh phÃ¹ há»£p

if 'comparison_selected_projects' not in st.session_state:
    st.session_state.comparison_selected_projects = [] # Hoáº·c giÃ¡ trá»‹ máº·c Ä‘á»‹nh phÃ¹ há»£p

if 'comparison_selected_months_over_time' not in st.session_state:
    st.session_state.comparison_selected_months_over_time = [] # Khá»Ÿi táº¡o lÃ  má»™t danh sÃ¡ch rá»—ng hoáº·c giÃ¡ trá»‹ máº·c Ä‘á»‹nh phÃ¹ há»£p

if 'selected_years' not in st.session_state: # VÃ­ dá»¥ cho bá»™ lá»c bÃ¡o cÃ¡o tiÃªu chuáº©n
    st.session_state.selected_years = [datetime.now().year]

if 'selected_months' not in st.session_state: # VÃ­ dá»¥ cho bá»™ lá»c bÃ¡o cÃ¡o tiÃªu chuáº©n
    st.session_state.selected_months = []

# ThÃªm dÃ²ng nÃ y Ä‘á»ƒ máº·c Ä‘á»‹nh ngÃ´n ngá»¯ lÃ  tiáº¿ng Anh
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = "English"

# ---------------------------
# PHáº¦N XÃC THá»°C TRUY Cáº¬P
# ---------------------------

@st.cache_data
def load_invited_emails():
    try:
        df = pd.read_csv(csv_file_path, header=None, encoding='utf-8')
        # Sá»­a lá»—i: ThÃªm .str trÆ°á»›c .strip()
        emails = df.iloc[:, 0].astype(str).str.strip().str.lower().tolist()
        return emails
    except FileNotFoundError:
        st.error(f"Lá»—i: KhÃ´ng tÃ¬m tháº¥y file invited_emails.csv táº¡i {csv_file_path}. Vui lÃ²ng kiá»ƒm tra Ä‘Æ°á»ng dáº«n.")
        return []
    except Exception as e:
        st.error(f"Lá»—i khi táº£i file invited_emails.csv: {e}")
        return []

# Táº£i danh sÃ¡ch email Ä‘Æ°á»£c má»i má»™t láº§n
INVITED_EMAILS = load_invited_emails()

# HÃ m ghi log truy cáº­p
def log_user_access(email):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {"Time": timestamp, "Email": email}
    if "access_log" not in st.session_state:
        st.session_state.access_log = []
    st.session_state.access_log.append(log_entry)

# Logic xÃ¡c thá»±c ngÆ°á»i dÃ¹ng
if "user_email" not in st.session_state:
    st.set_page_config(page_title="Triac Time Report", layout="wide")
    st.title("ðŸ” Access authentication")
    email_input = st.text_input("ðŸ“§ Enter the invited email to access:")

    if email_input:
        email = email_input.strip().lower()
        if email in INVITED_EMAILS:
            st.session_state.user_email = email
            log_user_access(email)
            st.success("âœ… Valid email! Entering application...")
            st.rerun()
        else:
            st.error("âŒ Email is not on the invitation list.")
    st.stop() # Dá»«ng thá»±c thi náº¿u chÆ°a xÃ¡c thá»±c

# ---------------------------
# PHáº¦N GIAO DIá»†N CHÃNH Cá»¦A á»¨NG Dá»¤NG
# ---------------------------
# Sá»­ dá»¥ng session_state Ä‘á»ƒ lÆ°u trá»¯ lá»±a chá»n ngÃ´n ngá»¯
if 'lang' not in st.session_state:
    st.session_state.lang = 'en' # Máº·c Ä‘á»‹nh lÃ  tiáº¿ng Anh

# Cáº¥u hÃ¬nh trang (chá»‰ cháº¡y má»™t láº§n sau khi xÃ¡c thá»±c)
st.set_page_config(page_title="Triac Time Report", layout="wide")

st.markdown("""
    <style>
        .report-title {font-size: 30px; color: #003366; font-weight: bold;}
        .report-subtitle {font-size: 14px; color: gray;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# =====================================
# Khá»Ÿi táº¡o ngÃ´n ngá»¯ vÃ  tá»« Ä‘iá»ƒn vÄƒn báº£n
# =====================================
# Tá»« Ä‘iá»ƒn cho cÃ¡c chuá»—i vÄƒn báº£n
TEXTS = {
    'vi': {
        'app_title': "ðŸ“Š CÃ´ng cá»¥ táº¡o bÃ¡o cÃ¡o thá»i gian",
        'lang_select': "Chá»n ngÃ´n ngá»¯:",
        'language_vi': "Tiáº¿ng Viá»‡t",
        'language_en': "English",
        'template_not_found': "âŒ KhÃ´ng tÃ¬m tháº¥y file template: {}. Vui lÃ²ng Ä‘áº£m báº£o file náº±m cÃ¹ng thÆ° má»¥c vá»›i á»©ng dá»¥ng.",
        'failed_to_load_raw_data': "âš ï¸ KhÃ´ng thá»ƒ táº£i dá»¯ liá»‡u thÃ´. Vui lÃ²ng kiá»ƒm tra sheet 'Raw Data' trong file template vÃ  Ä‘á»‹nh dáº¡ng dá»¯ liá»‡u.",
        'loading_data': "ðŸ”„ Äang táº£i dá»¯ liá»‡u vÃ  cáº¥u hÃ¬nh...",
        'tab_standard_report': "BÃ¡o cÃ¡o tiÃªu chuáº©n",
        'tab_comparison_report': "BÃ¡o cÃ¡o so sÃ¡nh",
        'tab_data_preview': "Xem trÆ°á»›c dá»¯ liá»‡u",
        'standard_report_header': "Cáº¥u hÃ¬nh bÃ¡o cÃ¡o thá»i gian tiÃªu chuáº©n",
        'select_analysis_mode': "Chá»n cháº¿ Ä‘á»™ phÃ¢n tÃ­ch:",
        'select_year': "Chá»n nÄƒm:",
        'select_months': "Chá»n thÃ¡ng(cÃ¡c thÃ¡ng):",
        'standard_project_selection_header': "Lá»±a chá»n dá»± Ã¡n cho bÃ¡o cÃ¡o tiÃªu chuáº©n",
        'standard_project_selection_text': "Chá»n dá»± Ã¡n Ä‘á»ƒ bao gá»“m (máº·c Ä‘á»‹nh chá»‰ bao gá»“m cÃ¡c dá»± Ã¡n 'yes' tá»« cáº¥u hÃ¬nh template):",
        'generate_standard_report_btn': "ðŸš€ Táº¡o bÃ¡o cÃ¡o tiÃªu chuáº©n",
        'no_year_selected_error': "Vui lÃ²ng chá»n má»™t nÄƒm há»£p lá»‡ Ä‘á»ƒ táº¡o bÃ¡o cÃ¡o.",
        'no_project_selected_warning_standard': "Vui lÃ²ng chá»n Ã­t nháº¥t má»™t dá»± Ã¡n Ä‘á»ƒ táº¡o bÃ¡o cÃ¡o tiÃªu chuáº©n.",
        'no_data_after_filter_standard': "âš ï¸ KhÃ´ng cÃ³ dá»¯ liá»‡u sau khi lá»c cho bÃ¡o cÃ¡o tiÃªu chuáº©n. Vui lÃ²ng kiá»ƒm tra cÃ¡c lá»±a chá»n cá»§a báº¡n.",
        'generating_excel_report': "Äang táº¡o bÃ¡o cÃ¡o Excel...",
        'excel_report_generated': "âœ… BÃ¡o cÃ¡o Excel Ä‘Ã£ Ä‘Æ°á»£c táº¡o: {}",
        'download_excel_report': "ðŸ“¥ Táº£i bÃ¡o cÃ¡o Excel",
        'generating_pdf_report': "Äang táº¡o bÃ¡o cÃ¡o PDF...",
        'pdf_report_generated': "âœ… BÃ¡o cÃ¡o PDF Ä‘Ã£ Ä‘Æ°á»£c táº¡o: {}",
        'download_pdf_report': "ðŸ“¥ Táº£i bÃ¡o cÃ¡o PDF",
        'failed_to_generate_excel': "âŒ ÄÃ£ xáº£y ra lá»—i khi táº¡o bÃ¡o cÃ¡o Excel.",
        'failed_to_generate_pdf': "âŒ ÄÃ£ xáº£y ra lá»—i khi táº¡o bÃ¡o cÃ¡o PDF.",
        'comparison_report_header': "Cáº¥u hÃ¬nh bÃ¡o cÃ¡o so sÃ¡nh",
        'select_comparison_mode': "Chá»n cháº¿ Ä‘á»™ so sÃ¡nh:",
        'compare_projects_month': "So SÃ¡nh Dá»± Ãn Trong Má»™t ThÃ¡ng",
        'compare_projects_year': "So SÃ¡nh Dá»± Ãn Trong Má»™t NÄƒm",
        'compare_one_project_over_time': "So SÃ¡nh Má»™t Dá»± Ãn Qua CÃ¡c ThÃ¡ng/NÄƒm",
        'filter_data_for_comparison': "Lá»c dá»¯ liá»‡u Ä‘á»ƒ so sÃ¡nh",
        'select_years': "Chá»n nÄƒm(cÃ¡c nÄƒm):", # DÃ¹ng chung cho cÃ¡c mode
        'select_months_comp': "Chá»n thÃ¡ng(cÃ¡c thÃ¡ng):", # DÃ¹ng chung cho cÃ¡c mode
        'select_projects_comp': "Chá»n dá»± Ã¡n(cÃ¡c dá»± Ã¡n):", # DÃ¹ng chung cho cÃ¡c mode
        'generate_comparison_report_btn': "ðŸš€ Táº¡o bÃ¡o cÃ¡o so sÃ¡nh",
        'no_data_after_filter_comparison': "âš ï¸ {}",
        'data_filtered_success': "âœ… Dá»¯ liá»‡u Ä‘Ã£ Ä‘Æ°á»£c lá»c thÃ nh cÃ´ng cho so sÃ¡nh.",
        'comparison_data_preview': "Xem trÆ°á»›c dá»¯ liá»‡u so sÃ¡nh",
        'generating_comparison_excel': "Äang táº¡o bÃ¡o cÃ¡o Excel so sÃ¡nh...",
        'comparison_excel_generated': "âœ… BÃ¡o cÃ¡o Excel so sÃ¡nh Ä‘Ã£ Ä‘Æ°á»£c táº¡o: {}",
        'download_comparison_excel': "ðŸ“¥ Táº£i bÃ¡o cÃ¡o Excel so sÃ¡nh",
        'generating_comparison_pdf': "Äang táº¡o bÃ¡o cÃ¡o PDF so sÃ¡nh...",
        'comparison_pdf_generated': "âœ… BÃ¡o cÃ¡o PDF so sÃ¡nh Ä‘Ã£ Ä‘Æ°á»£c táº¡o: {}",
        'download_comparison_pdf': "ðŸ“¥ Táº£i bÃ¡o cÃ¡o PDF so sÃ¡nh",
        'failed_to_generate_comparison_excel': "âŒ ÄÃ£ xáº£y ra lá»—i khi táº¡o bÃ¡o cÃ¡o Excel so sÃ¡nh.",
        'failed_to_generate_comparison_pdf': "âŒ ÄÃ£ xáº£y ra lá»—i khi táº¡o bÃ¡o cÃ¡o PDF so sÃ¡nh.",
        'raw_data_preview_header': "Dá»¯ liá»‡u Ä‘áº§u vÃ o thÃ´ (100 hÃ ng Ä‘áº§u)",
        'no_raw_data': "KhÃ´ng cÃ³ dá»¯ liá»‡u thÃ´ Ä‘Æ°á»£c táº£i.",
        'no_year_in_data': "KhÃ´ng cÃ³ nÄƒm nÃ o trong dá»¯ liá»‡u Ä‘á»ƒ chá»n.",
        'user_guide': "HÆ°á»›ng dáº«n sá»­ dá»¥ng",
        'export_options': "TÃ¹y chá»n xuáº¥t bÃ¡o cÃ¡o",
        'export_excel_option': "Xuáº¥t ra Excel (.xlsx)",
        'export_pdf_option': "Xuáº¥t ra PDF (.pdf)",
        'report_button': "Táº¡o bÃ¡o cÃ¡o",
        'no_data': "KhÃ´ng cÃ³ dá»¯ liá»‡u sau khi lá»c",
        'report_done': "ÄÃ£ táº¡o bÃ¡o cÃ¡o",
        'download_excel': "Táº£i Excel",
        'download_pdf': "Táº£i PDF",
        'warning_select_export_format': "Vui lÃ²ng chá»n Ã­t nháº¥t má»™t Ä‘á»‹nh dáº¡ng xuáº¥t bÃ¡o cÃ¡o (Excel hoáº·c PDF).",
        'error_generating_report': "CÃ³ lá»—i xáº£y ra khi táº¡o bÃ¡o cÃ¡o. Vui lÃ²ng thá»­ láº¡i.",
        # ThÃªm cÃ¡c tin nháº¯n má»›i cho mode "So SÃ¡nh Má»™t Dá»± Ãn Qua CÃ¡c ThÃ¡ng/NÄƒm"
        'select_single_project_warning': "Vui lÃ²ng chá»n CHá»ˆ Má»˜T dá»± Ã¡n cho cháº¿ Ä‘á»™ nÃ y.",
        'select_years_for_over_time_months': "Chá»n nÄƒm (hoáº·c cÃ¡c nÄƒm) báº¡n muá»‘n so sÃ¡nh:",
        'select_months_for_single_year': "Chá»n thÃ¡ng(cÃ¡c thÃ¡ng) trong nÄƒm Ä‘Ã£ chá»n:",
        'comparison_over_years_note': "LÆ°u Ã½: Báº¡n Ä‘Ã£ chá»n nhiá»u nÄƒm. BÃ¡o cÃ¡o sáº½ so sÃ¡nh dá»¯ liá»‡u cá»§a dá»± Ã¡n qua cÃ¡c nÄƒm Ä‘Ã£ chá»n. Lá»±a chá»n thÃ¡ng sáº½ bá»‹ bá» qua.",
        'comparison_over_months_note': "LÆ°u Ã½: BÃ¡o cÃ¡o sáº½ so sÃ¡nh dá»¯ liá»‡u cá»§a dá»± Ã¡n qua cÃ¡c thÃ¡ng Ä‘Ã£ chá»n trong nÄƒm {}.",
        'no_comparison_criteria_selected': "Vui lÃ²ng chá»n Ã­t nháº¥t má»™t nÄƒm hoáº·c má»™t thÃ¡ng Ä‘á»ƒ so sÃ¡nh.",
        'no_month_selected_for_single_year': "Vui lÃ²ng chá»n Ã­t nháº¥t má»™t thÃ¡ng khi so sÃ¡nh má»™t dá»± Ã¡n trong má»™t nÄƒm cá»¥ thá»ƒ."
    },
    'en': {
        'app_title': "ðŸ“Š Time Report Generator",
        'lang_select': "Select language:",
        'language_vi': "Tiáº¿ng Viá»‡t",
        'language_en': "English",
        'template_not_found': "âŒ Template file not found: {}. Please ensure the file is in the same directory as the application.",
        'failed_to_load_raw_data': "âš ï¸ Failed to load raw data. Please check the 'Raw Data' sheet in the template file and data format.",
        'loading_data': "ðŸ”„ Loading data and configurations...",
        'tab_standard_report': "Standard Report",
        'tab_comparison_report': "Comparison Report",
        'tab_data_preview': "Data Preview",
        'standard_report_header': "Standard Time Report Configuration",
        'select_analysis_mode': "Select analysis mode:",
        'select_year': "Select year:",
        'select_months': "Select month(s):",
        'standard_project_selection_header': "Project Selection for Standard Report",
        'standard_project_selection_text': "Select projects to include (only 'yes' projects from template config will be included by default):",
        'generate_standard_report_btn': "ðŸš€ Generate Standard Report",
        'no_year_selected_error': "Please select a valid year to generate the report.",
        'no_project_selected_warning_standard': "Please select at least one project to generate the standard report.",
        'no_data_after_filter_standard': "âš ï¸ No data after filtering for the standard report. Please check your selections.",
        'generating_excel_report': "Generating Excel report...",
        'excel_report_generated': "âœ… Excel Report generated: {}",
        'download_excel_report': "ðŸ“¥ Download Excel Report",
        'generating_pdf_report': "Generating PDF report...",
        'pdf_report_generated': "âœ… PDF Report generated: {}",
        'download_pdf_report': "ðŸ“¥ Download PDF Report",
        'failed_to_generate_excel': "âŒ Failed to generate Excel report.",
        'failed_to_generate_pdf': "âŒ Failed to generate PDF report.",
        'comparison_report_header': "Comparison Report Configuration",
        'select_comparison_mode': "Select comparison mode:",
        'compare_projects_month': "Compare Projects in a Month",
        'compare_projects_year': "Compare Projects in a Year",
        'compare_one_project_over_time': "Compare One Project Over Time (Months/Years)",
        'filter_data_for_comparison': "Filter Data for Comparison",
        'select_years': "Select Year(s):",
        'select_months_comp': "Select Month(s):",
        'select_projects_comp': "Select Project(s):",
        'generate_comparison_report_btn': "ðŸš€ Generate Comparison Report",
        'no_data_after_filter_comparison': "âš ï¸ {}",
        'data_filtered_success': "âœ… Data filtered successfully for comparison.",
        'comparison_data_preview': "Comparison Data Preview",
        'generating_comparison_excel': "Generating Comparison Excel Report...",
        'comparison_excel_generated': "âœ… Comparison Excel Report generated: {}",
        'download_comparison_excel': "ðŸ“¥ Download Comparison Excel",
        'generating_comparison_pdf': "Generating Comparison PDF Report...",
        'comparison_pdf_generated': "âœ… PDF Report generated: {}",
        'download_comparison_pdf': "ðŸ“¥ Download Comparison PDF",
        'failed_to_generate_comparison_excel': "âŒ Failed to generate Comparison Excel report.",
        'failed_to_generate_comparison_pdf': "âŒ Failed to generate Comparison PDF report.",
        'raw_data_preview_header': "Raw Input Data (First 100 rows)",
        'no_raw_data': "No raw data loaded.",
        'no_year_in_data': "No years in data to select.",
        'user_guide': "User Guide",
        'export_options': "Export Options",
        'export_excel_option': "Export as Excel (.xlsx)",
        'export_pdf_option': "Export as PDF (.pdf)",
        'report_button': "Generate report",
        'no_data': "No data after filtering",
        'report_done': "Report created successfully",
        'download_excel': "Download Excel",
        'download_pdf': "Download PDF",
        'warning_select_export_format': "Please select at least one report export format (Excel or PDF).",
        'error_generating_report': "An error occurred while generating the report. Please try again.",
        # Add new messages for "Compare One Project Over Time" mode
        'select_single_project_warning': "Please select ONLY ONE project for this mode.",
        'select_years_for_over_time_months': "Select the year(s) for comparison:",
        'select_months_for_single_year': "Select month(s) within the chosen year:",
        'comparison_over_years_note': "Note: You have selected multiple years. The report will compare the project's data across the selected years. Month selection will be ignored.",
        'comparison_over_months_note': "Note: The report will compare the project's data across the selected months in year {}.",
        'no_comparison_criteria_selected': "Please select at least one year or month for comparison.",
        'no_month_selected_for_single_year': "Please select at least one month when comparing a single project within a specific year."
    }
}

# Láº¥y tá»« Ä‘iá»ƒn vÄƒn báº£n dá»±a trÃªn lá»±a chá»n ngÃ´n ngá»¯ hiá»‡n táº¡i
def get_text(key):
    return TEXTS[st.session_state.lang].get(key, f"Missing text for {key}")

# Header cá»§a á»©ng dá»¥ng
col_logo_title, col_lang = st.columns([0.8, 0.2])
with col_logo_title:
    st.image("triac_logo.png", width=110) # Logo cá»‘ Ä‘á»‹nh
    st.markdown("<div class='report-title'>Triac Time Report Generator</div>", unsafe_allow_html=True) # TiÃªu Ä‘á» cá»‘ Ä‘á»‹nh
    st.markdown("<div class='report-subtitle'>Reporting tool for time tracking and analysis</div>", unsafe_allow_html=True) # Phá»¥ Ä‘á» cá»‘ Ä‘á»‹nh

with col_lang:
    st.session_state.lang = st.radio(
        get_text('lang_select'),
        options=['vi', 'en'],
        format_func=lambda x: get_text('language_' + x),
        key='language_selector_main'
    )


# Check if template file exists
if not os.path.exists(path_dict['template_file']):
    st.error(get_text('template_not_found').format(path_dict['template_file']))
    st.stop()

# Load raw data and configurations once
@st.cache_data(ttl=1800)
def cached_load():
    df_raw = load_raw_data(path_dict['template_file'])
    config_data = read_configs(path_dict['template_file'])
    return df_raw, config_data

with st.spinner(get_text('loading_data')):
    df_raw, config_data = cached_load()

if df_raw.empty:
    st.error(get_text('failed_to_load_raw_data'))
    st.stop()

# Get unique years, months, and projects from raw data for selectbox options
all_years = sorted(df_raw['Year'].dropna().unique().astype(int).tolist())
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
all_months = [m for m in month_order if m in df_raw['MonthName'].dropna().unique()]
all_projects = sorted(df_raw['Project name'].dropna().unique().tolist())


# Main interface tabs
tab_standard_report_main, tab_comparison_report_main, tab_data_preview_main, tab_user_guide_main = st.tabs([
    get_text('tab_standard_report'),
    get_text('tab_comparison_report'),
    get_text('tab_data_preview'),
    get_text('user_guide')
])

# =========================================================================
# STANDARD REPORT TAB
# =========================================================================
with tab_standard_report_main:
    st.header(get_text('standard_report_header'))

    col1_std, col2_std, col3_std = st.columns(3)
    with col1_std:
        # State management for standard analysis mode
        if 'standard_analysis_mode' not in st.session_state:
            st.session_state.standard_analysis_mode = config_data['mode'] if config_data['mode'] in ['year', 'month', 'week'] else 'year'

        mode_options = ['year', 'month', 'week']
        try:
            mode_index = mode_options.index(st.session_state.standard_analysis_mode)
        except ValueError:
            mode_index = 0
            st.session_state.standard_analysis_mode = mode_options[0]

        mode = st.selectbox(
            get_text('select_analysis_mode'),
            options=mode_options,
            index=mode_index,
            key='standard_mode_tab'
        )
        st.session_state.standard_analysis_mode = mode # Update state

    with col2_std:
        # State management for standard selected year
        if 'standard_selected_year' not in st.session_state:
            st.session_state.standard_selected_year = config_data['year'] if config_data['year'] in all_years else (all_years[0] if all_years else None)
        
        default_std_year_index = 0
        if st.session_state.standard_selected_year in all_years:
            default_std_year_index = all_years.index(st.session_state.standard_selected_year)
        elif all_years:
            st.session_state.standard_selected_year = all_years[0] # Fallback
            default_std_year_index = 0
        elif st.session_state.standard_selected_year is None: # No years available at all
            default_std_year_index = None


        selected_year = st.selectbox(
            get_text('select_year'),
            options=all_years,
            index=default_std_year_index,
            key='standard_year_tab'
        )
        st.session_state.standard_selected_year = selected_year # Update state

        if selected_year is None:
            st.warning(get_text('no_year_in_data'))

    with col3_std:
        # State management for standard selected months
        if 'standard_selected_months' not in st.session_state:
            st.session_state.standard_selected_months = config_data['months'] if config_data['months'] else all_months
        
        # Ensure default months are valid in current all_months
        valid_default_months = [m for m in st.session_state.standard_selected_months if m in all_months]
        if not valid_default_months and all_months: # Fallback if no valid default or if default is empty but options exist
            valid_default_months = all_months # Select all months as default if nothing is selected

        selected_months = st.multiselect(
            get_text('select_months'),
            options=all_months,
            default=valid_default_months,
            key='standard_months_tab'
        )
        st.session_state.standard_selected_months = selected_months # Update state


    st.subheader(get_text('standard_project_selection_header'))

    # Determine initial included projects based on config for default
    initial_included_projects_config = config_data['project_filter_df'][
        config_data['project_filter_df']['Include'].astype(str).str.lower() == 'yes'
    ]['Project Name'].tolist()

    # State management for standard project selection
    if 'standard_selected_projects' not in st.session_state:
        default_standard_projects = [p for p in initial_included_projects_config if p in all_projects]
        if not default_standard_projects and all_projects:
            default_standard_projects = all_projects # Default to all if config is empty
        st.session_state.standard_selected_projects = default_standard_projects
    
    # Ensure default value for multiselect is valid
    current_std_projects_default = [p for p in st.session_state.standard_selected_projects if p in all_projects]
    if not current_std_projects_default and all_projects: # Fallback if selected projects are no longer valid or empty
        current_std_projects_default = all_projects

    standard_project_selection = st.multiselect(
        get_text('standard_project_selection_text'),
        options=all_projects,
        default=current_std_projects_default,
        key='standard_project_selection_tab'
    )
    st.session_state.standard_selected_projects = standard_project_selection # Update state


    st.markdown("---")
    st.subheader(get_text("export_options"))
    export_excel = st.checkbox(get_text("export_excel_option"), value=True, key='export_excel_std')
    export_pdf = st.checkbox(get_text("export_pdf_option"), value=False, key='export_pdf_std')

    if st.button(get_text('generate_standard_report_btn'), key='generate_standard_report_btn_tab'):
        if not export_excel and not export_pdf:
            st.warning(get_text("warning_select_export_format"))
        elif selected_year is None:
            st.error(get_text('no_year_selected_error'))
        elif not standard_project_selection:
            st.warning(get_text('no_project_selected_warning_standard'))
        else:
            temp_project_filter_df_standard = pd.DataFrame({
                'Project Name': standard_project_selection,
                'Include': ['yes'] * len(standard_project_selection)
            })

            standard_report_config = {
                'mode': mode,
                'year': selected_year,
                'months': selected_months,
                'project_filter_df': temp_project_filter_df_standard
            }

            df_filtered_standard = apply_filters(df_raw, standard_report_config)

            if df_filtered_standard.empty:
                st.warning(get_text('no_data_after_filter_standard'))
            else:
                report_generated = False
                if export_excel:
                    with st.spinner(get_text('generating_excel_report')):
                        excel_success = export_report(df_filtered_standard, standard_report_config, path_dict['output_file'])
                    if excel_success:
                        st.success(get_text('excel_report_generated').format(os.path.basename(path_dict['output_file'])))
                        report_generated = True
                    else:
                        st.error(get_text('failed_to_generate_excel'))

                if export_pdf:
                    with st.spinner(get_text('generating_pdf_report')):
                        pdf_success = export_pdf_report(df_filtered_standard, standard_report_config, path_dict['pdf_report'], path_dict['logo_path'])
                    if pdf_success:
                        st.success(get_text('pdf_report_generated').format(os.path.basename(path_dict['pdf_report'])))
                        report_generated = True
                    else:
                        st.error(get_text('failed_to_generate_pdf'))

                if report_generated:
                    if export_excel and os.path.exists(path_dict['output_file']):
                        with open(path_dict['output_file'], "rb") as f:
                            st.download_button(get_text("download_excel"), data=f, file_name=os.path.basename(path_dict['output_file']), use_container_width=True, key='download_excel_std_btn')
                    if export_pdf and os.path.exists(path_dict['pdf_report']):
                        with open(path_dict['pdf_report'], "rb") as f:
                            st.download_button(get_text("download_pdf"), data=f, file_name=os.path.basename(path_dict['pdf_report']), use_container_width=True, key='download_pdf_std_btn')
                else:
                    st.error(get_text('error_generating_report'))


# =========================================================================
# COMPARISON REPORT TAB
# =========================================================================
with tab_comparison_report_main:
    st.header(get_text('comparison_report_header'))

    # Define the mapping from text key to (Vietnamese_internal_string, English_internal_string)
    # This ensures the correct internal string is passed to backend, regardless of UI language
    internal_comparison_modes_map = {
        'compare_projects_month': ("So SÃ¡nh Dá»± Ãn Trong Má»™t ThÃ¡ng", "Compare Projects in a Month"),
        'compare_projects_year': ("So SÃ¡nh Dá»± Ãn Trong Má»™t NÄƒm", "Compare Projects in a Year"),
        'compare_one_project_over_time': ("So SÃ¡nh Má»™t Dá»± Ãn Qua CÃ¡c ThÃ¡ng/NÄƒm", "Compare One Project Over Time (Months/Years)")
    }

    # Khá»Ÿi táº¡o giÃ¡ trá»‹ máº·c Ä‘á»‹nh náº¿u chÆ°a cÃ³ trong session_state
    if 'selected_comparison_mode_key' not in st.session_state:
        # Máº·c Ä‘á»‹nh chá»n key Ä‘áº§u tiÃªn trong danh sÃ¡ch
        st.session_state.selected_comparison_mode_key = list(internal_comparison_modes_map.keys())[0]

    # Táº¡o list cÃ¡c options Ä‘á»ƒ hiá»ƒn thá»‹ trong selectbox
    # vÃ  má»™t map Ä‘á»ƒ tÃ¬m key tá»« display text
    display_options = []
    display_to_key_map = {}
    for key in internal_comparison_modes_map.keys():
        display_text = get_text(key)
        display_options.append(display_text)
        display_to_key_map[display_text] = key

    # Láº¥y giÃ¡ trá»‹ hiá»ƒn thá»‹ máº·c Ä‘á»‹nh dá»±a trÃªn key Ä‘Ã£ lÆ°u
    default_display_value = get_text(st.session_state.selected_comparison_mode_key)
    
    # Äáº£m báº£o giÃ¡ trá»‹ máº·c Ä‘á»‹nh tá»“n táº¡i trong display_options Ä‘á»ƒ trÃ¡nh lá»—i
    # Náº¿u khÃ´ng tÃ¬m tháº¥y, fallback vá» má»¥c Ä‘áº§u tiÃªn vÃ  cáº­p nháº­t session_state
    try:
        current_index = display_options.index(default_display_value)
    except ValueError:
        # GiÃ¡ trá»‹ máº·c Ä‘á»‹nh khÃ´ng tÃ¬m tháº¥y trong options hiá»‡n táº¡i, fallback vá» Ä‘áº§u tiÃªn
        current_index = 0
        st.session_state.selected_comparison_mode_key = display_to_key_map[display_options[0]]
        default_display_value = display_options[0] # Cáº­p nháº­t láº¡i default_display_value cho Ä‘Ãºng

    selected_comparison_display = st.selectbox(
        get_text('select_comparison_mode'),
        options=display_options,
        index=current_index, # Äáº·t index dá»±a trÃªn giÃ¡ trá»‹ máº·c Ä‘á»‹nh Ä‘Ã£ Ä‘Æ°á»£c kiá»ƒm tra
        key='comparison_mode_select_tab_main'
    )
    
    # Cáº­p nháº­t key lá»±a chá»n vÃ o session_state khi ngÆ°á»i dÃ¹ng thay Ä‘á»•i
    current_selected_key = display_to_key_map[selected_comparison_display]
    if st.session_state.selected_comparison_mode_key != current_selected_key:
        st.session_state.selected_comparison_mode_key = current_selected_key


    # Láº¥y giÃ¡ trá»‹ chuá»—i ná»™i bá»™ (internal string) Ä‘á»ƒ truyá»n vÃ o backend
    # Dá»±a trÃªn key Ä‘Ã£ lÆ°u vÃ  ngÃ´n ngá»¯ hiá»‡n táº¡i
    vi_val, en_val = internal_comparison_modes_map[st.session_state.selected_comparison_mode_key]
    if st.session_state.lang == 'vi':
        comparison_mode = vi_val
    else: # 'en'
        comparison_mode = en_val

    st.subheader(get_text('filter_data_for_comparison'))

    comp_years = []
    comp_months = []
    comp_projects = []
    validation_error = False # Flag to check input errors

    # State management for comparison projects
    if 'comparison_selected_projects' not in st.session_state:
        st.session_state.comparison_selected_projects = [] # Default to empty

    comp_projects = st.multiselect(
        get_text('select_projects_comp'),
        options=all_projects,
        default=[p for p in st.session_state.comparison_selected_projects if p in all_projects], # Ensure default is valid
        key='comp_projects_select_tab_common'
    )
    st.session_state.comparison_selected_projects = comp_projects # Update state


    if comparison_mode == "So SÃ¡nh Má»™t Dá»± Ãn Qua CÃ¡c ThÃ¡ng/NÄƒm" or comparison_mode == "Compare One Project Over Time (Months/Years)":
        if len(comp_projects) != 1:
            st.warning(get_text('select_single_project_warning'))
            validation_error = True

        # State management for selected years in "Over Time" mode
        if 'comparison_selected_years_over_time' not in st.session_state:
            st.session_state.comparison_selected_years_over_time = []

        selected_years_over_time = st.multiselect(
            get_text('select_years_for_over_time_months'),
            options=all_years,
            default=[y for y in st.session_state.comparison_selected_years_over_time if y in all_years], # Ensure default is valid
            key='comp_years_select_tab_over_time'
        )
        st.session_state.comparison_selected_years_over_time = selected_years_over_time # Update state
        comp_years = selected_years_over_time # Assign to comp_years for config

        # State management for selected months in "Over Time" mode (if single year selected)
        if 'comparison_selected_months_over_time' not in st.session_state:
            st.session_state.comparison_selected_months_over_time = []


        if len(selected_years_over_time) == 1:
            st.info(get_text('comparison_over_months_note').format(selected_years_over_time[0]))
            comp_months = st.multiselect(
                get_text('select_months_for_single_year'),
                options=all_months,
                default=[m for m in st.session_state.comparison_selected_months_over_time if m in all_months], # Ensure default is valid
                key='comp_months_select_tab_over_time'
            )
            st.session_state.comparison_selected_months_over_time = comp_months # Update state

            if not comp_months:
                st.warning(get_text('no_month_selected_for_single_year'))
                validation_error = True

        elif len(selected_years_over_time) > 1:
            st.info(get_text('comparison_over_years_note'))
            comp_months = [] # Months are ignored for multi-year comparison
            st.session_state.comparison_selected_months_over_time = [] # Clear months state
        else:
            st.warning(get_text('no_comparison_criteria_selected'))
            validation_error = True
            comp_months = [] # Ensure empty
            st.session_state.comparison_selected_months_over_time = [] # Clear months state

    elif comparison_mode in ["So SÃ¡nh Dá»± Ãn Trong Má»™t ThÃ¡ng", "Compare Projects in a Month", "So SÃ¡nh Dá»± Ãn Trong Má»™t NÄƒm", "Compare Projects in a Year"]:
        col_comp1, col_comp2 = st.columns(2)
        with col_comp1:
            # State management for general comparison years
            if 'comparison_selected_years_general' not in st.session_state:
                st.session_state.comparison_selected_years_general = []

            comp_years = st.multiselect(
                get_text('select_years'),
                options=all_years,
                default=[y for y in st.session_state.comparison_selected_years_general if y in all_years],
                key='comp_years_select_tab_general'
            )
            st.session_state.comparison_selected_years_general = comp_years # Update state

        with col_comp2:
            # State management for general comparison months
            if 'comparison_selected_months_general' not in st.session_state:
                st.session_state.comparison_selected_months_general = []

            if comparison_mode in ["So SÃ¡nh Dá»± Ãn Trong Má»™t ThÃ¡ng", "Compare Projects in a Month"]:
                comp_months = st.multiselect(
                    get_text('select_months_comp'),
                    options=all_months,
                    default=[m for m in st.session_state.comparison_selected_months_general if m in all_months],
                    key='comp_months_select_tab_general'
                )
                st.session_state.comparison_selected_months_general = comp_months # Update state
            else:
                comp_months = [] # Months are not relevant for yearly comparison
                st.session_state.comparison_selected_months_general = [] # Clear months state

        if not comp_years:
            st.warning(get_text('no_comparison_criteria_selected'))
            validation_error = True
        
        if comparison_mode in ["So SÃ¡nh Dá»± Ãn Trong Má»™t ThÃ¡ng", "Compare Projects in a Month"] and not comp_months:
            st.warning(get_text('no_comparison_criteria_selected'))
            validation_error = True

        if not comp_projects:
            st.warning(get_text('no_project_selected_warning_standard')) # Reusing standard report message
            validation_error = True
            

    st.markdown("---")
    st.subheader(get_text("export_options"))
    export_excel_comp = st.checkbox(get_text("export_excel_option"), value=True, key='export_excel_comp')
    export_pdf_comp = st.checkbox(get_text("export_pdf_option"), value=False, key='export_pdf_comp')

    if st.button(get_text('generate_comparison_report_btn'), key='generate_comparison_report_btn_tab'):
        if not export_excel_comp and not export_pdf_comp:
            st.warning(get_text("warning_select_export_format"))
        elif validation_error:
            # Error messages already displayed by specific conditions
            pass
        else:
            # DEBUG print statements (giá»¯ láº¡i Ä‘á»ƒ cháº©n Ä‘oÃ¡n váº¥n Ä‘á» dá»± Ã¡n)
            print(f"DEBUG: Comparison Mode selected before filter: {comparison_mode}")
            print(f"DEBUG: Selected Projects before filter: {comp_projects}")
            print(f"DEBUG: Selected Years before filter: {comp_years}")
            print(f"DEBUG: Selected Months before filter: {comp_months}")


            comparison_config = {
                'selected_years': comp_years,
                'selected_months': comp_months,
                'selected_projects': comp_projects,
                # 'selected_months_over_time' khÃ´ng cáº§n truyá»n riÃªng náº¿u Ä‘Ã£ gÃ¡n vÃ o comp_months
                # nÃ³ Ä‘Ã£ Ä‘Æ°á»£c xá»­ lÃ½ trong logic trÃªn
            }
            
            # Print the final config before calling the function
            print(f"DEBUG: Final comparison_config sent to filter: {comparison_config}")

            df_filtered_comparison, comparison_filter_message = apply_comparison_filters(df_raw, comparison_config, comparison_mode)

            if df_filtered_comparison.empty:
                st.warning(get_text('no_data_after_filter_comparison').format(comparison_filter_message))
            else:
                st.success(get_text('data_filtered_success'))
                st.subheader(get_text('comparison_data_preview'))
                st.dataframe(df_filtered_comparison)

                report_generated_comp = False
                if export_excel_comp:
                    with st.spinner(get_text('generating_comparison_excel')):
                        excel_success_comp = export_comparison_report(df_filtered_comparison, comparison_config, comparison_mode, path_dict['comparison_output_file'])
                    if excel_success_comp:
                        st.success(get_text('comparison_excel_generated').format(os.path.basename(path_dict['comparison_output_file'])))
                        report_generated_comp = True
                    else:
                        st.error(get_text('failed_to_generate_comparison_excel'))

                if export_pdf_comp:
                    with st.spinner(get_text('generating_comparison_pdf')):
                        pdf_success_comp = export_comparison_pdf_report(df_filtered_comparison, comparison_config, comparison_mode, path_dict['comparison_pdf_report'], path_dict['logo_path'])
                    if pdf_success_comp:
                        st.success(get_text('comparison_pdf_generated').format(os.path.basename(path_dict['comparison_pdf_report'])))
                        report_generated_comp = True
                    else:
                        st.error(get_text('failed_to_generate_comparison_pdf'))
                
                if report_generated_comp:
                    if export_excel_comp and os.path.exists(path_dict['comparison_output_file']):
                        with open(path_dict['comparison_output_file'], "rb") as f:
                            st.download_button(get_text("download_comparison_excel"), data=f, file_name=os.path.basename(path_dict['comparison_output_file']), use_container_width=True, key='download_excel_comp_btn')
                    if export_pdf_comp and os.path.exists(path_dict['comparison_pdf_report']):
                        with open(path_dict['comparison_pdf_report'], "rb") as f:
                            st.download_button(get_text("download_comparison_pdf"), data=f, file_name=os.path.basename(path_dict['comparison_pdf_report']), use_container_width=True, key='download_pdf_comp_btn')
                else:
                    st.error(get_text('error_generating_report'))


# =========================================================================
# DATA PREVIEW TAB
# =========================================================================
with tab_data_preview_main:
    st.subheader(get_text('raw_data_preview_header'))
    if not df_raw.empty:
        st.dataframe(df_raw.head(100))
    else:
        st.info(get_text('no_raw_data'))

# =========================================================================
# USER GUIDE TAB
# =========================================================================
with tab_user_guide_main:
    st.markdown(f"### {get_text('user_guide')}")
    st.markdown("""
    - Select filters: mode, year, month, project
    - Select report export format (Excel, PDF or both)
    - Click "Create report"
    - Download generated report
    """)
