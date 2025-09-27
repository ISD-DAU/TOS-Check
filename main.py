import streamlit as st
from PIL import Image

platforms = ["Facebook", "Instagram", "Discord", "X", "TikTok", "YouTube", "Other"]
tos_violations = ["No", "Yes"]
published_research = ["Yes", "No"]
violation_extensive = ["Under 10,000 violations", "10,000+ violations"]
pii_involved = ["Yes", "No"]

# Example email template for permission
email_template = """
Hi!
I'm reaching out to ask for your permission to proceed with a project that involves [platform] and may violate its Terms of Service. The research will be published, it involves [number] violations, and there are concerns about sensitive PII.
Please let me know if you need more information or if this requires further review.
Best regards,
[Your Name]
"""

def calculate_risk(platform, tos_violations, published_research, violation_extensive, pii_involved, violation_actor):
    # Initialize risk score
    risk = 0
    
    if platform == "Discord":
        # Higher risk for platforms like Discord due to privacy expectations
        risk += 1
    
    if published_research == "Yes":  # Changed to check for "Yes" string
        risk += 1
    
    if violation_extensive == "10,000+ violations":
        if platform == "Discord" or platform == "Other closed platforms" or pii_involved == 'Yes':
            risk += 2
        else:
            risk += 1
    
    if pii_involved == "Yes":  # Changed to check for "Yes" string
        risk += 1
    
    # Adjust risk based on who is doing the violation
    if violation_actor == "Someone else":
        risk -= 1
    
    # Ensure risk doesn't go below 0
    risk = max(0, risk)
    
    return risk

def main():
    # Initialize session state
    if 'platform_choice' not in st.session_state:
        st.session_state.platform_choice = None
    if 'tos_active' not in st.session_state:
        st.session_state.tos_active = None
    if 'published' not in st.session_state:
        st.session_state.published = None
    if 'violation_count' not in st.session_state:
        st.session_state.violation_count = None
    if 'pii_check' not in st.session_state:
        st.session_state.pii_check = None
    if 'violation_actor' not in st.session_state:
        st.session_state.violation_actor = None
    
    # Determine if we should show mad reb based on current state
    mad_reb = (st.session_state.platform_choice == "X" or 
               st.session_state.tos_active == "Yes")
    
    # Create columns for title and icon
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("<h1 style='margin-bottom: 0;'>Ask Reb</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='margin-top: 0; color: gray;'>The ToS Violation Risk Expert</h2>", unsafe_allow_html=True)
    with col2:
        try:
            if mad_reb:
                icon = Image.open("bagel-icon-mad.png")
                st.image(icon, width=80)
            else:
                icon = Image.open("bagel-icon.png")
                st.image(icon, width=80)
        except FileNotFoundError:
            pass

    # Platform selection
    st.write("**1. Which platform are we dealing with?**")
    platform_choice = st.selectbox(
        "",
        platforms + ["Other closed platforms"],
        label_visibility="collapsed",
        index=None,
        placeholder="Select a platform...",
        key="platform_select"
    )
    
    # Update session state
    if platform_choice != st.session_state.platform_choice:
        st.session_state.platform_choice = platform_choice
        st.rerun()  # Refresh to update the icon
    
    # Display immediate warning only for platform X and stop flow
    if platform_choice == "X":
        st.markdown("### ⚠️ Violating X's terms of service is prohibited")
        st.markdown("---")
        return  # Stop here if X is selected
    
    # Only show question 2 if platform is selected (and not X)
    if platform_choice:
        # Active prohibition check
        st.write("**2. Does the project actively prohibit terms of service violations?**")
        tos_active = st.radio("", tos_violations, label_visibility="collapsed", index=None)
        
        # Update session state
        if tos_active != st.session_state.tos_active:
            st.session_state.tos_active = tos_active
            st.rerun()  # Refresh to update the icon
        
        # Display immediate warning for project prohibition
        if tos_active == "Yes":
            st.markdown("### 🚫 Violating terms of service is prohibited when prohibited by the project")
            st.markdown("---")
            return  # Stop here if prohibited by project
        
            # Only show remaining questions if TOS is not prohibited by project
            if tos_active == "No":
                # Published research status
                st.write("**3. Will this research be published?**")
                published = st.radio("", ["No", "Yes"], 
                                    label_visibility="collapsed", 
                                    key="published_radio", 
                                    index=None if st.session_state.published is None else (0 if st.session_state.published == "No" else 1))
                if published != st.session_state.published:
                    st.session_state.published = published
                
                # Only show question 4 if question 3 is answered
                if published is not None:
                    # Violation extent
                    st.write("**4. How many violations are we looking at?**")
                    violation_count = st.selectbox("", violation_extensive,
                                                  label_visibility="collapsed",
                                                  index=None if st.session_state.violation_count is None else (violation_extensive.index(st.session_state.violation_count) if st.session_state.violation_count in violation_extensive else None),
                                                  placeholder="Select violation count...")
                    if violation_count != st.session_state.violation_count:
                        st.session_state.violation_count = violation_count
                    
                    # Only show question 5 if question 4 is answered
                    if violation_count:
                        # Involvement of sensitive PII
                        st.write("**5. Does the project involve sensitive PII (Personally Identifiable Information)?**")
                        pii_check = st.radio("", ["No", "Yes"], 
                                            label_visibility="collapsed", 
                                            key="pii_radio", 
                                            index=None if st.session_state.pii_check is None else (0 if st.session_state.pii_check == "No" else 1))
                        if pii_check != st.session_state.pii_check:
                            st.session_state.pii_check = pii_check
                        
                        # Only show question 6 if question 5 is answered
                        if pii_check is not None:
                            # Who is doing the violation
                            st.write("**7. Are you doing the violation or has someone else (e.g. someone else scraped data that you want to use)?**")
                            violation_actor = st.radio("", ["Yourself", "Someone else"], 
                                                      label_visibility="collapsed", 
                                                      key="actor_radio", 
                                                      index=None if st.session_state.violation_actor is None else (0 if st.session_state.violation_actor == "Yourself" else 1))
                            if violation_actor != st.session_state.violation_actor:
                                st.session_state.violation_actor = violation_actor
                                
                            # Only show calculate button if question 7 is answered
                            if violation_actor:
                                # Add button to calculate risk
                                if st.button("Calculate Risk", type="primary"):
                                    # Debug: Show what values we're passing -- removed for now
                                    #st.write("Debug info:")
                                    #st.write(f"Platform: {platform_choice}")
                                    #st.write(f"TOS Active: {tos_active}")
                                    #st.write(f"Published: {published}")
                                    #st.write(f"Violation Count: {violation_count}")
                                    #st.write(f"PII Check: {pii_check}")
                                    #st.write(f"Violation Actor: {violation_actor}")
                                    
                                    # Calculate risk and display results
                                    total_risk = calculate_risk(platform_choice, tos_active, published, violation_count, pii_check, violation_actor)
                                    
                                    st.markdown("---")  # Add separator before results
                                    
                                    if total_risk >= 4:
                                        st.error(f"Project is deemed prohibited with a risk score of {total_risk}. No further action can be taken.")
                                    elif total_risk >= 2:
                                        st.warning(f"Risk level indicates the need for higher-level approval. Risk score: {total_risk}. Please refer to the email template below for guidance.")
                                        # Display example email for warning level only
                                        st.subheader("Example Email for Permission:")
                                        st.markdown(email_template.replace("[platform]", platform_choice).replace("[number]", str(violation_count)))
                                    else:
                                        st.success(f"Proceed with caution! Risk score: {total_risk}")
                                    
                                    # Special note for Discord
                                    if platform_choice == "Discord":
                                        st.info("📋 **Additional Note:** For Discord projects, please also check with our ethics officer before proceeding.")
                                    if pii_check == "Yes":
                                        st.info("📋 **Additional Note:** For collecting sensitive data, please also check with our ethics officer before proceeding.")

if __name__ == "__main__":
    main()
