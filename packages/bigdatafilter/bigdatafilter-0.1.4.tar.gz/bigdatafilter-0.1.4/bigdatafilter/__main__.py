import multiprocessing as mp
import tqdm
import os
from pathlib import Path
import shutil
import sys
import time


def dirmap(
    input_dir,
    func,
    additional_args=[],
    concurrent=False,
    cache_name=None,
    working_dir=None,
    inplace=False,
):
    """
    Convenience function for the main entry point of the Manager object
    """

    m = DirectoryMapper(**locals())
    m.execute()


def map(
    input_iter,
    func,
    additional_args=[],
    concurrent=False,
    cache_name=None,
    working_dir=None,
    inplace=False,
):
    """
    Convenience function for the main entry point of the Manager object
    """

    m = IterMapper(**locals())
    m.execute()


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class Timer:
    def __init__(self) -> None:
        self._start_time = None

    def start(self):

        if self._start_time is not None:
            raise TimerError(f"Timer is running")

        self._start_time = time.perf_counter()

    def stop(self) -> float:

        if self._start_time is None:
            raise TimerError(f"Timer is not running")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        return elapsed_time


class Mapper:
    def __init__(
        self,
        func,
        additional_args=[],
        concurrent=False,
        working_dir=None,
        cache_name=None,
        quiet=False,
    ) -> None:

        self.func = func
        self.additional_args = additional_args
        self.working_dir = working_dir
        self.concurrent = concurrent
        self.cache_name = cache_name
        self.quiet = False
        self.i = 0
        self.tqdm_kwargs = {"leave": False}
        self._t = None
        self._timer = Timer()
        self._setup_msg = ""

    def _tqdm_write(self, msg: str) -> None:

        self._t.write(msg)
        if self.quiet and self._t is not None:
            self._t.write(msg)

    def _setup(self):
        """
        Startup actions to be taken before main execution
        """

        self._timer.start()

        if self._setup_msg != "":
            self._tqdm_write(self._setup_msg)

        if self.working_dir is not None:

            if os.path.exists(self.working_dir):
                if len(os.listdir(self.working_dir)) > 0:
                    raise FileExistsError(
                        f"Output directory {self.working_dir} is not empty"
                    )
            else:
                os.makedirs(self.working_dir)

            self.origin_path = os.getcwd()
            os.chdir(self.working_dir)

    def _cleanup(self):

        elapsed_time = self._timer.stop()

        if not self.quiet and self._t is not None:
            self._t.write(f"Elapsed time: {elapsed_time:0.2f} seconds")

        if self.origin_path is not None:
            os.chdir(self.origin_path)

    def _callback(self, result):
        """
        Async callback that is called during execution if the execution
        is using concurrency
        """

        self.i += 1

        if self._t is not None:
            self._t.n = self.i
            self._t.update()

    def _execute_concurrent(self):
        """
        Placeholder
        """
        pass

    def _execute_nonconcurrent(self):
        """
        Placeholder
        """

        pass

    def execute(self):
        """
        Main entry point
        """
        self._setup()

        try:
            if self.concurrent:
                self._execute_concurrent()
            else:
                self._execute_nonconcurrent()
        except KeyboardInterrupt:
            sys.exit(self._cleanup())


class IterMapper(Mapper):
    def __init__(
        self,
        func,
        input_iter,
        additional_args=[],
        concurrent=False,
        cache_name=None,
        working_dir=None,
        inplace=False,
    ) -> None:

        super().__init__(func, additional_args, concurrent, working_dir, cache_name)
        self.input_iter = input_iter
        self._t = tqdm.tqdm(total=len(self.input_iter), **self.tqdm_kwargs)

        self._setup_msg = f"> {len(input_iter)} items -> {working_dir}"

    def _execute_concurrent(self):

        with mp.Pool() as pool:

            for item in self.input_iter:
                args = [item]
                if len(self.additional_args) > 0:
                    for ar in self.additional_args:
                        args.append(ar)
                        # print(args)
                pool.apply_async(self.func, args=tuple(args), callback=self._callback)

            pool.close()
            pool.join()
            self._cleanup()


class DirectoryMapper(Mapper):
    """
    Class that handles the main loop of execution for iterating over files found in the
    input directory. Manages caching and multiprocessing if their respective boolean flags
    are used
    """

    def __init__(
        self,
        func,
        input_dir,
        additional_args=[],
        concurrent=False,
        cache_name=None,
        working_dir=None,
        inplace=False,
    ) -> None:

        if cache_name is None:
            cache_name = Path(input_dir).stem

        super().__init__(func, additional_args, concurrent, working_dir, cache_name)

        self.contents = []

        ext = ""
        for i, file in enumerate(os.scandir(input_dir)):
            self.contents.append(os.path.abspath(file.path))
            if i == 0:
                ext = os.path.splitext(file.name)[1]
            if ext != os.path.splitext(file.name)[1]:
                ext = "varied"

        self._t = tqdm.tqdm(total=len(self.contents), **self.tqdm_kwargs)
        self.input_dir = str(Path(input_dir).absolute())
        self.origin_path = None
        self.cache_file = os.path.join(self.input_dir, (cache_name + ".cache.json"))

        self._setup_msg = f'> {len(self.contents)} files with extension "{ext}" from {input_dir} -> {working_dir}'

    def _execute_concurrent(self):

        """
        Start the execution loop with a multiprocessing pool
        """
        with mp.Pool() as pool:

            for file in self.contents:
                args = [file]
                if len(self.additional_args) > 0:
                    for ar in self.additional_args:
                        args.append(ar)
                        # print(args)
                pool.apply_async(self.func, args=tuple(args), callback=self._callback)

            pool.close()
            pool.join()
            self._cleanup()

    def _execute_nonconcurrent(self):

        raise NotImplementedError(
            "Use concurrent flag, non-concurrent not yet implemented"
        )

        # for file in self.contents:
        #     args = [file]
        #     if len(self.additional_args) > 0:
        #         for ar in self.additional_args:
        #                 args.append(ar)
        #         args.insert(0, file)
        #         self.func(**args)
