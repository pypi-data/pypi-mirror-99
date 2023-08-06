from .base import Aligner
import pypipegraph as ppg
from pathlib import Path
from ..util import download_file, Version


class Subread(Aligner):
    def __init__(self, version="_last_used", store=None):
        super().__init__(version, store)

    @property
    def name(self):
        return "Subread"

    @property
    def multi_core(self):
        return True

    def _aligner_build_cmd(self, output_dir, ncores, arguments):
        if "subread-align" in arguments[0]:
            return arguments + ["-T", str(ncores)]
        else:
            return arguments

    def align_job(
        self,
        input_fastq,
        paired_end_filename,
        index_basename,
        output_bam_filename,
        parameters,
    ):
        if not parameters.get("input_type") in ("dna", "rna"):
            raise ValueError("invalid parameters['input_type'], must be dna or rna")

        if parameters["input_type"] == "dna":
            input_type = "1"
        else:
            input_type = "0"
        output_bam_filename = Path(output_bam_filename)
        cmd = [
            "FROM_ALIGNER",
            str(
                self.path
                / f"subread-{self.version}-Linux-x86_64"
                / "bin"
                / "subread-align"
            ),
            "-t",
            input_type,
            "-I",
            "%i" % parameters.get("indels_up_to", 5),
            "-B",
            "%i" % parameters.get("max_mapping_locations", 1),
            "-i",
            (Path(index_basename) / "subread_index").absolute(),
            "-r",
            Path(input_fastq).absolute(),
            "-o",
            output_bam_filename.absolute(),
        ]
        if "keepReadOrder" in parameters:  # pragma: no cover
            cmd.append("--keepReadOrder")
        else:
            cmd.append("--sortReadsByCoordinates")
        if paired_end_filename:
            cmd.extend(("-R", str(Path(paired_end_filename).absolute())))
        if "max_mapping_locations" in parameters:  # pragma: no cover
            cmd.append("--multiMapping")

        def remove_bai():
            # subread create broken bais where idxstat doesn't work.
            # but the mbf_aligned.lanes.AlignedSample will recreate it.
            # so it's ok if we simply throw it away here.
            bai_name = output_bam_filename.with_name(output_bam_filename.name + ".bai")
            if bai_name.exists():
                bai_name.unlink()

        job = self.run(
            Path(output_bam_filename).parent,
            cmd,
            additional_files_created=[
                output_bam_filename,
                # subread create broken bais where idxstat doesn't work.
                # output_bam_filename.with_name(output_bam_filename.name + ".bai"),
            ],
            call_afterwards=remove_bai,
        )
        job.depends_on(
            ppg.ParameterInvariant(output_bam_filename, sorted(parameters.items()))
        )
        return job

    def build_index_func(self, fasta_files, gtf_input_filename, output_fileprefix):
        cmd = [
            "FROM_ALIGNER",
            str(
                self.path
                / f"subread-{self.version}-Linux-x86_64"
                / "bin"
                / "subread-buildindex"
            ),
            "-o",
            str((output_fileprefix / "subread_index").absolute()),
        ]
        if not hasattr(fasta_files, "__iter__"):
            fasta_files = [fasta_files]
        cmd.extend([str(Path(x).absolute()) for x in fasta_files])
        return self.get_run_func(output_fileprefix, cmd)

    def get_index_version_range(self):
        """What minimum_acceptable_version, maximum_acceptable_version for the index is ok?"""
        if Version(self.version) >= "1.6":
            return "1.6", None
        else:
            return "0.1", "1.5.99"

    def get_latest_version(self):
        return "1.6.3"

    def fetch_version(self, version, target_filename):  # pragma: no cover
        url = f"https://downloads.sourceforge.net/project/subread/subread-{version}/subread-{version}-Linux-x86_64.tar.gz"
        with open(target_filename, "wb") as op:
            download_file(url, op)

    def get_alignment_stats(self, output_bam_filename):
        import re

        output_bam_filename = Path(output_bam_filename)
        target = output_bam_filename.parent / "stderr.txt"
        raw = target.read_text()
        raw = raw[raw.find("= Summary =") :]
        result = {}
        keys = "Uniquely mapped", "Multi-mapping", "Unmapped"
        for k in keys:
            result[k] = int(re.findall(f"{k} : (\\d+)", raw)[0])
        return result
