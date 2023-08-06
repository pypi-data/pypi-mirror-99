import multiprocessing as mp
from tqdm import tqdm
import os
from pathlib import Path
import shutil
import sys


def map(
    input_dir,
    func,
    additional_args=[],
    concurrent=False,
    cache_name=None,
    output_dir=None,
    inplace=False,
):
    """
    Convenience function for the main entry point of the Manager object
    """

    m = Manager(**locals())
    m.execute()


class Manager:
    """
    Class that handles the main loop of execution for iterating over files found in the
    input directory. Manages caching and multiprocessing if their respective boolean flags
    are used
    """

    def __init__(
        self,
        input_dir,
        func,
        additional_args=[],
        concurrent=False,
        cache_name=None,
        output_dir=None,
        inplace=False,
    ) -> None:

        self.func = func
        self.contents = [os.path.abspath(file.path) for file in os.scandir(input_dir)]
        self.t = tqdm(total=len(self.contents))
        self.additional_args = additional_args
        self.input_dir = str(Path(input_dir).absolute())
        self.concurrent = concurrent
        self.output_dir = output_dir
        self.origin_path = None
        self.i = 0

        if cache_name is None:
            cache_name = Path(input_dir).stem

        self.cache_file = os.path.join(self.input_dir, (cache_name + ".cache.json"))

    def __callback(self, result):
        """
        Async callback that is called during execution if the execution
        is using concurrency
        """

        # assert os.path.exists(result)

        # if self.output_dir is not None:
        #     os.rename(result, os.path.join(self.output_dir, result))

        self.i += 1
        self.t.n = self.i
        self.t.update()

    def __setup(self):
        """
        Startup actions to be taken before main execution
        """

        if self.output_dir is not None:
            sys.path.append(os.getcwd())
            os.makedirs(self.output_dir)
            self.origin_path = os.getcwd()
            os.chdir(self.output_dir)

    def __cleanup(self):
        if self.origin_path is not None:
            os.chdir(self.origin_path)

    def __execute_concurrent(self):

        """
        Start the execution loop with a multiprocessing pool
        """

        with mp.Pool() as pool:

            for file in self.contents:
                args = [file]

                if len(self.additional_args) > 0:
                    for ar in self.additional_args:
                        args.append(ar)
                        print(args)
                pool.apply_async(self.func, args=tuple(args), callback=self.__callback)

            pool.close()
            pool.join()
            self.__cleanup()

    def __execute_nonconcurrent(self):

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

    def execute(self):
        """
        Main entry point
        """

        self.__setup()

        try:
            if self.concurrent:
                self.__execute_concurrent()
            else:
                self.__execute_nonconcurrent()
        except KeyboardInterrupt:
            sys.exit(self.__cleanup())