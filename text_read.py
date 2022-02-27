from gtts import gTTS
import streamlit as st

def main():
	st.title('マス君へ')

	if st.button('Speak'):
		audio = 'speech.mp3'
		tts = gTTS(text='マス君、漫才がんばってね', lang='ja')
		tts.save(audio)
		st.audio(audio)

if __name__=='__main__':
	main()