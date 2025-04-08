import tempfile
from pathlib import Path

from openbabel import pybel
from biopandas.mol2 import PandasMol2


class IO():
    """
    Handles file input/output, converting molecular files to MOL2 format
    and returning them as a DataFrame.
    """
    @staticmethod
    def open(file_path):
        """
        Converts a file to MOL2 format and returns its data as a DataFrame.
        Args:
            file_path (str): Path to the input file.
        Returns:
            pandas.DataFrame: DataFrame containing the MOL2 file data.
        """
        file_path = Path(file_path)
        file_type = file_path.suffix[1:]

        mol2_str = IO._to_mol2(file_path, file_type)
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mol2") as tmp_f:
            temp_path = tmp_f.name
            with open(temp_path, "w") as f:
                f.write(mol2_str)
            mol2_df = PandasMol2().read_mol2(temp_path).df

        return mol2_df

    @staticmethod
    def _to_mol2(file_path, file_type):
        mols = list(pybel.readfile(file_type, str(file_path)))

        if not mols:
            raise ValueError(f"No molecules found on {file_path.name}")

        mol = mols[0]
        mol.removeh()
        mol2_str = mol.write("mol2")

        return mol2_str
