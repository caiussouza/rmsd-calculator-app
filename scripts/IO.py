import tempfile
from pathlib import Path

from openbabel import openbabel as ob
from biopandas.mol2 import PandasMol2


class IO():
    """
    Handles file input/output, converting molecular files to MOL2 format
    and returning them as a DataFrame.
    """
    @staticmethod
    def open(file_path):
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
        ob_conversion = ob.OBConversion()
        ob_conversion.SetInAndOutFormats(file_type, "mol2")

        mol = ob.OBMol()
        success = ob_conversion.ReadFile(mol, str(file_path))
        if not success:
            raise ValueError(f"No molecules found on {file_path.name}")

        mol.DeleteHydrogens()

        mol2_str = ob_conversion.WriteString(mol)

        return mol2_str
