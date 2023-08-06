import os

commands = ["python setup.py sdist", "twine upload -r testpypi dist/* -username='alekya' -password='Kumar2020' --verbose"]
for c in commands:
    stream = os.popen(c)
    output = stream.readlines()
    for x in output:
        print(x)
