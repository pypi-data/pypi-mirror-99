__version__ = '0.9.1'
git_version = '046cabc233e12c60d084e767db1d3c4d4d4533bd'
from torchvision.extension import _check_cuda_version
if _check_cuda_version() > 0:
    cuda = _check_cuda_version()
