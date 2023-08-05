#!/usr/bin/python3
# ***************************************************************
# Copyright (c) 2021 Jittor. All Rights Reserved. 
# Maintainers: Dun Liang <randonlang@gmail.com>. 
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
# ***************************************************************

# Polish steps:
# 1. create jittor-polish repo
# 2. copy jittor src into it
# 3. remove files
# 4. commit jittor-polish(check modify and break)
# 5. compile to build/$git_version/$cc_type/$use_cuda/a.obj
# 6. rsync to build-server
# 7. push to github
# 8. push to pip

import os
import jittor as jt
from jittor import LOG
from jittor.compiler import run_cmd
from jittor_utils import translator
import sys

jittor_path = jt.flags.jittor_path
root_path = os.path.realpath(os.path.join(jt.flags.jittor_path, "..", ".."))
data_path = os.path.join(jittor_path, "src", "__data__")
build_path = os.path.join(data_path, "build")
if not os.path.isdir(build_path):
    os.mkdir(build_path)
status = run_cmd("git status", data_path)
print(status)
if "working tree clean" not in status:
    LOG.f("__data__ has untracked files")

git_version = run_cmd("git rev-parse HEAD", data_path)
LOG.i("git_version", git_version)

run_cmd(f"git rev-parse HEAD > {jittor_path}/version", data_path)

# remove files
files = jt.compiler.files
data_files = [ name for name in files
    if "__data__" in name
]
LOG.i("data_files", data_files)

# compile data files
from pathlib import Path
home = str(Path.home())
# for cc_type in ["g++", "clang"]:
#     for device in ["cpu", "cuda"]:
for cc_type in ["g++"]:
    for device in ["cpu"]:
        key = f"{git_version}-{cc_type}-{device}"
        env = f"cache_name=build/{cc_type}/{device} cc_path="
        cname = "g++" if cc_type=="g++" else "clang-8"
        env += cname
        # use core2 arch, avoid using avx instructions
        # TODO: support more archs, such as arm, or use ir(GIMPLE or LLVM)
        env += " cc_flags='-march=core2' "
        if device == "cpu":
            env += "nvcc_path='' "
        elif jt.flags.nvcc_path == "":
            env = "unset nvcc_path && " + env
        cmd = f"{env} {sys.executable} -c 'import jittor'"
        LOG.i("run cmd:", cmd)
        os.system(cmd)
        LOG.i("run cmd:", cmd)
        os.system(cmd)

        obj_path = home + f"/.cache/jittor/build/{cc_type}/{device}/{cname}/obj_files"
        obj_files = []
        for name in data_files:
            name = name.split("/")[-1]
            fname = f"{obj_path}/{name}.o"
            assert os.path.isfile(fname), fname
            obj_files.append(fname)
        run_cmd(f"ld -r {' '.join(obj_files)} -o {build_path}/{key}.o")

# compress source
# tar -cvzf build/jittor.tgz . --exclude build --exclude .git --exclude .ipynb_checkpoints --exclude __pycache__
# mkdir -p jittor && tar -xvf ./jittor.tgz -C jittor
assert os.system(f"cd {root_path} && tar --exclude=build --exclude=.git --exclude=.ipynb_checkpoints --exclude=__pycache__ --exclude=__data__  --exclude=my --exclude=dist  --exclude=.vscode --exclude=.github  -cvzf {build_path}/jittor.tgz * ")==0

# rsync to build-server
jittor_web_base_dir = "Documents/jittor-blog/assets/"
jittor_web_build_dir = jittor_web_base_dir
assert os.system(f"rsync -avPu {build_path} jittor-web:{jittor_web_build_dir}")==0
assert os.system(f"ssh jittor-web Documents/jittor-blog.git/hooks/post-update")==0


# sys.exit(0)

# push to github
# assert os.system(f"cd {polish_path} && git push -f origin master")==0

# push to pip