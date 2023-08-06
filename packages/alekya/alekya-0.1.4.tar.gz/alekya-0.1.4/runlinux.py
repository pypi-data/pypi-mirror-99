import os,time

commands = ["python setup.py sdist", "twine upload -r testpypi dist/* -username='alekya' -password='Kumar2020' --repository-url https://upload.pypi.org/legacy/"]
for c in commands:
    stream = os.popen(c)
    output = stream.readlines()
    for x in output:
        print(x)
    time.sleep(5)
