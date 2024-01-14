
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Définissez le chemin complet du fichier audio que vous souhaitez transcrire
filename = r"C:\Users\INSEP\Downloads\WhatsApp Audio 2023-09-25 à 15.33.33.waptt (1).wav"
path = r"C:\Users\INSEP\Downloads\WhatsApp Audio 2023-09-25 à 15.33.33.waptt (1).wav"

# Initialisez le recognizer
r = sr.Recognizer()         

# Ouvrez le fichier audio
with sr.AudioFile(filename) as source :         
    # Écoutez les données (chargez l'audio en mémoire)
    audio_data = r.record(source)        
    # Reconnaissez (convertissez de la parole en texte)
    text = r.recognize_google(audio_data)        
    print(text)            
                                                                                                                                                                                         
# Fonction pour transcrire un fichier audio                                                                                                        
def transcribe_audio(path):
    with sr.AudioFile(path) as source:
        audio_listened = r.record(source)
        try:
            text = r.recognize_google(audio_listened, language="fr-FR")
        except sr.UnknownValueError as e:
            print("Erreur:", str(e))
            text = ""
    return text
                                       
# Fonction qui divise le fichier audio en morceaux sur le silence et applique la reconnaissance vocale
def get_large_audio_transcription_on_silence(path):
    # Ouvrez le fichier audio en utilisant pydub
    sound = AudioSegment.from_file(path)
    # Divisez le son là où il y a du silence de 500 millisecondes ou plus et obtenez des morceaux
    chunks = split_on_silence(sound,
        # Expérimentez avec cette valeur pour votre fichier audio cible
        min_silence_len=500,
        # Ajustez ceci selon les besoins
        silence_thresh=sound.dBFS - 14,
        # Conservez le silence pendant 1 seconde, réglable également
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # Créez un répertoire pour stocker les morceaux audio
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # Traitez chaque morceau
    for i, audio_chunk in enumerate(chunks, start=1):
        # Exportez le morceau audio et enregistrez-le dans le répertoire `folder_name`                      
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")                                              
        audio_chunk.export(chunk_filename, format="wav")                                 
        # Reconnaissez le morceau                                                                                                                             
        try:
            text = transcribe_audio(chunk_filename)
        except sr.UnknownValueError as e:
            print("Erreur :", str(e))
        else:                                           
            text = f"{text.capitalize()}. "
            print(chunk_filename, ":", text)
            whole_text += text
    # Retournez le texte pour tous les morceaux détectés
    return whole_text                              
        
# Définissez le chemin complet du fichier audio pour cette fonction                                              
audio_path =  r"C:\Users\INSEP\Downloads\WhatsApp Audio 2023-09-25 à 15.33.33.waptt (1).wav"              
# Appelez la fonction pour transcrire un fichier audio volumineux               
print("\nTexte complet:", get_large_audio_transcription_on_silence(audio_path))                                       
                   