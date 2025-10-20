import tkinter as tk
import random

# Define the Pokemon class
class Pokemon:
    def __init__(self, name, p_type, hp, attack, defense, moves):
        self.name = name
        self.type = p_type
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.moves = moves

    def __str__(self):
        return f"{self.name} ({self.type})"

# Type effectiveness dictionary (simplified)
type_chart = {
    ("Fire", "Grass"): 2.0,
    ("Fire", "Water"): 0.5,
    ("Water", "Fire"): 2.0,
    ("Water", "Electric"): 0.5,
    ("Electric", "Water"): 2.0,
    ("Electric", "Grass"): 0.5,
    ("Grass", "Water"): 2.0,
    ("Grass", "Fire"): 0.5,
}

# List of Pokemon choices
pokemon_list = [
    Pokemon("Charmander", "Fire", 39, 52, 43, ["Ember", "Scratch"]),
    Pokemon("Squirtle", "Water", 44, 48, 65, ["Tackle", "Water Gun"]),
    Pokemon("Bulbasaur", "Grass", 45, 49, 49, ["Vine Whip", "Tackle"]),
    Pokemon("Pikachu", "Electric", 35, 55, 40, ["Thunder Shock", "Quick Attack"]),
    Pokemon("Eevee", "Normal", 55, 55, 50, ["Tackle", "Bite"])
]

# Function to calculate damage
def calculate_damage(attacker, defender):
    base_damage = (attacker.attack / defender.defense) * 10
    multiplier = type_chart.get((attacker.type, defender.type), 1.0)
    return max(1, int(base_damage * multiplier))

# Battle logic to run on move selection
def battle(player_move):
    global player_pokemon, opponent_pokemon

    damage = calculate_damage(player_pokemon, opponent_pokemon)
    opponent_pokemon.hp -= damage
    text.insert(tk.END, f"{player_pokemon.name} used {player_move}! It dealt {damage} damage!\n")
    update_status()

    if opponent_pokemon.hp <= 0:
        text.insert(tk.END, f"{opponent_pokemon.name} fainted! {player_pokemon.name} wins!\n")
        disable_moves()
        return

    damage = calculate_damage(opponent_pokemon, player_pokemon)
    player_pokemon.hp -= damage
    text.insert(tk.END, f"{opponent_pokemon.name} attacks back! It dealt {damage} damage!\n")
    update_status()

    if player_pokemon.hp <= 0:
        text.insert(tk.END, f"{player_pokemon.name} fainted! {opponent_pokemon.name} wins!\n")
        disable_moves()

# Update HP display
def update_status():
    hp_label.config(text=f"Your {player_pokemon.name}: {max(0, player_pokemon.hp)} HP | Opponent {opponent_pokemon.name}: {max(0, opponent_pokemon.hp)} HP")

# Disable move buttons after win/loss
def disable_moves():
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button) and widget != restart_btn and widget not in pokemon_buttons:
            widget.config(state="disabled")


# Restart Battle
def restart_battle():
    global player_pokemon, opponent_pokemon, pokemon_buttons
    # Reset all Pokémon HP
    for pkmn in pokemon_list:
        pkmn.hp = pkmn.max_hp
    player_pokemon = None
    opponent_pokemon = None
    text.delete(1.0, tk.END)
    hp_label.config(text="")
    # Remove move buttons, but keep restart_btn and pokemon_buttons
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button) and widget != restart_btn and widget not in pokemon_buttons:
            widget.destroy()
    choose_pokemon()


# Let the user choose their Pokemon
def choose_pokemon():
    text.delete(1.0, tk.END)
    text.insert(tk.END, "Choose your Pokémon:\n")
    for i, pkmn in enumerate(pokemon_list):
        btn = tk.Button(root, text=pkmn.name, command=lambda p=pkmn: start_battle(p))
        btn.grid(row=2, column=i)
        pokemon_buttons.append(btn)

def start_battle(pokemon):
    global player_pokemon, opponent_pokemon, pokemon_buttons
    for btn in pokemon_buttons:
        btn.destroy()
    pokemon_buttons = []

    player_pokemon = pokemon
    opponent_pokemon = random.choice([p for p in pokemon_list if p != player_pokemon])

    text.delete(1.0, tk.END)
    text.insert(tk.END, f"Battle start! {player_pokemon.name} vs {opponent_pokemon.name}!\n\n")
    update_status()

    for i, move in enumerate(player_pokemon.moves):
        btn = tk.Button(root, text=move, command=lambda m=move: battle(m))
        btn.grid(row=3, column=i)

# GUI window setup
root = tk.Tk()
root.title("Mini Pokémon Battle")
root.geometry("600x400")

text = tk.Text(root, height=10, width=70)
text.grid(row=0, column=0, columnspan=5)

hp_label = tk.Label(root, text="")
hp_label.grid(row=1, column=0, columnspan=5)

pokemon_buttons = []
player_pokemon, opponent_pokemon = None, None

choose_pokemon()

restart_btn = tk.Button(root, text="Restart Battle", command=restart_battle)
restart_btn.grid(row=4, column=2)

root.mainloop()