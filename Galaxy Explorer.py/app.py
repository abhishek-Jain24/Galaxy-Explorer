import io
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

#Page Configure
st.set_page_config(
    page_title="Galaxy Generator",
    page_icon="🌌",
    layout="wide",
)

st.title("🌌 Galaxy Generator")
st.write("Create and customize your own spiral galaxy.")
st.caption("A procedural visualization, not a real physics simulation.")

# Initialize the random seed once per session
if "galaxy_seed" not in st.session_state:
    st.session_state["galaxy_seed"] = 42

# Change the seed when the user requests a new galaxy
def generate_new_galaxy():
    st.session_state["galaxy_seed"] = int(
        np.random.default_rng().integers(0, 1_000_000)
    )



# Add sidebar controls for the galaxy shape
st.sidebar.header("⚙️ Galaxy Settings")

star_count = st.sidebar.slider(
    "Number of stars",
    min_value=1000,
    max_value=15000,
    value=5000,
    step=1000,
)

arms = st.sidebar.slider(
    "Spiral arms",
    min_value=2,
    max_value=6,
    value=4,
)

twist = st.sidebar.slider(
    "Spiral twist",
    min_value=1.0,
    max_value=8.0,
    value=4.0,
    step=0.5,
)

spread = st.sidebar.slider(
    "Arm spread",
    min_value=0.05,
    max_value=0.50,
    value=0.20,
    step=0.05,
)


# Add color controls
st.sidebar.subheader("🎨 Colors")

star_color = st.sidebar.color_picker(
    "Star color",
    value="#91BFFF",
)

core_color = st.sidebar.color_picker(
    "Core color",
    value="#FFD89B",
)


# Add a button to generate a different random pattern
st.sidebar.button(
    "✨ Generate new galaxy",
    on_click=generate_new_galaxy,
)

st.sidebar.caption(
    f"Current seed: {st.session_state['galaxy_seed']}"
)


# Create a random generator using the current seed
rng = np.random.default_rng(st.session_state["galaxy_seed"])


# Assign each main star a radius and a spiral arm
radius = rng.uniform(0.02, 1.0, star_count)
arm_index = rng.integers(0, arms, star_count)


# Calculate the star angle using its arm, radius, and random variation
#Procedural Spiral Galaxy Formula /  Gaussian-Scattered Spiral Arm Formula.
angle = (
    arm_index * (2 * np.pi / arms)
    + twist * radius
    + rng.normal(0, spread, star_count)
)

# Convert polar coordinates into x and y coordinates
x = radius * np.cos(angle)
y = radius * np.sin(angle)


# Generate display sizes for the main stars
sizes = rng.uniform(0.3, 2.0, star_count)

# Generate a small central cluster
core_count = star_count // 5

core_x = rng.normal(0, 0.06, core_count)
core_y = rng.normal(0, 0.06, core_count)

# Generate distant background stars
background_x = rng.uniform(-1.2, 1.2, 400)
background_y = rng.uniform(-1.2, 1.2, 400)

# Display a short summary of the generated galaxy
col1, col2, col3 = st.columns(3)

col1.metric("Main stars", star_count)
col2.metric("Spiral arms", arms)
col3.metric("Core stars", core_count)


# Create the plotting area
background_color = "#03030D"

fig, ax = plt.subplots(
    figsize=(8, 8),
    facecolor=background_color,
)

ax.set_facecolor(background_color)

# Draw background stars
ax.scatter(
    background_x,
    background_y,
    s=0.5,
    color="white",
    alpha=0.4,
    linewidths=0,
)

# Draw the main stars
ax.scatter(
    x,
    y,
    s=sizes,
    color=star_color,
    alpha=0.85,
    linewidths=0,
)

# Draw the central cluster
ax.scatter(
    core_x,
    core_y,
    s=2,
    color=core_color,
    alpha=0.6,
    linewidths=0,
)

# Set the visible area and hide the axes
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect("equal")
ax.axis("off")


# Display the galaxy in the app
st.pyplot(fig)

# Save the current galaxy as a PNG in memory
image_buffer = io.BytesIO()

fig.savefig(
    image_buffer,
    format="png",
    dpi=150,
    facecolor=background_color,
    bbox_inches="tight",
    pad_inches=0,
)

# Provide an image download button
st.download_button(
    label="📥 Download galaxy",
    data=image_buffer.getvalue(),
    file_name="galaxy.png",
    mime="image/png",
)

# Release the Matplotlib figure
plt.close(fig)