# and   import pypipegraph as ppg
#  import time
#  from pathlib import Path
#  from .. import find_code_path
from ..externals import ExternalAlgorithm, reproducible_tar
from ..util import download_file


class LiftOver(ExternalAlgorithm):
    @property
    def name(self):
        return "LiftOver"

    def build_cmd(self, output_directory, ncores, arguments):  # pragma: no cover
        """Arguments = oldFile, map.chain, newFile"""
        return [str(self.path / "liftOver")] + arguments

    @property
    def multi_core(self):  # pragma: no cover
        return False

    def get_latest_version(self):
        return "0.1"

    def fetch_version(self, version, target_filename):  # pragma: no cover
        import tempfile
        from pathlib import Path
        import subprocess

        v = version
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            url = "http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/liftOver"
            with (tmpdir / "liftOver").open("wb") as zip_file:
                download_file(url, zip_file)
                subprocess.check_call(["chmod", "+x", str(tmpdir / "liftOver")])

            reproducible_tar(target_filename, "./liftOver", cwd=tmpdir)
            print(f"done downloading liftover version {v}")


class BedToBigBed(ExternalAlgorithm):
    @property
    def name(self):
        return "bedToBigBed"

    def build_cmd(self, output_directory, ncores, arguments):  # pragma: no cover
        """Arguments = oldFile, map.chain, newFile"""
        return [str(self.path / "bedToBigBed")] + arguments

    @property
    def multi_core(self):  # pragma: no cover
        return False

    def get_latest_version(self):
        return "0.1"

    def fetch_version(self, version, target_filename):  # pragma: no cover
        import tempfile
        from pathlib import Path
        import subprocess

        v = version
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            url = "http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/bedToBigBed"
            with (tmpdir / "bedToBigBed").open("wb") as zip_file:
                download_file(url, zip_file)
                subprocess.check_call(["chmod", "+x", str(tmpdir / "bedToBigBed")])

            reproducible_tar(target_filename, "./bedToBigBed", cwd=tmpdir)
            print(f"done downloading bedToBigBed version {v}")
