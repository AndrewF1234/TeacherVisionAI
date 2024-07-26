# Mounting Docker on Repository
Mounts the container onto repository. Passes in the host directory and then passes in the directory within the container.
```
$ cd jetson-inference
$ docker/run.sh --volume ~/TeacherVisionAI:/TeacherVisionAI
```