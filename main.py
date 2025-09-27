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
    # Create columns for title and icon
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("<h1 style='margin-bottom: 0;'>Ask Reb</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='margin-top: 0; color: gray;'>The ToS Violation Risk Expert</h2>", unsafe_allow_html=True)
    with col2:
        try:
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
        placeholder="Select a platform..."
    )
    
    # Display immediate warning only for platform X and stop flow
    if platform_choice == "X":
        st.markdown("### ⚠️ Violating X's terms of service is prohibited")
        st.markdown("---")
        return  # Stop here if X is selected
    
    # Only show question 2 if platform is selected (and not X)
    if platform_choice:
        # Active prohibition check
        st.write("**2. Does the relevant project actively prohibit terms of service violations?**")
        tos_active = st.radio("", tos_violations, label_visibility="collapsed", index=None)
        
        # Display immediate warning for project prohibition
        if tos_active == "Yes":
            st.markdown("### 🚫 Violating terms of service is prohibited when prohibited by the project")
            st.markdown("---")
            return  # Stop here if prohibited by project
        
        # Only show remaining questions if TOS is not prohibited by project
        if tos_active == "No":
            # Published research status
            st.write("**3. Will this research be published?**")
            published = st.radio("", ["No", "Yes"], label_visibility="collapsed", key="published_radio", index=None)
            
            # Only show question 4 if question 3 is answered
            if published is not None:
                # Violation extent
                st.write("**4. How many violations are we looking at?**")
                violation_count = st.selectbox(
                    "",
                    violation_extensive,
                    label_visibility="collapsed",
                    index=None,
                    placeholder="Select violation count..."
                )
                
                # Only show question 5 if question 4 is answered
                if violation_count:
                    # Involvement of sensitive PII
                    st.write("**5. Does it involve sensitive data, such as PII from personal Facebook pages.**")
                    pii_check = st.radio("", ["No", "Yes"], label_visibility="collapsed", key="pii_radio", index=None)
                    
                    # Only show question 6 if question 5 is answered
                    if pii_check is not None:
                    
                        # Who is doing the violation
                        st.write("**6. Are you doing the violation or has someone else (e.g. someone else scraped data that you want to use)?**")
                        violation_actor = st.radio("", ["Yourself", "Someone else"], label_visibility="collapsed", key="actor_radio", index=None)
                        
                        # Only show calculate button if question 6 is answered
                        if violation_actor:
                            # Add button to calculate risk
                            if st.button("Calculate Risk", type="primary"):
                                # Debug: Show what values we're passing
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
                                    st.error(f"Violation is likely prohibited with a risk score of {total_risk}. Recommend no further action - but do consult legal counsel if important.")
                                elif total_risk >= 2:
                                    st.warning(f"Risk level indicates the need for higher-level approval. Risk score: {total_risk}. Please refer to the email template below for guidance.")
                                    # Display example email for warning level only
                                    st.subheader("Example Email for Permission:")
                                    st.markdown(email_template.replace("[platform]", platform_choice).replace("[number]", str(violation_count)))
                                else:
                                    st.success(f"Proceed with caution! Risk score: {total_risk}")
                                
                                # Special note for Discord
                                if platform_choice == "Discord":
                                    st.info("📋 **Additional Note:** For ToS violations on closed platforms like Discord, please also check with our ethics officer before proceeding.")
                                if pii_check == "Yes":
                                    st.info("📋 **Additional Note:** For sensitive data, please also check with our ethics officer before proceeding.")

if __name__ == "__main__":
    main()
