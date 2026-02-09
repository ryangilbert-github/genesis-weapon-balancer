import streamlit as st
import pandas as pd
import time
import sys
import os
import random

# Add the parent directory to Python path so we can import 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.monster import Monster
from src.weapon import Weapon
from src.genetic_engine import fitness_score, mutate, crossover, calculate_ttk


# ==========================================
# HELPER: ARCHETYPE GENERATORS
# ==========================================
def create_archetype(archetype_name):
    """
    Returns a random weapon constrained to a specific style.
    """
    if archetype_name == "Sniper Rifle":
        return Weapon("Sniper",
                      damage=random.randint(80, 200),
                      fire_rate=random.uniform(0.5, 1.5),
                      mag=random.randint(1, 10))
    elif archetype_name == "SMG":
        return Weapon("SMG",
                      damage=random.randint(5, 25),
                      fire_rate=random.uniform(10.0, 20.0),
                      mag=random.randint(20, 50))
    else:  # Assault Rifle
        return Weapon("AR",
                      damage=random.randint(20, 50),
                      fire_rate=random.uniform(5.0, 10.0),
                      mag=random.randint(20, 40))


# ==========================================
# UI LAYOUT
# ==========================================
st.set_page_config(page_title="Genesis Weapon Balancer", layout="wide")

st.title("⚔️ Genesis Module 1: Automated Weapon Balancer")
st.markdown("### The 'Ground Truth' Generator")

# --- SIDEBAR: THE PROBLEM ---
st.sidebar.header("1. Define The Enemy")
enemy_type = st.sidebar.selectbox("Target Type", ["Trash Mob (Goblin)", "Elite (Orc)", "Raid Boss (Dragon)"])

if enemy_type == "Trash Mob (Goblin)":
    default_hp, default_ttk = 100, 1.5
elif enemy_type == "Elite (Orc)":
    default_hp, default_ttk = 1000, 8.0
else:
    default_hp, default_ttk = 50000, 60.0

# Allow manual override
enemy_hp = st.sidebar.number_input("Enemy HP", value=default_hp)
target_ttk = st.sidebar.number_input("Target TTK (Seconds)", value=default_ttk)

# --- SIDEBAR: THE SOLUTION SPACE ---
st.sidebar.header("2. Define Weapon Archetype")
weapon_type = st.sidebar.selectbox("Weapon Class", ["Assault Rifle", "Sniper Rifle", "SMG"])

st.sidebar.markdown("---")
st.sidebar.header("3. AI Settings")
generations = st.sidebar.slider("Max Generations", 10, 200, 50)
pop_size = st.sidebar.slider("Population Size", 10, 200, 100)
mutation_rate = st.sidebar.slider("Mutation Rate", 0.01, 0.5, 0.1)

run_btn = st.sidebar.button("🧬 Evolve Solution", type="primary")

# --- MAIN EXECUTION ---
if run_btn:
    # 1. Initialize Constraint
    target_monster = Monster(enemy_type, enemy_hp, target_ttk)

    # 2. Initialize Population
    population = [create_archetype(weapon_type) for _ in range(pop_size)]

    # 3. UI Containers
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"Evolution Progress ({weapon_type} vs {enemy_type})")
        chart_placeholder = st.empty()

    with col2:
        st.subheader("Current Best Candidate")
        best_card = st.empty()

    history = []
    progress_bar = st.progress(0)

    # 4. Evolution Loop
    for gen in range(generations):

        # A. Evaluate
        population.sort(key=lambda w: fitness_score(w, target_monster))
        best_weapon = population[0]
        current_error = fitness_score(best_weapon, target_monster)
        actual_ttk = calculate_ttk(best_weapon, target_monster)

        # B. Record Data for History
        history.append({
            "Generation": gen,
            "Damage": best_weapon.damage,
            "Fire Rate": round(best_weapon.fire_rate, 2),
            "Mag Size": best_weapon.mag,
            "Actual TTK": round(actual_ttk, 2),
            "Target TTK": target_ttk,
            "Error": round(current_error, 4)
        })

        # C. Update Charts LIVE
        df = pd.DataFrame(history)

        with chart_placeholder:
            # We plot Actual TTK vs Target Line
            chart_data = df.set_index("Generation")[["Actual TTK", "Target TTK"]]
            st.line_chart(chart_data, color=["#FF4B4B", "#00FF00"])  # Red = Actual, Green = Target

        with best_card:
            st.info(f"""
            **{best_weapon.name} Gen-{gen}**
            * Damage: {best_weapon.damage}
            * Fire Rate: {best_weapon.fire_rate:.2f}
            * Mag: {best_weapon.mag}
            * **TTK: {actual_ttk:.2f}s**
            """)

        # D. Convergence Check
        if current_error < 0.05:
            st.success(f"🚀 CONVERGENCE REACHED at Gen {gen}!")
            break

        # E. Reproduce
        next_gen = population[:10]  # Elites
        while len(next_gen) < pop_size:
            p1 = random.choice(population[:20])
            p2 = random.choice(population[:20])
            child = crossover(p1, p2)
            child = mutate(child, mutation_rate)
            next_gen.append(child)

        population = next_gen
        progress_bar.progress((gen + 1) / generations)
        time.sleep(0.05)  # Speed of animation

    # --- FINAL SUMMARY ---
    st.balloons()
    st.success(f"Genesis AI has successfully engineered the '{best_weapon.name} Mark IV'.")

    # 1. Show Data History
    with st.expander("📜 View Full Evolution History"):
        st.dataframe(df, use_container_width=True)

    # 2. Show JSON Output
    st.markdown("### 📤 Export to Game Engine")
    st.code(f"""
    {{
        "item_name": "{best_weapon.name}_Procedural",
        "base_damage": {best_weapon.damage},
        "fire_rate": {best_weapon.fire_rate:.2f},
        "magazine_capacity": {best_weapon.mag},
        "balance_target": "{enemy_type}"
    }}
    """, language="json")

else:
    st.info("👈 Select your Enemy and Weapon Class, then click Evolve.")
