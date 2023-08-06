import multiprocessing as mp
from tqdm import tqdm
import os
from pathlib import Path


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
        inplace=False,
    ) -> None:

        self.func = func
        self.contents = [file.path for file in os.scandir(input_dir)]
        self.t = tqdm(total=len(self.contents))
        self.additional_args = additional_args
        self.input_dir = str(Path(input_dir).absolute())
        self.concurrent = concurrent
        self.i = 0

        if cache_name is None:
            cache_name = Path(input_dir).stem

        self.cache_file = os.path.join(self.input_dir, (cache_name + ".cache.json"))

    def __callback(self, result):
        self.i += 1
        self.t.n = self.i
        self.t.update()

    def execute(self):

        if self.concurrent:

            with mp.Pool() as pool:

                for file in self.contents:
                    args = [file]
                    if len(self.additional_args) > 0:
                        for ar in self.additional_args:
                            args.append(ar)
                    pool.apply_async(
                        self.func, args=tuple(args), callback=self.__callback
                    )

                pool.close()
                pool.join()

        else:
            for file in self.contents:
                args = [file]
                if len(self.additional_args) > 0:
                    for ar in self.additional_args:
                        args.append(ar)
                args.insert(0, file)
                self.func(**args)
