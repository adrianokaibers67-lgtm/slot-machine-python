
import random
import tkinter as tk
import threading

# Som (Windows)
try:
    import winsound
    def som_giro():
        winsound.Beep(800, 80)

    def som_vitoria():
        winsound.Beep(1200, 150)
        winsound.Beep(1500, 150)
except:
    def som_giro(): pass
    def som_vitoria(): pass

# ====================
# CONFIGURAÇÕES
# ====================
FICHAS_INICIAIS = 100
simbolos = ["🍒", "🍋", "⭐", "💎"]

cores_simbolos = {
    "🍒": "#ff4d4d",
    "🍋": "#ffe600",
    "⭐": "#ffd700",
    "💎": "#00cfff"
}

fichas = FICHAS_INICIAIS
vitorias = 0
rodando = False

# ====================
# FUNÇÕES DO JOGO
# ====================
def girar():
    global fichas, rodando

    if fichas <= 0 or rodando:
        return

    rodando = True
    fichas -= 1
    atualizar_fichas()

    threading.Thread(target=som_giro).start()
    animar_giro(0)

def animar_giro(contador):
    if contador < 12:
        s1 = random.choice(simbolos)
        s2 = random.choice(simbolos)
        s3 = random.choice(simbolos)
        label_simbolos.config(text=f"{s1}   {s2}   {s3}", fg="#ffffff", bg="#2b2b2b")
        janela.after(80, animar_giro, contador + 1)
    else:
        finalizar_rodada()

def finalizar_rodada():
    global fichas, vitorias, rodando

    s1, s2, s3 = label_simbolos.cget("text").split()
    label_simbolos.config(fg=cores_simbolos.get(s1, "#ffffff"))

    if s1 == s2 == s3:
        fichas += 50
        vitorias += 1
        atualizar_vitorias()
        label_resultado.config(
            text="🎉 PRÊMIO! +50 FICHAS 🎉",
            fg="#00ff88"
        )
        threading.Thread(target=som_vitoria).start()
        efeito_vitoria(0)
    else:
        label_resultado.config(
            text="❌ NÃO FOI DESSA VEZ",
            fg="#ff5555"
        )
        label_simbolos.config(bg="#4f1f1f")

    atualizar_fichas()
    rodando = False

    if fichas <= 0:
        game_over()

# ====================
# EFEITO VISUAL DE VITÓRIA
# ====================
def efeito_vitoria(passo):
    cores = ["#1f4f3a", "#2ecc71", "#1f4f3a", "#2ecc71"]
    if passo < len(cores):
        label_simbolos.config(bg=cores[passo])
        janela.after(120, efeito_vitoria, passo + 1)

# ====================
# AUXILIARES
# ====================
def atualizar_fichas():
    label_fichas.config(text=f"Fichas: {fichas}")

def atualizar_vitorias():
    label_vitorias.config(text=f"Vitórias: {vitorias}")

def game_over():
    label_resultado.config(text="💀 GAME OVER 💀", fg="#ff0000")
    label_simbolos.config(text="❌   ❌   ❌", bg="#2b2b2b", fg="#ffffff")
    botao_girar.config(state="disabled")

def reiniciar():
    global fichas, vitorias, rodando
    fichas = FICHAS_INICIAIS
    vitorias = 0
    rodando = False

    label_simbolos.config(text="❓   ❓   ❓", fg="#ffffff", bg="#2b2b2b")
    label_resultado.config(text="Boa sorte!", fg="#ffffff")
    atualizar_fichas()
    atualizar_vitorias()
    botao_girar.config(state="normal")

# ====================
# JANELA
# ====================
janela = tk.Tk()
janela.title("🎰 Spin Arcade FX")
janela.geometry("460x420")
janela.resizable(False, False)
janela.configure(bg="#1e1e1e")

# ====================
# INTERFACE
# ====================
tk.Label(
    janela, text="🎰 SPIN ARCADE FX",
    font=("Arial", 20, "bold"),
    fg="#f5f5f5", bg="#1e1e1e"
).pack(pady=10)

label_fichas = tk.Label(
    janela, text=f"Fichas: {fichas}",
    font=("Arial", 12),
    fg="#f5f5f5", bg="#1e1e1e"
)
label_fichas.pack()

label_vitorias = tk.Label(
    janela, text=f"Vitórias: {vitorias}",
    font=("Arial", 12),
    fg="#00ff88", bg="#1e1e1e"
)
label_vitorias.pack()

label_simbolos = tk.Label(
    janela, text="❓   ❓   ❓",
    font=("Arial", 34),
    fg="#ffffff", bg="#2b2b2b",
    relief="ridge", bd=4, width=10
)
label_simbolos.pack(pady=25)

botao_girar = tk.Button(
    janela, text="GIRAR (-1 FICHA)",
    font=("Arial", 12, "bold"),
    bg="#ffaa00", fg="#000000",
    width=20, command=girar
)
botao_girar.pack(pady=5)

tk.Button(
    janela, text="🔄 REINICIAR",
    font=("Arial", 11, "bold"),
    bg="#444444", fg="#ffffff",
    width=20, command=reiniciar
).pack(pady=5)

label_resultado = tk.Label(
    janela, text="Boa sorte!",
    font=("Arial", 12),
    fg="#ffffff", bg="#1e1e1e"
)
label_resultado.pack(pady=10)

# ====================
# START
# ====================
janela.mainloop()
