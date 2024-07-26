# Mounting Docker on Repository
Mounts the container onto repository. Passes in the host directory and then passes in the directory within the container.
```
$ cd jetson-inference
$ docker/run.sh --volume ~/TeacherVisionAI:/TeacherVisionAI
```

# Deploying a USB camera
Most USB cameras are under the V4L2 devices and can be accessed through:
``` /dev/video0 ```

You can run it using the docker.sh jetson inference with:
```
$ cd jetson-inference/build/aarch64/bin
$ ./imagenet.py /dev/video0
```

Or with recognition.py:

