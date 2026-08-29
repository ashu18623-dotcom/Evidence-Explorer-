import streamlit as st
import time
import random
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random
# ======================================================
# RUTHERFORD CONSTANTS
# ======================================================

k_coulomb = 8.99e9
electron_charge = 1.602e-19

alpha_Z = 2
gold_Z = 79

# ======================================================
# Basic Element Database py -3.12 -m streamlit run "E:\Python\MOOSLEY.py" 
# ======================================================

elements = {

    "H": {
        "Name": "Hydrogen",
        "Atomic Number": 1,
        "Atomic Mass": 1.008,
        "Protons": 1,
        "Electrons": 1,
        "Neutrons": 0
    },

    "He": {
        "Name": "Helium",
        "Atomic Number": 2,
        "Atomic Mass": 4.0026,
        "Protons": 2,
        "Electrons": 2,
        "Neutrons": 2
    },

    "Li": {
        "Name": "Lithium",
        "Atomic Number": 3,
        "Atomic Mass": 6.94,
        "Protons": 3,
        "Electrons": 3,
        "Neutrons": 4
    },

    "Be": {
        "Name": "Beryllium",
        "Atomic Number": 4,
        "Atomic Mass": 9.0122,
        "Protons": 4,
        "Electrons": 4,
        "Neutrons": 5
    },

    "B": {
        "Name": "Boron",
        "Atomic Number": 5,
        "Atomic Mass": 10.81,
        "Protons": 5,
        "Electrons": 5,
        "Neutrons": 6
    },

    "C": {
        "Name": "Carbon",
        "Atomic Number": 6,
        "Atomic Mass": 12.011,
        "Protons": 6,
        "Electrons": 6,
        "Neutrons": 6
    },

    "N": {
        "Name": "Nitrogen",
        "Atomic Number": 7,
        "Atomic Mass": 14.007,
        "Protons": 7,
        "Electrons": 7,
        "Neutrons": 7
    },

    "O": {
        "Name": "Oxygen",
        "Atomic Number": 8,
        "Atomic Mass": 15.999,
        "Protons": 8,
        "Electrons": 8,
        "Neutrons": 8
    },

    "F": {
        "Name": "Fluorine",
        "Atomic Number": 9,
        "Atomic Mass": 18.998,
        "Protons": 9,
        "Electrons": 9,
        "Neutrons": 10
    },

    "Ne": {
        "Name": "Neon",
        "Atomic Number": 10,
        "Atomic Mass": 20.180,
        "Protons": 10,
        "Electrons": 10,
        "Neutrons": 10
    },

    "Na": {
        "Name": "Sodium",
        "Atomic Number": 11,
        "Atomic Mass": 22.990,
        "Protons": 11,
        "Electrons": 11,
        "Neutrons": 12
    }

}


# ======================================================
# AAS ABSORPTION SPECTRAL DATABASE
# ======================================================

aas_spectra = {

    "H": [656.3, 486.1, 434.0],

    "He": [447.1, 501.6, 587.6, 667.8],

    "Li": [610.4, 670.8],

    "Be": [234.9, 313.0],

    "B": [249.7],

    "C": [193.1, 247.9],

    "N": [149.3],

    "O": [130.2],

    "F": [95.0],

    "Ne": [585.2, 640.2],

    "Na": [589.0, 589.6]
}
# ======================================================
# ATOMIC EMISSION SPECTRAL DATABASE
# ======================================================

emission_spectra = {

    "H": {
        "lines": [410.2, 434.0, 486.1, 656.3],
        "color": "violet"
    },

    "He": {
        "lines": [447.1, 501.6, 587.6, 667.8],
        "color": "orange"
    },

    "Li": {
        "lines": [610.4, 670.8],
        "color": "red"
    },

    "Be": {
        "lines": [457.3, 469.9],
        "color": "cyan"
    },

    "B": {
        "lines": [412.2, 420.1],
        "color": "green"
    },

    "C": {
        "lines": [426.7, 658.8],
        "color": "blue"
    },

    "N": {
        "lines": [500.5, 567.9],
        "color": "purple"
    },

    "O": {
        "lines": [557.7, 630.0],
        "color": "lime"
    },

    "F": {
        "lines": [685.6],
        "color": "pink"
    },

    "Ne": {
        "lines": [540.1, 585.2, 640.2],
        "color": "orange"
    },

    "Na": {
        "lines": [589.0, 589.6],
        "color": "gold"
    }

}
# ======================================================
# ======================================================
# ORBITAL INFORMATION ENGINE
# ======================================================

orbital_database = {

    "1s": (1,0,0),
    "2s": (2,0,0),

    "2px": (2,1,-1),
    "2py": (2,1,0),
    "2pz": (2,1,1),

    "3s": (3,0,0),

    "3px": (3,1,-1),
    "3py": (3,1,0),
    "3pz": (3,1,1),

    "3dxy": (3,2,-2),
    "3dyz": (3,2,-1),
    "3dz²": (3,2,0),
    "3dxz": (3,2,1),
    "3dx²-y²": (3,2,2)

}
def orbital_information(orbital):

    n, l, m = orbital_database[orbital]

    radial_nodes = n - l - 1

    angular_nodes = l

    total_nodes = n - 1

    return {
        "n": n,
        "l": l,
        "m": m,
        "radial": radial_nodes,
        "angular": angular_nodes,
        "total": total_nodes
    }

# ======================================================
# QUANTUM ORBITAL ENGINE
# ======================================================

def draw_orbital_cloud(orbital):

    fig, ax = plt.subplots(figsize=(7,7))

    ax.set_aspect("equal")
    ax.axis("off")

    # -----------------------------
    # Nucleus
    # -----------------------------

    nucleus = plt.Circle(
        (0,0),
        0.12,
        color="gold",
        ec="black"
    )

    ax.add_patch(nucleus)

    # Number of probability points

    N = 4000

    # =====================================================
    # 1s Orbital
    # =====================================================

    if orbital == "1s":

        theta = np.random.uniform(
            0,
            2*np.pi,
            N
        )

        r = np.random.exponential(
            scale=0.35,
            size=N
        )

        x = r*np.cos(theta)
        y = r*np.sin(theta)

        ax.scatter(
            x,
            y,
            s=2,
            color="royalblue",
            alpha=0.18
        )

    # =====================================================
    # 2s Orbital
    # =====================================================

    elif orbital == "2s":

        theta = np.random.uniform(
            0,
            2*np.pi,
            N
        )

        r = np.random.exponential(
            scale=0.70,
            size=N
        )

        mask = r > 0.45

        x = r[mask]*np.cos(theta[mask])
        y = r[mask]*np.sin(theta[mask])

        ax.scatter(
            x,
            y,
            s=2,
            color="green",
            alpha=0.18
        )

    # =====================================================
    # 2p Orbital
    # =====================================================

    elif orbital == "2px":

        theta = np.random.uniform(
            0,
            2*np.pi,
            N
        )

        r = np.random.normal(
            1.1,
            0.25,
            N
        )

        x = r*np.cos(theta)
        y = r*np.sin(theta)

        mask = np.abs(x) > np.abs(y)

        ax.scatter(
            x[mask],
            y[mask],
            s=2,
            color="red",
            alpha=0.18
        )
         # =====================================================
    # 2py Orbital
    # =====================================================

    elif orbital == "2py":

        theta = np.random.uniform(
            0,
            2*np.pi,
            N
        )

        r = np.random.normal(
            1.1,
            0.25,
            N
        )

        x = r*np.cos(theta)
        y = r*np.sin(theta)

        # Vertical dumbbell
        mask = np.abs(y) > np.abs(x)

        ax.scatter(
            x[mask],
            y[mask],
            s=2,
            color="purple",
            alpha=0.18
        )

    # =====================================================
    # 2pz Orbital
    # =====================================================

    elif orbital == "2pz":

        theta = np.random.uniform(
            0,
            2*np.pi,
            N
        )

        r = np.random.normal(
            1.1,
            0.25,
            N
        )

        x = r*np.cos(theta)
        y = r*np.sin(theta)

        # Circular projection (placeholder for z-axis)
        mask = np.sqrt(x**2 + y**2) > 0.7

        ax.scatter(
            x[mask],
            y[mask],
            s=2,
            color="darkorange",
            alpha=0.18
        )

        ax.text(
            0,
            2.6,
            "Projection of 2pz Orbital",
            fontsize=10,
            ha="center"
        )

    # ====================================================
    # =====================================================
        # =====================================================
    # 3s Orbital
    # =====================================================

    elif orbital == "3s":

        theta = np.random.uniform(
            0,
            2*np.pi,
            N
        )

        r = np.random.exponential(
            scale=1.1,
            size=N
        )

        mask = r > 0.35

        x = r[mask] * np.cos(theta[mask])
        y = r[mask] * np.sin(theta[mask])

        ax.scatter(
            x,
            y,
            s=2,
            color="navy",
            alpha=0.15
        )

    # =====================================================
    # 3px Orbital
    # =====================================================

    elif orbital == "3px":

        theta = np.random.uniform(
            0,
            2*np.pi,
            N
        )

        r = np.random.normal(
            1.8,
            0.35,
            N
        )

        x = r * np.cos(theta)
        y = r * np.sin(theta)

        mask = np.abs(x) > np.abs(y)

        ax.scatter(
            x[mask],
            y[mask],
            s=2,
            color="darkred",
            alpha=0.18
        )

    # =====================================================
    # 3py Orbital
    # =====================================================

    elif orbital == "3py":

        theta = np.random.uniform(
            0,
            2*np.pi,
            N
        )

        r = np.random.normal(
            1.8,
            0.35,
            N
        )

        x = r * np.cos(theta)
        y = r * np.sin(theta)

        mask = np.abs(y) > np.abs(x)

        ax.scatter(
            x[mask],
            y[mask],
            s=2,
            color="darkgreen",
            alpha=0.18
        )

    # =====================================================
    # 3pz Orbital
    # =====================================================

    elif orbital == "3pz":

     theta = np.random.uniform(0, 2*np.pi, N)

     r = np.random.normal(1.8, 0.35, N)

     x = r*np.cos(theta)
     y = r*np.sin(theta)

     mask = np.sqrt(x**2 + y**2) > 1.2

     ax.scatter(
        x[mask],
        y[mask],
        s=2,
        color="orange",
        alpha=0.18
    )

     ax.text(
        0,
        3.3,
        "Projection of 3pz",
        fontsize=10,
        ha="center"
    )

    elif orbital == "3dxy":

     N = 6000

     r = np.random.normal(2.0, 0.30, N)

     theta = np.random.uniform(0, 2*np.pi, N)

    # Four lobes between axes
     x = r * np.cos(theta) * np.sin(2 * theta)
     y = r * np.sin(theta) * np.sin(2 * theta)

     mask = np.sqrt(x**2 + y**2) > 0.5

     ax.scatter(
        x[mask],
        y[mask],
        s=2,
        color="deepskyblue",
        alpha=0.18
    )

     ax.text(
        0,
        3.5,
        "Projection of 3dxy",
        fontsize=10,
        ha="center"
    )

    elif orbital == "3dx²-y²":

     N = 7000

     theta = np.random.uniform(0, 2*np.pi, N)

     r = np.random.normal(2.0, 0.30, N)

    # Four lobes along x and y axes
     x = r * np.cos(theta) * np.cos(2 * theta)
     y = r * np.sin(theta) * np.cos(2 * theta)

     mask = np.sqrt(x**2 + y**2) > 0.5

     ax.scatter(
        x[mask],
        y[mask],
        s=2,
        color="crimson",
        alpha=0.18
    )

     ax.text(
        0,
        3.5,
        "Projection of 3d(x²−y²)",
        fontsize=10,
        ha="center"
    )
  
# Bohr ENGINE
# ======================================================
def shell_configuration(Z):
    """
    Returns shell-wise electron distribution.
    """

    capacities = [2, 8, 18, 32, 32, 18, 8]

    remaining = Z
    shells = []

    for cap in capacities:

        if remaining <= 0:
            break

        electrons = min(cap, remaining)

        shells.append(electrons)

        remaining -= electrons

    return shells
# ======================================================
# DRAW BOHR ATOM
# ======================================================

def draw_bohr_atom(Z):

    shells = shell_configuration(Z)

    fig, ax = plt.subplots(figsize=(7,7))

    ax.set_aspect("equal")

    ax.axis("off")

    # ---------------------------
    # Nucleus
    # ---------------------------

    nucleus = plt.Circle(
        (0,0),
        0.18,
        color="gold",
        ec="black"
    )

    ax.add_patch(nucleus)

    ax.text(
        0,
        0,
        str(Z),
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold"
    )
    # Shell Labels
    # ---------------------------

    shell_names = ["K","L","M","N","O","P","Q"]
    # ---------------------------
    # Shells
    # ---------------------------

    shell_gap = 0.55

    for i, electrons in enumerate(shells):

        radius = shell_gap * (i+1)

        orbit = plt.Circle(
            (0,0),
            radius,
            fill=False,
            linestyle="--",
            linewidth=1.6,
            color="gray"
        )

        ax.add_patch(orbit)

              # Label Shell
        # ---------------------------

        ax.text(
            radius,
            0.10,
            shell_names[i],
            fontsize=12,
            fontweight="bold",
            color="darkred",
            ha="center",
            va="bottom"
        )

        # ------------------------
        # Electrons
        # ------------------------

        for j in range(electrons):

            angle = 2*np.pi*j/electrons

            x = radius*np.cos(angle)

            y = radius*np.sin(angle)

            electron = plt.Circle(
                (x,y),
                0.05,
                color="royalblue",
                ec="black"
            )

            ax.add_patch(electron)

    limit = shell_gap*(len(shells)+1)

    ax.set_xlim(-limit,limit)
    ax.set_ylim(-limit,limit)

    return fig
# ======================================================
# ======================================================
# RUTHERFORD GOLD FOIL SCATTERING ENGINE
# ======================================================


# Constants

k_coulomb = 8.99e9

electron_charge = 1.602e-19

alpha_Z = 2

gold_Z = 79



# ======================================================
# GENERATE ALPHA PARTICLES
# ======================================================

def generate_alpha_trajectories(number, energy_MeV):

    trajectories = []


    energy = energy_MeV * 1.602e-13


    for i in range(number):


        # Correct impact distribution
        # area probability

        b_max = 1e-10


        b = np.sqrt(
            np.random.random()
        ) * b_max



        theta = 2 * np.arctan(

            (
                k_coulomb
                *
                alpha_Z
                *
                gold_Z
                *
                electron_charge**2
            )

            /

            (
                2
                *
                energy
                *
                b
            )

        )


        # scattering direction

        if random.random() < 0.5:

            theta = -theta



        trajectories.append({

            "theta":theta,

            "b":b

        })


    return trajectories


# ======================================================
# DRAW GOLD FOIL FRAME
# ======================================================


def draw_goldfoil_frame(
        trajectories,
        frame
):


    fig, ax = plt.subplots(
        figsize=(10,5)
    )


    ax.set_xlim(
        0,
        10
    )

    ax.set_ylim(
        -5,
        5
    )


    ax.axis("off")



    # Alpha source

    ax.scatter(

        0.5,
        0,

        s=300,

        color="red"

    )


    ax.text(

        0.5,
        -0.6,

        "☢ Source",

        ha="center"

    )



    # Gold foil

    ax.plot(

        [5,5],

        [-3,3],

        linewidth=10,

        color="gold"

    )


    ax.text(

        5,
        3.5,

        "Gold Foil",

        ha="center"

    )



    # Detector

    detector = plt.Circle(

        (9,0),

        1,

        fill=False,

        color="green",

        linewidth=2

    )


    ax.add_patch(detector)



    ax.text(

        9,
        -1.5,

        "Detector",

        ha="center"

    )




    # Draw alpha trajectories

    for particle in trajectories:


        theta = particle["theta"]



        distance = frame / 10



        x = np.linspace(

            0,

            distance,

            100

        )


        y = (

            np.tan(theta)

            *

            (x-5)

        )



        ax.plot(

            x,

            y,

            color="red",

            alpha=0.5

        )



    return fig

    # Statistics

    straight, small, large = calculate_scattering_statistics(
        particles
    )


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Straight",
        straight
    )

    col2.metric(
        "Small Deflection",
        small
    )

    col3.metric(
        "Large Deflection",
        large
    )


    # Plot

    result_plot = plot_scattering_results(
        particles
    )


    st.pyplot(
        result_plot
    )
    # ======================================================
# RUTHERFORD RESULTS PLOTS
# ======================================================

def plot_scattering_results(trajectories):

    angles = []

    for particle in trajectories:

        angle = np.degrees(
            abs(particle["theta"])
        )

        angles.append(angle)


    fig, ax = plt.subplots(
        figsize=(8,4)
    )


    ax.hist(
        angles,
        bins=30
    )


    ax.set_xlabel(
        "Scattering Angle (degrees)"
    )

    ax.set_ylabel(
        "Number of Alpha Particles"
    )


    ax.set_title(
        "Rutherford Scattering Angle Distribution"
    )


    return fig
# ======================================================
# SCATTERING STATISTICS
# ======================================================

def calculate_scattering_statistics(trajectories):

    straight = 0
    small = 0
    large = 0


    for particle in trajectories:

        angle = abs(
            np.degrees(
                particle["theta"]
            )
        )


        if angle < 5:

            straight += 1

        elif angle < 90:

            small += 1

        else:

            large += 1


    return straight, small, large
    st.divider()


# ======================================================
# STREAMLIT ANIMATION
# ======================================================


def animate_goldfoil(

        trajectories

):


    placeholder = st.empty()



    for frame in range(1,101):


        fig = draw_goldfoil_frame(

            trajectories,

            frame

        )


        placeholder.pyplot(

            fig

        )


        plt.close(fig)


        time.sleep(0.05)
# ======================================================
# THOMSON ENGINE
# ======================================================

def generate_thomson_positions(electrons):

    positions = []

    for i in range(electrons):

        r = random.uniform(0.2, 0.8)
        theta = random.uniform(0, 2 * math.pi)

        x = r * math.cos(theta)
        y = r * math.sin(theta)

        positions.append((x, y))

    return positions


def draw_thomson_atom(positions, filled):

    fig, ax = plt.subplots(figsize=(6,6))

    positive = plt.Circle(
        (0,0),
        1,
        color="gold",
        alpha=0.35
    )

    ax.add_artist(positive)

    for x, y in positions[:filled]:

        ax.scatter(
            x,
            y,
            s=120,
            color="blue",
            edgecolors="black"
        )

    ax.set_xlim(-1.2,1.2)
    ax.set_ylim(-1.2,1.2)

    ax.set_aspect("equal")

    ax.axis("off")

    return fig


# ======================================================
# AUFBAU ENGINE
# H → Na
# ======================================================

orbitals = [
    ("1s", 2),
    ("2s", 2),
    ("2p", 6),
    ("3s", 2),
    ("3p", 6)
]


# ======================================================
# AUFBAU MODULE
# ======================================================

aufbau_orbitals = [

    ("1s", 2),
    ("2s", 2),
    ("2p", 6),
    ("3s", 2),
    ("3p", 6)

]

def aufbau_electron_configuration(electrons):

    configuration = []

    remaining = electrons

    for orbital, capacity in aufbau_orbitals:

        if remaining <= 0:
            break

        filled = min(remaining, capacity)

        configuration.append((orbital, filled))

        remaining -= filled

    return configuration
# ======================================================
# ELECTRON CONFIGURATION TEXT
# ======================================================

def electron_configuration_text(configuration):

    text = ""

    superscript = {
        "0":"⁰",
        "1":"¹",
        "2":"²",
        "3":"³",
        "4":"⁴",
        "5":"⁵",
        "6":"⁶",
        "7":"⁷",
        "8":"⁸",
        "9":"⁹"
    }

    for orbital, electrons in configuration:

        exp = ""

        for digit in str(electrons):
            exp += superscript[digit]

        text += orbital + exp + " "

    return text.strip()
# ======================================================
# HUND MODULE
# ======================================================

def hund_filling(number_of_boxes, electrons):

    boxes = [""] * number_of_boxes

    # First pass (↑)

    i = 0

    while electrons > 0 and i < number_of_boxes:

        boxes[i] = "↑"

        electrons -= 1

        i += 1

    # Second pass (↓)

    i = 0

    while electrons > 0 and i < number_of_boxes:

        boxes[i] += "↓"

        electrons -= 1

        i += 1

    return boxes

# ======================================================
# ORBITAL DIAGRAM MODULE
# ======================================================

orbital_boxes = {
    "1s": 1,
    "2s": 1,
    "2p": 3,
    "3s": 1,
    "3p": 3
}

def draw_orbitals(configuration):

    for orbital, electrons in configuration:

        st.write(f"### {orbital}")

        # Number of boxes
        n_boxes = orbital_boxes[orbital]

        # Hund filling
        boxes = [""] * n_boxes

        remaining = electrons

        # ---------- First Pass ----------
        # Put one ↑ in each box

        for i in range(n_boxes):

            if remaining > 0:
                boxes[i] = "↑"
                remaining -= 1

        # ---------- Second Pass ----------
        # Now start pairing

        for i in range(n_boxes):

            if remaining > 0:
                boxes[i] += "↓"
                remaining -= 1

        cols = st.columns(n_boxes)

        for i in range(n_boxes):

            if boxes[i] == "":
                cols[i].info("")

            elif boxes[i] == "↑":
                cols[i].warning("↑")

            else:
                cols[i].success(boxes[i])
# ======================================================
# PAGE SETTINGS
# ======================================================

import streamlit as st

st.set_page_config(
    page_title="Evidence Explorer",
    page_icon="⚛️",
    layout="wide"
)

# ======================================================
# CUSTOM CSS
# ======================================================

st.markdown("""
<style>

.stApp{
    background-color:#0f172a;
}



.hero{
    background:linear-gradient(90deg,#0f172a,#1e3a8a,#2563eb);
    padding:30px;
    border-radius:20px;
    margin-bottom:25px;
    box-shadow:0px 5px 20px rgba(0,0,0,.4);
}

.title{
    font-size:50px;
    font-weight:bold;
    text-align:center;
    color:#00d4ff;
}

.subtitle{
    font-size:22px;
    text-align:center;
    color:white;
}

button[data-baseweb="tab"]{
    font-size:17px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)
# ======================================================
#  LOGO 
# ======================================================

#col1, col2, col3 = st.columns([1,2,1])

#with col2:

 #   st.image(
  #      r"E:\Python\file_00000000a00c720b84fbafc34f0ed732 (1) (1).png",
   #     width=100
    #)


# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:

    st.title("⚛ Evidence Explorer")

    st.write("### Select Element")

    selected = st.selectbox(
        "",
        list(elements.keys())
    )

    st.divider()

    st.success("Version 2.0")

    st.info("Elements Available\n\nH → Na")

element = elements[selected]

# ======================================================
# HERO BANNER
# ======================================================

st.markdown("""

<div class="hero">

<div class="title">

⚛ HOW DO WE KNOW?

</div>

<div class="subtitle">

Scientific Evidence Explorer

</div>

</div>

""", unsafe_allow_html=True)

# ======================================================
# ELEMENT TITLE
# ======================================================

st.header(f"⚛ {element['Name']} ({selected})")

# ======================================================
# INFORMATION CARDS
# ======================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Atomic Number",
        element["Atomic Number"]
    )

with c2:
    st.metric(
        "Atomic Mass",
        element["Atomic Mass"]
    )

with c3:
    st.metric(
        "Electrons",
        element["Electrons"]
    )

with c4:
    st.metric(
        "Neutrons",
        element["Neutrons"]
    )

st.divider()

# ======================================================
# TABS
# ======================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📘 Basic Information",
    "⚛ Electronic Structure",
    "🪐 Atomic Models",
    "📈 Spectroscopy",
    "📡 Moseley's Law",
    "📚 History",
    "❓ How Do We Know?"
])

# ======================================================
# TAB 1
# ======================================================

with tab1:

    st.subheader("Basic Information")

    for key, value in element.items():
        st.write(f"**{key}:** {value}")

# ======================================================
# TAB 2
# ======================================================

with tab2:

    st.header("⚛ Electronic Structure")

    electrons = element["Electrons"]

    st.metric("Total Electrons", electrons)

    st.divider()

    # ------------------------------------------
    # Electron Configuration
    # ------------------------------------------

    config = aufbau_electron_configuration(electrons)

    st.subheader("Electron Configuration")

    st.code(
        electron_configuration_text(config),
        language=None
    )

    # ------------------------------------------
    # Orbital Diagram
    # ------------------------------------------

    st.subheader("Orbital Diagram")

    draw_orbitals(config)

    st.divider()

    # ------------------------------------------
    # Live Aufbau Simulation
    # ------------------------------------------

    st.subheader("Live Aufbau Filling")

    if st.button("▶ Start Simulation", key="aufbau_button"):

        placeholder = st.empty()

        for e in range(1, electrons + 1):

            config = aufbau_electron_configuration(e)

            with placeholder.container():

                st.metric("Electrons Filled", e)

                draw_orbitals(config)

            time.sleep(0.6)

        st.success("Aufbau Filling Completed!")
# ======================================================
# ======================================================
# TAB 3 : ATOMIC MODELS
# ======================================================

with tab3:

    st.header("⚛ Atomic Models")

    st.write("""
    Explore the historical development of atomic theory and understand
    how our picture of the atom evolved through experimental evidence.
    """)

    st.divider()

    # =====================================================
    # DALTON MODEL
    # =====================================================

    with st.expander("⚪ Dalton's Atomic Theory (1803)", expanded=True):

        st.subheader("John Dalton (1766–1844)")

        st.markdown("""
### 📖 Historical Background

At the beginning of the nineteenth century, scientists had no direct
knowledge of atoms. Matter was understood through experiments on
chemical reactions rather than microscopic observations.

John Dalton proposed the first modern scientific atomic theory to
explain why substances always combine in fixed proportions during
chemical reactions.
""")

        st.divider()

        st.subheader("⚛ Dalton's Postulates")

        st.markdown("""
1. All matter consists of tiny indivisible particles called atoms.

2. All atoms of a given element are identical in mass and properties.

3. Atoms of different elements differ in mass and properties.

4. Atoms cannot be created or destroyed during ordinary chemical reactions.

5. Compounds are formed when atoms combine in simple whole-number ratios.

6. Chemical reactions involve only the rearrangement of atoms.
""")

        st.divider()

        st.subheader("🧪 Experimental Evidence")

        st.markdown("""
• Law of Conservation of Mass (Lavoisier)

• Law of Definite Proportions (Proust)

• Law of Multiple Proportions (Dalton)
""")

        st.divider()

        st.subheader("✅ Achievements")

        st.success("""
✔ First modern scientific atomic theory

✔ Explained chemical reactions

✔ Explained compounds

✔ Introduced relative atomic masses
""")

        st.divider()

        st.subheader("❌ Limitations")

        st.error("""
✘ Atoms are divisible

✘ No electrons

✘ No nucleus

✘ Could not explain isotopes
""")

        st.divider()

        st.info("""
Discovery of the electron by J. J. Thomson (1897)
led to the next atomic model.
""")

    # =====================================================
    # # =====================================================
# THOMSON MODEL
# =====================================================

with st.expander("🍮 Thomson Model (1897)"):

    st.subheader("J. J. Thomson (1856–1940)")

    st.markdown("""
### 📖 Historical Background

J. J. Thomson discovered the electron using cathode ray experiments.

This proved that atoms are divisible.

He proposed the Plum Pudding Model.
""")

    st.divider()

    st.subheader("🍮 Plum Pudding Model")

    st.markdown("""
• Atom is a positively charged sphere.

• Electrons are embedded inside.

• Positive and negative charges balance each other.

• Therefore, the atom is electrically neutral.
""")

    st.divider()

    st.subheader("⚛ Thomson Atom")

    st.info(
        f"Selected Element : {element['Name']} ({selected})\n\n"
        f"Electrons : {element['Electrons']}"
    )

    st.divider()

    # ======================================================
    # LIVE THOMSON SIMULATION
    # ======================================================

    st.subheader("🍮 Live Thomson Simulation")

    if st.button("⚛ Build Thomson Atom"):

        placeholder = st.empty()

        positions = generate_thomson_positions(
            element["Electrons"]
        )

        for i in range(1, element["Electrons"] + 1):

            fig = draw_thomson_atom(positions, i)

            placeholder.pyplot(fig)

            time.sleep(0.5)

        st.success(
            f"{element['Name']} Thomson Atom Successfully Constructed!"
        )

        st.caption(
            f"Thomson Model of {element['Name']} ({selected}) "
            f"containing {element['Electrons']} electrons."
        )

    st.divider()

    st.subheader("🧪 Experimental Evidence")

    st.markdown("""
Cathode Ray Experiment

• Cathode rays carry negative charge.

• These particles were named electrons.

• Every atom contains electrons.
""")

    st.divider()

    st.subheader("✅ Achievements")

    st.success("""
✔ Discovery of the electron

✔ First atomic model containing subatomic particles

✔ Explained electrical neutrality
""")

    st.divider()

    st.subheader("❌ Limitations")

    st.error("""
✘ No nucleus

✘ Could not explain Rutherford's Gold Foil Experiment

✘ Could not explain atomic spectra

✘ Positive charge distribution was incorrect
""")

    st.divider()

    st.subheader("➡ Transition to Rutherford Model")

    st.info("""
In 1911, Ernest Rutherford performed the Gold Foil Experiment.

The observation that some alpha particles were deflected at large angles
proved that positive charge is concentrated in a tiny nucleus.

This replaced Thomson's Plum Pudding Model.
""")

    # =====================================================
   
    # =====================================================
# RUTHERFORD MODEL
# =====================================================

with st.expander("🏹 Rutherford Nuclear Model (1911)"):

    st.subheader("Ernest Rutherford (1871–1937)")

    st.markdown("""
### 📖 Historical Background

In 1909, Hans Geiger and Ernest Marsden, under the supervision of
Ernest Rutherford, performed the famous Gold Foil Experiment.

The unexpected scattering of alpha particles demonstrated that the
positive charge of an atom is concentrated in a very small central
region called the nucleus.

In 1911, Rutherford proposed the Nuclear Model of the atom.
""")

    st.divider()

    st.subheader("🏹 Rutherford's Atomic Model")

    st.markdown("""
According to Rutherford:

• Almost all the mass of the atom is concentrated in the nucleus.

• The nucleus carries the positive charge.

• Electrons move around the nucleus.

• Most of the atom is empty space.
""")

    st.divider()

    st.subheader("⚛ Selected Element")

    st.info(f"""
Element : {element['Name']} ({selected})

Atomic Number : {element['Atomic Number']}

Electrons : {element['Electrons']}
""")

    st.divider()

    # =====================================================
    # GOLD FOIL EXPERIMENT
    # =====================================================

    st.subheader("🧪 Gold Foil Experiment")

    st.markdown("""
This virtual laboratory recreates Rutherford's famous Gold Foil
Experiment performed between 1909–1911.

You can modify the experimental conditions and observe how alpha
particles interact with an ultra-thin gold foil.
""")

    st.divider()

    # =====================================================
    # LABORATORY SETUP
    # =====================================================

    st.subheader("🏛 Laboratory Setup")

    st.info("""
☢ Alpha Source

↓

Ultra Thin Gold Foil

↓

Zinc Sulphide Detector Screen

↓

Scattering Observation
""")

    st.divider()

    # =====================================================
    # GOLD FOIL PROPERTIES
    # =====================================================

    st.subheader("🥇 Gold Foil Properties")

    left, right = st.columns(2)

    with left:

        st.metric("Element", "Gold (Au)")
        st.metric("Atomic Number", 79)
        st.metric("Atomic Mass", "196.97 u")
        st.metric("Density", "19.32 g/cm³")

    with right:

        st.metric("Crystal", "FCC")
        st.metric("Nuclear Charge", "+79e")
        st.metric("Foil Purity", "99.99 %")
        st.metric("Typical Thickness", "10–100 nm")

    st.divider()

    # =====================================================
    # ALPHA PARTICLE SOURCE
    # =====================================================

    st.subheader("☢ Alpha Particle Source")

    left, right = st.columns(2)

    with left:

        st.metric("Particle", "⁴He²⁺")
        st.metric("Charge", "+2e")
        st.metric("Mass", "4.0015 u")

    with right:

        st.metric("Energy", "5.30 MeV")
        st.metric("Velocity", "1.6×10⁷ m/s")
        st.metric("Source", "Polonium-210")

    st.divider()

    # =====================================================
    # EXPERIMENT CONTROLS
    # =====================================================

    st.subheader("⚙ Experiment Controls")

    col1, col2 = st.columns(2)

    with col1:

        foil_thickness = st.selectbox(
            "Gold Foil Thickness (nm)",
            [10, 20, 50, 100],
            key="foil"
        )

        alpha_particles = st.selectbox(
            "Number of Alpha Particles",
            [100, 500, 1000],
            key="alpha"
        )

    with col2:

        alpha_energy = st.selectbox(
            "Alpha Particle Energy (MeV)",
            [5.30],
            key="energy"
        )

        detector_radius = st.slider(
            "Detector Radius",
            5,
            20,
            10,
            key="radius"
        )

    st.divider()

    start_experiment = st.button(
        "▶ Start Gold Foil Experiment",
        use_container_width=True,
        key="goldfoil"
    )
if start_experiment:

    particles = generate_alpha_trajectories(
        alpha_particles,
        alpha_energy
    )


    animate_goldfoil(
        particles
    )


    st.success(
        "Experiment Completed!"
    )


    # Statistics

    straight, small, large = calculate_scattering_statistics(
        particles
    )


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Straight",
        straight
    )

    col2.metric(
        "Small Deflection",
        small
    )

    col3.metric(
        "Large Deflection",
        large
    )


    # Plot

    result_plot = plot_scattering_results(
        particles
    )


    st.pyplot(
        result_plot
    )
    # ======================================================
# RUTHERFORD RESULTS PLOTS
# ======================================================

def plot_scattering_results(trajectories):

    angles = []

    for particle in trajectories:

        angle = np.degrees(
            abs(particle["theta"])
        )

        angles.append(angle)


    fig, ax = plt.subplots(
        figsize=(8,4)
    )


    ax.hist(
        angles,
        bins=30
    )


    ax.set_xlabel(
        "Scattering Angle (degrees)"
    )

    ax.set_ylabel(
        "Number of Alpha Particles"
    )


    ax.set_title(
        "Rutherford Scattering Angle Distribution"
    )


    return fig
# ======================================================
# SCATTERING STATISTICS
# ======================================================

def calculate_scattering_statistics(trajectories):

    straight = 0
    small = 0
    large = 0


    for particle in trajectories:

        angle = abs(
            np.degrees(
                particle["theta"]
            )
        )


        if angle < 5:

            straight += 1

        elif angle < 90:

            small += 1

        else:

            large += 1


    return straight, small, large
    st.divider()

    # =====================================================
    # OBSERVATIONS
    # =====================================================

    st.subheader("🧪 Experimental Observations")

    st.markdown("""
• Most alpha particles passed straight through.

• Some particles were deflected through small angles.

• A very small number were reflected backwards.
""")

    st.divider()

    st.subheader("🔬 Rutherford's Conclusions")

    st.success("""
✔ Atom is mostly empty space.

✔ Positive charge is concentrated in a tiny nucleus.

✔ Almost all atomic mass lies inside the nucleus.
""")

    st.divider()

    st.subheader("❌ Limitations")

    st.error("""
✘ Could not explain atomic stability.

✘ Orbiting electrons should continuously lose energy.

✘ Classical theory predicts electrons would spiral into the nucleus.

✘ Could not explain atomic spectra.
""")

    st.divider()

    st.subheader("➡ Transition to Bohr Model")

    st.info("""
In 1913, Niels Bohr proposed quantized electron orbits,
explaining atomic stability and the hydrogen spectrum.
""")
    st.subheader("🔬 Rutherford's Conclusions")

    st.success("""
✔ Atom is mostly empty space.

✔ Positive charge is concentrated in a tiny nucleus.

✔ Almost all atomic mass lies inside the nucleus.
""")

    st.divider()

    st.subheader("❌ Limitations")

    st.error("""
✘ Could not explain atomic stability.

✘ According to classical electrodynamics,
orbiting electrons continuously radiate energy.

✘ Classical physics predicts that electrons
would eventually spiral into the nucleus.

✘ Could not explain atomic spectra.
""")

    st.divider()

    st.subheader("➡ Transition to Bohr Model")

    st.info("""
In 1913, Niels Bohr proposed quantized
electron orbits to explain atomic stability
and the hydrogen spectrum.
""")
    # =====================================================
    # BOHR MODEL
    # =====================================================

    # =====================================================
# =====================================================
# BOHR MODEL
# =====================================================

with st.expander("🪐 Bohr Model (1913)"):

    st.subheader("Niels Bohr (1885–1962)")

    st.markdown("""
### 📖 Historical Background

In 1913, Niels Bohr proposed a revolutionary model of the atom by
combining Rutherford's nuclear atom with Max Planck's quantum theory.

Bohr suggested that electrons can move only in certain allowed circular
orbits around the nucleus without losing energy.

This successfully explained the stability of atoms and the hydrogen
emission spectrum.
""")

    st.divider()

    st.subheader("🪐 Bohr's Postulates")

    st.markdown("""
• Electrons revolve around the nucleus in fixed circular orbits.

• Maximum allowed electrons in the K, L, M and N shells are determined by 2n², where n = 1, 2, 3 and 4 respectively.

• Only certain discrete energy levels are allowed.

• Electrons do not radiate energy while moving in an allowed orbit.

• Electrons absorb energy to move to higher energy levels.

• Electrons emit photons when returning to lower energy levels.
""")

    st.divider()

    st.subheader("⚛ Selected Element")

    st.info(
        f"""
Element : {element['Name']} ({selected})

Atomic Number : {element['Atomic Number']}

Electrons : {element['Electrons']}
"""
    )

    st.divider()

    # =====================================================
    # LIVE BOHR MODEL
    # =====================================================

    st.subheader("🪐 Live Bohr Model")

    if st.button(
        "⚛ Build Bohr Atom",
        key="bohr_build"
    ):

        fig = draw_bohr_atom(
            element["Atomic Number"]
        )
        

        st.pyplot(fig)

        st.success(
            f"{element['Name']} Bohr Atom Successfully Built!"
        )

    st.divider()

    st.subheader("🧪 Experimental Evidence")

    st.markdown("""
The Bohr model successfully explained:

• Hydrogen emission spectrum

• Quantized atomic energy levels

• Rydberg formula for hydrogen

• Stability of the hydrogen atom
""")

    st.divider()

    st.subheader("✅ Achievements")

    st.success("""
✔ First successful quantum model

✔ Explained hydrogen spectrum

✔ Introduced quantized energy levels

✔ Explained atomic stability
""")

    st.divider()

    st.subheader("❌ Limitations")

    st.error("""
✘ Works accurately only for hydrogen-like atoms.

✘ Cannot explain multi-electron atoms.

✘ Cannot explain fine structure.

✘ Replaced later by Quantum Mechanics.
""")

    st.divider()

    st.subheader("➡ Transition to Quantum Mechanical Model")

    st.info("""
In 1926, Erwin Schrödinger replaced fixed electron orbits with
probability distributions called atomic orbitals.

This became the modern Quantum Mechanical Model.
""")

# =====================================================
# QUANTUM MECHANICAL MODEL
# =====================================================

with st.expander("🌊 Quantum Mechanical Model (1926)"):

    st.subheader("Erwin Schrödinger (1887–1961)")

    st.markdown("""
### 📖 Historical Background

The Bohr model successfully explained the hydrogen atom but failed
to describe multi-electron atoms and many experimentally observed
spectroscopic phenomena.

In 1926, Erwin Schrödinger developed Wave Mechanics, describing
electrons by a wavefunction rather than fixed circular orbits.

This became the foundation of Modern Quantum Mechanics.
""")

    st.divider()

    st.subheader("🌊 Fundamental Concepts")

    st.markdown("""
• Electrons exhibit wave-particle duality.

• Electrons do not travel in fixed circular orbits.

• Their position is described by a probability distribution.

• Regions of high probability are called atomic orbitals.

• The probability density is given by |ψ|².
""")

    st.divider()

    st.subheader("⚛ Selected Element")

    configuration = aufbau_electron_configuration(
        element["Electrons"]
    )

    config_text = " ".join(
        f"{orbital}{filled}"
        for orbital, filled in configuration
    )

    st.info(
        f"""
Element : {element['Name']} ({selected})

Atomic Number : {element['Atomic Number']}

Electrons : {element['Electrons']}

Electronic Configuration :

{config_text}
"""
    )

    st.subheader("☁️ Atomic Orbitals")

    orbital = st.selectbox(
        "Select Orbital",
        [
            "1s",
            "2s",
            "2px",
            "2py",
            "2pz",

            "3s",
            "3px",
            "3py",
            "3pz",
            "3dxy",
            "3dyz",
            "3dxz",
            "3dx²-y²",
            "3dz²",

           
        ]
    )

    if st.button(
        "☁️ Build Orbital",
        key="orbital"
    ):

        fig = draw_orbital_cloud(orbital)

        st.pyplot(fig)

        info = orbital_information(orbital)

        info = orbital_information(
            orbital
        )

        st.info(f"""
Orbital : {orbital}

Principal Quantum Number (n) : {info['n']}

Azimuthal Quantum Number (l) : {info['l']}

Magnetic Quantum Number (mₗ) : {info['m']}

Spin Quantum Number (mₛ) : ±1/2

Maximum Electrons : 2

Radial Nodes : {info['radial']}

Angular Nodes : {info['angular']}

Total Nodes : {info['total']}
""")
# TAB 4
# ======================================================

with tab4:

    st.header("📈 Spectroscopy")

    st.markdown("""
Spectroscopy is one of the most powerful experimental techniques used to identify
elements. Every element possesses a unique spectral fingerprint because its
electrons can occupy only specific energy levels.

When electrons move between these energy levels, they absorb or emit photons
of characteristic wavelengths. By analysing these wavelengths, scientists can
identify the element present in a sample.
""")

    st.divider()

    spectroscopy = st.selectbox(
    "Select Spectroscopic Technique",
    [
        "Atomic Emission Spectroscopy (AES)",
        "Atomic Absorption Spectroscopy (AAS)",
        "X-ray Fluorescence (XRF)",
        "Energy Dispersive X-ray Spectroscopy (EDS)",
        "X-ray Photoelectron Spectroscopy (XPS)"
    ]
)

st.divider()

if spectroscopy == "Atomic Emission Spectroscopy (AES)":

    st.header("🔬 Atomic Emission Spectroscopy Laboratory")

    st.write("""
Atomic Emission Spectroscopy identifies elements by analysing the light
emitted when excited electrons return to lower energy levels.

Every element produces a unique emission spectrum which acts as its
optical fingerprint.
""")

    st.divider()

    st.subheader("🧪 Selected Sample")

    st.success(f"{element['Name']} ({selected})")

    st.divider()

    st.subheader("Experimental Setup")

    st.code("""
⚡ Excitation Source
        │
        ▼
🧪 Atomic Sample
        │
        ▼
🔍 Spectrometer
        │
        ▼
💻 Detector
        │
        ▼
📈 Emission Spectrum
""")

    st.divider()

    if st.button("▶ Start Atomic Emission Experiment"):

        status = st.empty()

        messages = [
            "Loading sample...",
            "Applying excitation energy...",
            "Electrons are being excited...",
            "Electron transitions occurring...",
            "Photons emitted...",
            "Collecting emitted light...",
            "Spectrometer analysing wavelengths...",
            "Building emission spectrum..."
        ]

        for message in messages:

            status.info(message)

            time.sleep(0.8)

        status.success("Experiment Completed Successfully!")

        st.divider()

        st.subheader("📈 Live Emission Spectrum")

        fig, ax = plt.subplots(figsize=(12, 2))

        ax.set_xlim(380, 750)
        ax.set_ylim(0, 1)
        ax.set_xlabel("Wavelength (nm)")
        ax.set_yticks([])

        placeholder = st.empty()

        spectrum = emission_spectra[selected]

        for wavelength in spectrum["lines"]:

            ax.vlines(
                wavelength,
                0,
                1,
                color=spectrum["color"],
                linewidth=3
            )

            placeholder.pyplot(fig)

            time.sleep(0.8)

        st.divider()

        st.subheader("Observed Spectral Lines")

        for wavelength in spectrum["lines"]:

            st.write(f"• {wavelength:.1f} nm")

        st.divider()

        st.subheader("Scientific Interpretation")

        st.success(
            f"""
The observed emission wavelengths match the
reference Atomic Emission Spectrum of
{element['Name']} ({selected}).

Conclusion:

The analysed sample is identified as
{element['Name']} because its characteristic
emission spectrum agrees with the
reference database.
"""
        )
        

elif spectroscopy == "Atomic Absorption Spectroscopy (AAS)":

    st.header("🔬 Atomic Absorption Spectroscopy Laboratory")

    st.write("""
Atomic Absorption Spectroscopy (AAS) identifies elements by measuring
the absorption of characteristic wavelengths of radiation by
ground-state atoms.

The absorbed wavelengths appear as dark lines within a continuous
spectrum.
""")

    st.divider()

    # ==================================================
    # SELECTED SAMPLE
    # ==================================================

    st.subheader("🧪 Selected Sample")

    st.success(
        f"{element['Name']} ({selected}) sample loaded"
    )

    st.divider()

    # ==================================================
    # EXPERIMENTAL SETUP
    # ==================================================

    st.subheader("🔬 Experimental Setup")

    st.code("""
💡 Hollow Cathode Lamp
        │
        ▼
🔥 Atomizer / Flame
        │
        ▼
🧪 Ground-State Atoms
        │
        ▼
🔍 Monochromator
        │
        ▼
📡 Detector
        │
        ▼
🌈⚫ Absorption Spectrum
""")

    st.divider()

    # ==================================================
    # START EXPERIMENT
    # ==================================================

    if st.button("▶ Start AAS Experiment"):

        status = st.empty()

        messages = [

            "Preparing hollow cathode lamp...",

            "Loading selected element...",

            "Atomizing the sample...",

            "Producing ground-state atoms...",

            "Radiation passing through the atomic vapour...",

            "Atoms absorbing characteristic wavelengths...",

            "Detector measuring transmitted intensity...",

            "Building absorption spectrum..."

        ]

        for message in messages:

            status.info(message)

            time.sleep(0.7)

        status.success(
            "AAS Experiment Completed Successfully!"
        )

        st.divider()

        # ==================================================
        # LIVE ABSORPTION SPECTRUM
        # ==================================================

        st.subheader("📉 Live AAS Absorption Spectrum")

        # Visible wavelength range
        wavelengths = np.linspace(380, 750, 1200)

        # Create continuous spectrum
        spectrum = np.ones_like(wavelengths)

        # Create figure
        fig, ax = plt.subplots(figsize=(12, 3))

        # --------------------------------------------------
        # Continuous coloured spectrum
        # --------------------------------------------------

        for i in range(len(wavelengths) - 1):

            ax.axvspan(
                wavelengths[i],
                wavelengths[i + 1],
                color=plt.cm.hsv(
                    (wavelengths[i] - 380) / (750 - 380)
                ),
                linewidth=0
            )

        # --------------------------------------------------
        # Axis
        # --------------------------------------------------

        ax.set_xlim(380, 750)

        ax.set_ylim(0, 1)

        ax.set_xlabel("Wavelength (nm)")

        ax.set_ylabel("Transmitted Light")

        ax.set_yticks([])

        # --------------------------------------------------
        # Black absorption lines
        # --------------------------------------------------

        absorption_lines = aas_spectra.get(
            selected,
            []
        )

        visible_lines = [
            line
            for line in absorption_lines
            if 380 <= line <= 750
        ]

        placeholder = st.empty()

        # Draw spectrum first
        placeholder.pyplot(fig)

        time.sleep(0.8)

        # --------------------------------------------------
        # Add absorption lines one by one
        # --------------------------------------------------

        for wavelength in visible_lines:

            ax.axvline(
                wavelength,
                color="black",
                linewidth=3
            )

            placeholder.pyplot(fig)

            time.sleep(0.8)

        st.divider()

        # ==================================================
        # OBSERVED LINES
        # ==================================================

        st.subheader("⚫ Observed Absorption Lines")

        if visible_lines:

            for wavelength in visible_lines:

                st.write(
                    f"• {wavelength:.1f} nm"
                )

        else:

            st.info(
                "The characteristic lines for this element "
                "are outside the visible range shown here."
            )

        st.divider()

        # ==================================================
        # SCIENTIFIC INTERPRETATION
        # ==================================================

        st.subheader("🔬 Scientific Interpretation")

        if visible_lines:

            st.success(
                f"""
The absorption spectrum of {element['Name']} ({selected})
contains characteristic absorption lines at:

{", ".join(f"{x:.1f} nm" for x in visible_lines)}

These wavelengths correspond to transitions involving
the electronic structure of the selected element.

The characteristic absorption pattern provides an
element-specific analytical fingerprint.
"""
            )

        else:

            st.info(
                f"""
The selected element is {element['Name']} ({selected}).

Its characteristic absorption wavelengths included
in the current database lie outside the visible
380–750 nm display range.

A future UV/extended-range detector module can
display these lines.
"""
            )

        # AAS spectrum will be added here

    elif spectroscopy == "X-ray Fluorescence (XRF)":

        st.subheader("X-ray Fluorescence")

        st.info("Characteristic X-ray spectrum coming soon.")

    elif spectroscopy == "Energy Dispersive X-ray Spectroscopy (EDS)":

        st.subheader("Energy Dispersive X-ray Spectroscopy")

        st.info("Elemental composition analysis coming soon.")

    elif spectroscopy == "X-ray Photoelectron Spectroscopy (XPS)":

        st.subheader("X-ray Photoelectron Spectroscopy")

        st.info("Binding energy spectrum coming soon.")
# ======================================================
# TAB 5
# ======================================================

with tab5:

    st.subheader("Moseley's Law")

    st.info("Interactive Moseley graph coming soon.")

# ======================================================
# TAB 6
# ======================================================

with tab6:

    st.subheader("History")

    st.info("Discovery timeline and historical development.")

# ======================================================
# TAB 7
# ======================================================

with tab7:

    st.subheader("How Do We Know?")

    st.write("""
This module will explain how scientists identify elements using:

- Atomic spectroscopy
- Moseley's Law
- Mass spectrometry
- Chemical analysis
- Nuclear experiments
- Historical discoveries

The goal is not only to tell **what we know**, but also **how we know it**.
""")

st.divider()

st.caption("Evidence Explorer • Version 2.0 • Educational Prototype")
