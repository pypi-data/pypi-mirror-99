"""
Many algorithms need prebuild data structures (indices and so on)
which both are too time consuming to build, to big to copy to each
experiment and need to be versioned,
but they can often be shared among versions."""

import socket
from .util import Version, sort_versions, UpstreamChangedError, write_md5_sum
import pypipegraph as ppg
from pathlib import Path
import time
import stat
import os
import json


class PrebuildFunctionInvariantFileStoredExploding(ppg.FunctionInvariant):
    def __init__(self, storage_filename, func):
        self.is_prebuild = True
        super().__init__(storage_filename, func)

    @classmethod
    def hash_function(cls, function):
        new_source, new_funchash, new_closure = cls._hash_function(function)
        return cls._compare_new_and_old(new_source, new_funchash, new_closure, False)

    def _get_invariant(self, old, all_invariant_stati):
        stf = Path(
            self.job_id
        )  # the old file format - using just the function's dis-ed code.
        stf2 = Path(self.job_id).with_name(
            stf.name + "2"
        )  # the new style, dict based storage just like FunctionInvariant after 0.190
        new_source, new_func_hash, new_closure = self._hash_function(self.function)
        if stf2.exists():
            old_hash = json.loads(stf2.read_text())
        elif stf.exists():
            old_hash = stf.read_text()
            new_closure = ""
        else:
            new_value = self._compare_new_and_old(
                new_source, new_func_hash, new_closure, False
            )
            stf2.write_text(json.dumps(new_value))
            return old  # signal no change necessary.

        try:
            new_hash = self._compare_new_and_old(
                new_source, new_func_hash, new_closure, old_hash
            )
            if new_hash != old_hash:
                self.complain_about_hash_changes(new_hash)
            else:
                return old
        except ppg.NothingChanged as e:
            # we accept the stuff there as no change.
            # and we write out the new value, because it might be a format change.
            try:
                stf2.write_text(json.dumps(e.new_value))
            except OSError as e2:
                if "Read-only file system" in str(e2):
                    import warnings

                    warnings.warn(
                        "PrebuildFunctionInvariantFileStoredExploding: Could not update %s to newest version - read only file system"
                        % stf
                    )
            raise e
        raise NotImplementedError("Should not happen")

    def complain_about_hash_changes(self, invariant_hash):
        stf = Path(self.job_id)
        try:
            of = stf.with_name(stf.name + ".changed")
            of.write_text(json.dumps(invariant_hash))
        except IOError:  # noqa: E722 pragma: no cover
            # fallback if the stf directory is not writeable.
            of = Path(stf.name + ".changed")  # pragma: no cover
            of.write_text(json.dumps(invariant_hash))  # pragma: no cover
        raise UpstreamChangedError(
            (
                "Calculating function changed.\n"
                "If you are actively working on it, you need to bump the version:\n"
                "If not, you need to figure out what's causing the change.\n"
                "Do not nuke the job info (%s) light heartedly\n"
                "To compare, run \n"
                "icdiff %s %s"
            )
            % (self.job_id, Path(self.job_id).absolute(), of.absolute())
        )


class _PrebuildFileInvariantsExploding(ppg.MultiFileInvariant):
    """Used by PrebuildJob to handle input file deps"""

    def __new__(cls, job_id, filenames):
        job_id = "PFIE_" + str(job_id)
        return ppg.Job.__new__(cls, job_id)

    def __init__(self, job_id, filenames):
        job_id = "PFIE_" + str(job_id)
        self.filenames = filenames
        for f in filenames:
            if not (isinstance(f, str) or isinstance(f, Path)):  # pragma: no cover
                raise ValueError(f"filenames must be str/path. Was {repr(f)}")
        self.is_prebuild = True
        ppg.Job.__init__(self, job_id)

    def calc_checksums(self, old):
        """return a list of tuples
        (filename, filetime, filesize, checksum)"""
        result = []
        if old:
            old_d = {x[0]: x[1:] for x in old}
        else:
            old_d = {}
        for fn in self.filenames:
            if not os.path.exists(fn):
                result.append((fn, None, None, None))
            else:
                st = os.stat(fn)
                filetime = st[stat.ST_MTIME]
                filesize = st[stat.ST_SIZE]
                if (
                    fn in old_d
                    and (old_d[fn][0] == filetime)
                    and (old_d[fn][1] == filesize)
                ):  # we can reuse the checksum
                    result.append((fn, filetime, filesize, old_d[fn][2]))
                else:
                    result.append((fn, filetime, filesize, ppg.util.checksum_file(fn)))
        return result

    def _get_invariant(self, old, all_invariant_stati):
        if not old:
            old = self.find_matching_renamed(all_invariant_stati)
        checksums = self.calc_checksums(old)
        if old is False:
            raise ppg.ppg_exceptions.NothingChanged(checksums)
        # elif old is None: # not sure when this would ever happen
        # return checksums
        else:
            old_d = {x[0]: x[1:] for x in old}
            checksums_d = {x[0]: x[1:] for x in checksums}
            for fn in self.filenames:
                if old_d[fn][2] != checksums_d[fn][2] and old_d[fn][2] is not None:
                    raise UpstreamChangedError(
                        """Upstream file changed for job, bump version or rollback.
Job: %s
File: %s"""
                        % (self, fn)
                    )
                    # return checksums
            raise ppg.ppg_exceptions.NothingChanged(checksums)


class PrebuildJob(ppg.MultiFileGeneratingJob):
    def __new__(cls, filenames, calc_function, output_path):
        if not hasattr(filenames, "__iter__"):
            raise TypeError("filenames was not iterable")
        for x in filenames:
            if not (isinstance(x, str) or isinstance(x, Path)):
                raise TypeError("filenames must be a list of strings or pathlib.Path")
        for of in filenames:
            if of.is_absolute():
                raise ValueError("output_files must be relative")
        filenames = cls._normalize_output_files(filenames, output_path)
        job_id = ":".join(sorted(str(x) for x in filenames))
        res = ppg.Job.__new__(cls, job_id)
        res.filenames = filenames
        res.output_path = Path(output_path)
        return res

    @classmethod
    def _normalize_output_files(cls, output_files, output_path):
        output_files = [
            Path(cls.verify_job_id(output_path / of)) for of in output_files
        ]
        output_files.append(Path(cls.verify_job_id(output_path / "mbf.done")))
        return output_files

    def __init__(self, output_files, calc_function, output_path):
        output_files = self._normalize_output_files(output_files, output_path)
        output_path.mkdir(parents=True, exist_ok=True)

        self.real_callback = calc_function
        self.is_prebuild = True

        def calc():
            self.real_callback(output_path)
            output_files[-1].write_text(str(time.time()))
            for fn in output_files[:-1]:
                if os.path.exists(fn):
                    write_md5_sum(fn)

        super().__init__(output_files, calc, rename_broken=True, empty_ok=True)
        self.output_path = output_path

    def depends_on_func(self, name, func):
        job = PrebuildFunctionInvariantFileStoredExploding(
            self.output_path / ("%s.md5sum" % (name,)), func
        )
        self.depends_on(job)
        return job

    def depends_on_file(self, filename):
        job = _PrebuildFileInvariantsExploding(filename, [filename])
        self.depends_on(job)
        return job

    def depends_on(self, jobs):
        for job in ppg.util.flatten_jobs(jobs):
            if not hasattr(job, "is_prebuild") or not job.is_prebuild:
                raise ppg.JobContractError(
                    "%s depended on a non-prebuild dependency %s - not supported"
                    % (self, job)
                )
            ppg.Job.depends_on(self, job)
        return self

    def inject_auto_invariants(self):
        self.depends_on_func("mbf_func", self.real_callback)

    def invalidated(self, reason):
        exists = [Path(of).exists() for of in self.filenames]
        if all(exists) or not any(exists):
            pass
        else:
            raise ValueError(
                "Some output files existed, some don't - undefined state, manual cleanup needed\n:%s"
                % (list(zip(self.filenames, exists)))
            )
        self.was_invalidated = True

    def name_file(self, output_filename):
        """Adjust path of output_filename by job path"""
        return self.output_path / output_filename

    def find_file(self, output_filename):
        """Search for a file named output_filename in the job's known created files"""
        of = self.name_file(output_filename)
        for fn in self.filenames:
            if of.resolve() == Path(fn).resolve():
                return of
        else:
            raise KeyError("file not found: %s" % output_filename)


class PrebuildManager:
    def __init__(self, prebuilt_path, hostname=None):
        self.prebuilt_path = Path(prebuilt_path)
        self.hostname = hostname if hostname else socket.gethostname()
        (self.prebuilt_path / self.hostname).mkdir(exist_ok=True)

    def _find_versions(self, name):
        result = {}
        dirs_to_consider = [
            p
            for p in self.prebuilt_path.glob("*")
            if (p / name).exists() and p.name != self.hostname
        ]
        # prefer versions from this host - must be last!
        dirs_to_consider.append(self.prebuilt_path / self.hostname)
        for p in dirs_to_consider:
            for v in (p / name).glob("*"):
                if (v / "mbf.done").exists():
                    result[v.name] = v
        return result

    def prebuild(  # noqa: C901
        self,
        name,
        version,
        input_files,
        output_files,
        calculating_function,
        minimum_acceptable_version=None,
        maximum_acceptable_version=None,
        further_function_deps={},
    ):
        """Create a job that will prebuilt the files if necessary

        @further_function_deps is a dictionary name => func,
        and will end up as PrebuildFunctionInvariantFileStoredExploding
        in the correct directory

        """
        if minimum_acceptable_version is None:
            minimum_acceptable_version = version

        available_versions = self._find_versions(name)
        if version in available_versions:
            output_path = available_versions[version]
        else:
            # these are within minimum..maximum_acceptable_version
            acceptable_versions = sort_versions(
                [
                    (v, p)
                    for v, p in available_versions.items()
                    if (
                        (Version(v) >= minimum_acceptable_version)
                        and (
                            maximum_acceptable_version is None
                            or (Version(v) < maximum_acceptable_version)
                        )
                    )
                ]
            )
            ok_versions = []

            (
                new_source,
                new_funchash,
                new_closure,
            ) = ppg.FunctionInvariant._hash_function(calculating_function)

            for v, p in acceptable_versions:
                func_md5sum_path = p / "mbf_func.md5sum"
                func_md5sum_path2 = p / "mbf_func.md5sum2"
                try:
                    func_md5sum = json.loads(func_md5sum_path2.read_text())
                except OSError:
                    func_md5sum = func_md5sum_path.read_text()
                ok = False
                try:
                    new = ppg.FunctionInvariant._compare_new_and_old(
                        new_source, new_funchash, new_closure, func_md5sum
                    )
                    ok = False
                except ppg.NothingChanged:
                    ok = True
                if ok:
                    ok_versions.append((v, p))

            if ok_versions:
                version, output_path = ok_versions[-1]
            else:  # no version that is within the acceptable range and had the same build function
                output_path = self.prebuilt_path / self.hostname / name / version

        if isinstance(output_files, (str, Path)):
            output_files = [output_files]
        output_files = [Path(of) for of in output_files]
        if ppg.inside_ppg():
            job = PrebuildJob(output_files, calculating_function, output_path)
            job.depends_on(_PrebuildFileInvariantsExploding(output_path, input_files))
            job.version = version
            return job
        else:
            for of in output_files:
                if not (output_path / of).exists():
                    raise ValueError(
                        "%s was missing and prebuild used outside of ppg - can't build it"
                        % (output_path / of).absolute()
                    )

            class DummyJob:
                """just enough of the Jobs interface to ignore the various calls
                and allow finding the msgpack jobs
                """

                def __init__(self, output_path, filenames):
                    self.output_path = output_path
                    self.filenames = PrebuildJob._normalize_output_files(
                        filenames, output_path
                    )
                    # self.job_id = ":".join(sorted(str(x) for x in filenames))

                def depends_on(self, _other_job):  # pragma: no cover
                    return self

                def depends_on_func(self, _name, _func):  # pragma: no cover
                    return self

                def depends_on_file(self, _filename):  # pragma: no cover
                    return self

                def name_file(self, output_filename):
                    """Adjust path of output_filename by job path"""
                    return self.output_path / output_filename

                def find_file(self, output_filename):
                    """Search for a file named output_filename in the job's known created files"""
                    of = self.name_file(output_filename)
                    for fn in self.filenames:
                        if of.resolve() == Path(fn).resolve():
                            return of
                    else:
                        raise KeyError("file not found: %s" % output_filename)

                def __iter__(self):
                    yield self

            return DummyJob(output_path, output_files)


_global_manager = None


def change_global_manager(new_manager):
    global _global_manager
    _global_manager = new_manager


def get_global_manager():
    return _global_manager
