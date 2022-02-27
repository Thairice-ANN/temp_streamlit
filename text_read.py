from gtts import gTTS
import win32com.client as wincl
import streamlit as st

def main():
	st.title('君へ')
	text = st.text_input(label='Message',value='Fight!')

	if st.button('Speak'):
		audio = 'speech.mp3'
		tts = gTTS(text=text, lang='ja')
		tts.save(audio)
		st.audio(audio)

if __name__=='__main__':
	main()