import streamlit as st
import time

from wedding_organizer_agent import WeddingOrganizerAgent

st.set_page_config(
    page_title="Wedding Song Checker",
    page_icon="💕",
    layout="centered"
)

st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #E91E63;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    .powered-by {
        text-align: center;
        color: #FFA726;
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }
    .section-header {
        color: #333;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 2rem 0 1rem 0;
        text-align: center;
    }
    .result-box {
        background: linear-gradient(135deg, #C8E6C9, #A5D6A7);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        border: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .result-header {
        color: #2E7D32;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .song-title {
        color: #E91E63;
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .song-description {
        color: #555;
        font-size: 1rem;
        line-height: 1.5;
        margin-bottom: 1rem;
    }
    .magic-text {
        color: #FFA726;
        font-size: 0.9rem;
        font-style: italic;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid #eee;
        color: #888;
        font-size: 0.8rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #E91E63, #F06292);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
        width: 100%;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #C2185B, #E91E63);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(233, 30, 99, 0.3);
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #E0E0E0;
        padding: 0.75rem;
        font-size: 1rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #E91E63;
        box-shadow: 0 0 0 2px rgba(233, 30, 99, 0.2);
    }
</style>
""", unsafe_allow_html=True)

WEDDING_SONGS_DB = {
    "taylor swift": {
        "cornelia street": {
            "suitable": True,
            "reason": "Esta música tem um tom positivo e celebratório que funcionaria bem para uma atmosfera de casamento.",
            "magic_factor": "Esta música tornará seu dia ainda mais mágico! ✨"
        },
        "love story": {
            "suitable": True,
            "reason": "Uma música romântica clássica perfeita para momentos especiais de casamento.",
            "magic_factor": "Uma escolha atemporal que encantará todos os convidados! ✨"
        },
        "you belong with me": {
            "suitable": True,
            "reason": "Tem energia positiva e é sobre encontrar o amor verdadeiro, ideal para casamentos.",
            "magic_factor": "Vai criar momentos inesquecíveis na sua celebração! ✨"
        }
    },
    "ed sheeran": {
        "perfect": {
            "suitable": True,
            "reason": "Uma das músicas de casamento mais populares, romântica e emotiva.",
            "magic_factor": "Literalmente perfeita para o seu grande dia! ✨"
        },
        "thinking out loud": {
            "suitable": True,
            "reason": "Letra romântica sobre amor duradouro, ideal para casamentos.",
            "magic_factor": "Tocará o coração de todos os presentes! ✨"
        }
    },
    "john legend": {
        "all of me": {
            "suitable": True,
            "reason": "Uma declaração de amor completa e incondicional, perfeita para casamentos.",
            "magic_factor": "Uma música que expressa amor verdadeiro e eterno! ✨"
        }
    }
}

wedding_organizer_agent = WeddingOrganizerAgent()

def evaluate_song(song_title, artist_name):
    """Avalia se uma música é adequada para casamento"""
    song = song_title.lower().strip()
    artist = artist_name.lower().strip()

    return wedding_organizer_agent.run(artist, song)

if 'evaluation_done' not in st.session_state:
    st.session_state.evaluation_done = False
if 'song_result' not in st.session_state:
    st.session_state.song_result = None

st.markdown('<div class="main-header">💕 Wedding Song Checker 🎵</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Encontre a trilha sonora perfeita para o seu grande dia</div>', unsafe_allow_html=True)
st.markdown('<div class="powered-by">✨ Com o Wedding Song Checker, você descobre rapidamente se uma música é apropriada para o grande dia. <br /> Evite letras com linguagem explícita, temas negativos ou que não combinam com o clima de amor e celebração. <br /> Nossa inteligência artificial analisa a letra e te mostra se ela é ideal para o seu momento especial. ✨</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">🎵 Avaliar uma música</div>', unsafe_allow_html=True)

with st.container():
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown("💕 **Nome do artista**")
        artist_name = st.text_input("", placeholder="Digite o nome do artista", label_visibility="collapsed", key="artist_input")
        
        st.markdown("") 

        st.markdown("🎵 **Título da música**")
        song_title = st.text_input("", placeholder="Digite o título da música", label_visibility="collapsed", key="song_input")
        
        st.markdown("") 
        
        if st.button("✨ Avaliar música"):
            if song_title and artist_name:
                with st.spinner("Avaliando música..."):
                    time.sleep(1.5)
                
                result = evaluate_song(song_title, artist_name)

                print(result)

                st.markdown(result)

                st.session_state.song_result = {
                    'title': song_title,
                    'artist': artist_name,
                    'evaluation': result
                }
                st.session_state.evaluation_done = True
                st.rerun()
            else:
                st.error("Por favor, preencha o título da música e o nome do artista.")

if st.session_state.evaluation_done and st.session_state.song_result:
    result = st.session_state.song_result
    
    if result['evaluation']['is_appropriate']:
        st.markdown("""
        <div class="result-box">
            <div class="result-header">✅ Música ideal para o seu casamento!</div>
            <div class="song-title">🎵 "{}" by {}</div>
            <div class="song-description">{}</div>
        </div>
        """.format(
            result['title'],
            result['artist'], 
            result['evaluation']['reason'],
        ), unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFCDD2, #F8BBD9); padding: 2rem; border-radius: 15px; text-align: center; margin: 2rem 0;">
            <div style="color: #C62828; font-size: 1.3rem; font-weight: bold; margin-bottom: 1rem;">
                🤔 Considere outras opções
            </div>
            <div class="song-title">🎵 "{}" by {}</div>
            <div class="song-description">{}</div>
        </div>
        """.format(
            result['title'],
            result['artist'],
            result['evaluation']['reason']
        ), unsafe_allow_html=True)

# if st.session_state.evaluation_done:
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         if st.button("🔄 Avaliar outra música"):
#             st.session_state.evaluation_done = False
#             st.session_state.song_result = None
#             st.rerun()

# Footer
st.markdown("""
<div class="footer">
    © 2025 Wedding Song Checker. 
</div>
""", unsafe_allow_html=True)