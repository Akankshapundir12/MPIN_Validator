import streamlit as st
from datetime import datetime
from main import MPINValidator

def format_date(date):
    return date.strftime('%d-%m-%Y')

def display_reasons(reasons):
    if not reasons:
        return
    
    st.markdown("### Reasons for Weakness:")
    
    categories = {
        'Common Patterns': ['COMMON_PATTERN'],
        'Demographic Matches': ['DEMOGRAPHIC_DOB_SELF', 'DEMOGRAPHIC_DOB_SPOUSE',
                              'DEMOGRAPHIC_ANNIVERSARY', 'DEMOGRAPHIC_COMBINED'],
        'Format Issues': ['INVALID_FORMAT']
    }
    
    for category, reason_types in categories.items():
        category_reasons = {k: v for k, v in reasons.items() if k in reason_types}
        if category_reasons:
            st.markdown(f"#### {category}")
            for reason_type, explanations in category_reasons.items():
                if reason_type == 'COMMON_PATTERN':
                    st.markdown("This MPIN is commonly used because:")
                    for explanation in explanations:
                        st.markdown(f"- {explanation}")
                elif reason_type == 'DEMOGRAPHIC_COMBINED':
                    st.markdown("This MPIN contains patterns from combined dates:")
                    for explanation in explanations:
                        st.markdown(f"- {explanation}")
                else:
                    for explanation in explanations:
                        st.markdown(f"- {explanation}")

def main():
    st.set_page_config(
        page_title="MPIN Strength Validator",
        page_icon="",
        layout="wide"
    )

    st.title(" MPIN Strength Validator")
    
    validator = MPINValidator()

    input_col, output_col = st.columns([1, 1])

    with input_col:
        st.markdown("### Input Details")
        mpin_type = st.radio(
            "Select MPIN Type",
            ["4-digit MPIN", "6-digit MPIN"],
            horizontal=True
        )

        mpin = st.text_input(
            "Enter your MPIN",
            max_chars=6 if mpin_type == "6-digit MPIN" else 4,
            help="Enter your MPIN (numbers only)",
            placeholder="Enter 4 or 6 digit MPIN"
        )

        dob = st.date_input(
            "Your Date of Birth",
            value=None,
            help="Select your date of birth",
            format="DD-MM-YYYY",
            min_value=datetime(1900, 1, 1),
            max_value=datetime.now()
        )
        
        marital_status = st.radio(
            "Marital Status",
            ["Single", "Married"],
            horizontal=True
        )
        
        if marital_status == "Married":
            spouse_dob = st.date_input(
                "Spouse's Date of Birth",
                value=None,
                help="Select your spouse's date of birth",
                format="DD-MM-YYYY",
                min_value=datetime(1900, 1, 1),
                max_value=datetime.now()
            )
            
            anniversary = st.date_input(
                "Wedding Anniversary",
                value=None,
                help="Select your wedding anniversary date",
                format="DD-MM-YYYY",
                min_value=datetime(1900, 1, 1),
                max_value=datetime.now()
            )
        else:
            spouse_dob = None
            anniversary = None

        validate_button = st.button("Validate MPIN", type="primary", use_container_width=True)

    with output_col:
        st.markdown("### Validation Results")
        
        if validate_button:
            if not mpin:
                st.error("Please enter your MPIN!")
            elif not mpin.isdigit():
                st.error("MPIN must contain only numbers!")
            elif len(mpin) != (6 if mpin_type == "6-digit MPIN" else 4):
                st.error(f"MPIN must be {6 if mpin_type == '6-digit MPIN' else 4} digits long!")
            elif not dob:
                st.error("Please enter your date of birth!")
            elif marital_status == "Married" and (not spouse_dob or not anniversary):
                st.error("Please enter both spouse's date of birth and wedding anniversary!")
            else:
                dob_str = format_date(dob)
                spouse_dob_str = format_date(spouse_dob) if spouse_dob else None
                anniversary_str = format_date(anniversary) if anniversary else None

                strength, reasons, strength_percentage, color = validator.validate_mpin(
                    mpin, dob_str, spouse_dob_str, anniversary_str
                )

                result_col1, result_col2 = st.columns(2)
                
                with result_col1:
                    st.metric(
                        "Strength",
                        strength,
                        f"{strength_percentage}%"
                    )

                with result_col2:
                    if color == "red":
                        st.error("MPIN is Weak")
                    else:
                        st.success("MPIN is Strong")

                if color == "red":
                    st.markdown(
                        f'<div style="background-color: #ffcdd2; padding: 10px; border-radius: 5px;">'
                        f'<div style="width: {strength_percentage}%; background-color: #f44336; height: 20px; border-radius: 5px;"></div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div style="background-color: #c8e6c9; padding: 10px; border-radius: 5px;">'
                        f'<div style="width: {strength_percentage}%; background-color: #4caf50; height: 20px; border-radius: 5px;"></div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                if reasons:
                    st.markdown("#### Reasons for Weakness:")
                    
                    categories = {
                        'Common Patterns': ['COMMON_PATTERN'],
                        'Demographic Matches': ['DEMOGRAPHIC_DOB_SELF', 'DEMOGRAPHIC_DOB_SPOUSE',
                                              'DEMOGRAPHIC_ANNIVERSARY', 'DEMOGRAPHIC_COMBINED'],
                        'Format Issues': ['INVALID_FORMAT']
                    }
                    
                    for category, reason_types in categories.items():
                        category_reasons = {k: v for k, v in reasons.items() if k in reason_types}
                        if category_reasons:
                            st.markdown(f"**{category}**")
                            for reason_type, explanations in category_reasons.items():
                                if reason_type == 'COMMON_PATTERN':
                                    for explanation in explanations:
                                        st.markdown(f"• {explanation}")
                                elif reason_type == 'DEMOGRAPHIC_COMBINED':
                                    for explanation in explanations:
                                        st.markdown(f"• {explanation}")
                                else:
                                    for explanation in explanations:
                                        st.markdown(f"• {explanation}")
                else:
                    st.success("No patterns detected! This is a strong MPIN.")
        else:
            st.info("Enter your details and click 'Validate MPIN' to see the results.")
            
if __name__ == "__main__":
    main() 