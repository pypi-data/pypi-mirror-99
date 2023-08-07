# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import platform
import pkg_resources

# awkward-cuda-kernels is only supported on Linux, but let's leave the placeholder.
if platform.system() == "Windows":
    shared_library_name = "awkward-cuda-kernels.dll"
elif platform.system() == "Darwin":
    shared_library_name = "libawkward-cuda-kernels.dylib"
else:
    shared_library_name = "libawkward-cuda-kernels.so"

shared_library_path = pkg_resources.resource_filename(
    "awkward_cuda_kernels", shared_library_name
)

del platform
del pkg_resources
__version__ ='1.2.0rc4'
cuda_version ='9.0'
docker_image ='docker.io/nvidia/cuda:9.0-devel-ubuntu16.04'
