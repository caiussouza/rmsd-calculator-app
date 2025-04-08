from pathlib import Path
from PIL import Image
import tempfile

import streamlit as st

from IO import IO
from RMSD import RMSD


st.set_page_config(page_title="RMSD Calculator", layout="centered")
st.markdown("""
    <style>
    @media (prefers-color-scheme: dark) {
        .sticky-header {
            background-color: rgba(14, 17, 23, 0.8);
            color: white;
            border-bottom: 1px solid #444;
        }
    }

    @media (prefers-color-scheme: light) {
        .sticky-header {
            background-color: rgba(255, 255, 255, 0.8);
            color: black;
            border-bottom: 1px solid #ccc;
        }
    }

    .sticky-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        padding: 25px 0;
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        z-index: 1000;
    }

    .main-content {
        padding-top: 80px;
    }
    </style>

    <div class="sticky-header">
        <br>
        Molecular RMSD Calculator
    </div>
    <div class="main-content">
""", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("imgs/ilustracao_site.png", width=350)

st.markdown("""
*This application calculates the Root Mean Square Deviation (RMSD)
between two molecular structures.*
""")
with st.expander("ℹ️ About RMSD Calculation"):
    st.markdown("""
**RMSD (Root Mean Square Deviation)** is a measure of the average distance
between atoms (usually the backbone atoms) of aligned molecules.

### Formula
RMSD is computed as:

$$
\\text{RMSD} = \\sqrt{\\frac{1}{N} \\sum_{i=1}^{N} \\|x_i - y_i\\|^2}
$$

Where:
- **N** is the number of atoms
- **x_i** are the coordinates of atom *i* in the reference molecule
- **y_i** are the coordinates in the model molecule

### Note
- No structural alignment is performed (only direct positional comparison).
    """)
st.markdown("---")
st.markdown("### Upload your molecules")
with st.expander("📤 Uploading rules"):
    st.markdown("""
- Upload two molecular files in the allowed formats.
- Both molecules must have equal numbers of atoms.
- The atoms must be in the same order.
- The molecules should have been aligned previously.
""")

file1 = st.file_uploader(
    "**Probe molecule**", type=["sdf", "mol", "mol2", "pdb", "xyz"])
file2 = st.file_uploader(
    "**Reference molecule**", type=["sdf", "mol", "mol2", "pdb", "xyz"])

if file1 and file2:
    with tempfile.TemporaryDirectory() as tmpdir:
        path1 = Path(tmpdir) / file1.name
        path2 = Path(tmpdir) / file2.name

        path1.write_bytes(file1.read())
        path2.write_bytes(file2.read())

        try:
            mol_df1 = IO.open(path1)
            mol_df2 = IO.open(path2)
            with st.expander("🔍 Check your data"):
                st.markdown("**Probe molecule**")
                st.markdown(f"**File name:** {file1.name}")
                st.dataframe(mol_df1)
                st.markdown("**Reference molecule**")
                st.markdown(f"**File name:** {file2.name}")
                st.dataframe(mol_df2)

            if st.button("Calculate RMSD"):
                rmsd = RMSD.calculate(mol_df1, mol_df2)
                st.success(f"RMSD: {rmsd:.4f}")

        except Exception as e:
            st.error(f"Error: {str(e)}")


logos = [
    ("imgs/logo_ufmg.png", "UFMG"),
    ("imgs/logo_fapemig.png", "FAPEMIG"),
    ("imgs/logo_litc.png", "LITC"),
    ("imgs/logo_mmlab.png", "MMLab")
]

st.markdown("---")
st.markdown("**Supported by**")

cols = st.columns(len(logos))

for col, (path, alt) in zip(cols, logos):
    img = Image.open(path).resize((150, 90))
    col.image(img, caption=alt)
