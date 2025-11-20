import streamlit_authenticator as stauth

plain_text_passwords = ["your_password_here"]
hashed_passwords = stauth.Hasher(plain_text_passwords).generate()
print(hashed_passwords[0])
