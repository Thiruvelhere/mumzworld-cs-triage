import streamlit as st
from triage import triage_email

st.set_page_config(page_title='Mumzworld CS Triage', page_icon='👶')
st.title('Mumzworld CS Email Triage')
st.caption('Paste a customer email in English or Arabic')

email_input = st.text_area('Customer email:', height=180,
    placeholder='Paste email here...')

if st.button('Triage Email') and email_input.strip():
    with st.spinner('Analysing...'):
        result = triage_email(email_input)

    if result.get('validation_failed'):
        st.error('Schema validation failed')
        st.code(result.get('raw_output', ''))
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric('Intent', result['intent'].upper())
        col2.metric('Urgency', result['urgency'].upper())
        conf = result['confidence']
        col3.metric('Confidence', f'{conf:.0%}' if conf else 'N/A')

        st.info(f'Reasoning: {result["reasoning"]}')

        if result['out_of_scope']:
            st.warning('Out of scope — no reply generated')
        else:
            st.subheader('Draft Reply — English')
            st.write(result['reply_en'])
            st.subheader('Draft Reply — Arabic')
            st.write(result['reply_ar'])
