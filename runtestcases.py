import os
import shlex
import glob
import subprocess

dpath = "testcases"


def run(args, dpath):
    print(f"Running: {shlex.join(args)} # in dir {shlex.quote(dpath)}")
    subprocess.run(args, cwd=dpath, check=True)


testwords = {
    "hello-world": "hello",
    "hello-world-wmain": "hęłło",
}


buildgenpy = os.path.abspath("buildgen.py")
for dname in os.listdir("testcases"):
    dpath = os.path.join("testcases", dname)
    print("#" * 50)
    print(dpath)
    cfiles = [os.path.basename(x) for x in glob.glob(f"{dpath}/*.c")]
    print(cfiles)

    run(["python3", buildgenpy] + sorted(cfiles), dpath=dpath)
    run(["busybox", "bash", "build.sh"], dpath=dpath)

    testword = testwords.get(dname, "???")

    # TODO: check its jsut 1 or sort them since calver sorts well, or idk, delete them before/after build/test
    exes = glob.glob(f"{dpath}/*.exe")
    r = subprocess.run(
        [exes[0], testword],
        stdout=subprocess.PIPE,
        check=True,
        encoding="UTF-8",
    )
    print(f"{dname} exe OK? {r.stdout == testword}")

    linuxes = glob.glob(f"{dpath}/*.linux")
    r = subprocess.run(
        ["wsl", linuxes[0].replace("\\", "/"), testword],
        stdout=subprocess.PIPE,
        check=True,
        encoding="UTF-8",
    )

    print(f"{dname} linux OK? {r.stdout == testword}")
    print()

# hmm, how to here make sure ascii and utf-16 are preserved... maybe instead of iterating list test cases one by one, blaze/bazel like?
