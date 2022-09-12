import urllib.request
from pathlib import Path
from threading import Thread
from urllib.error import HTTPError

from tqdm import tqdm
#/Wav2Lip/checkpoints/wav2lip_gan.pth
#/Wav2Lip/face_detection/detection/sfd/s3fd.pth
default_models = {
    "wav2lip_gan": ("https://drive.google.com/u/0/uc?id=1V8hobVlZJdp8dzI8qWaAlbhCrXdBiUET&export=download&confirm=t", 435801865,'checkpoints'),
    "s3fd": ("https://drive.google.com/u/0/uc?id=1Y-mgxW8iq1pXUQicU_8ClNB85eQ1lk0o&export=download", 89843225,'face_detection/detection/sfd'),

}


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download(url: str, target: Path, bar_pos=0):
    # Ensure the directory exists
    target.parent.mkdir(exist_ok=True, parents=True)

    desc = f"Downloading {target.name}"
    with DownloadProgressBar(unit="B", unit_scale=True, miniters=1, desc=desc, position=bar_pos, leave=False) as t:
        try:
            urllib.request.urlretrieve(url, filename=target, reporthook=t.update_to)
        except HTTPError:
            return


def ensure_default_models(models_dir: Path):
    # Define download tasks
    jobs = []
    for model_name, (url, size,path_tobe) in default_models.items():
        target_path = models_dir   / path_tobe / f"{model_name}.pth"
        print(target_path)
        if target_path.exists():
            if target_path.stat().st_size != size:
                print(f"File {target_path} is not of expected size, redownloading...")
            else:
                continue

        thread = Thread(target=download, args=(url, target_path, len(jobs)))
        thread.start()
        jobs.append((thread, target_path, size))

    # Run and join threads
    for thread, target_path, size in jobs:
        thread.join()

        assert target_path.exists() and target_path.stat().st_size == size, \
            f"Download for {target_path.name} failed. You may download models manually instead.\n" \
