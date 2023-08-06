from abc import abstractmethod
import os
from typing import Union
from ._shellscript import ShellScript
from .dockerimage import DockerImage, _use_singularity

class DockerImageFromScript(DockerImage):
    def __init__(self, *, name: str, dockerfile: str):
        self._name = name
        self._dockerfile = dockerfile
        self._prepared = False
        self._tag: Union[None, str] = None
    def _get_tag_from_dockerfile(self) -> str:
        try:
            from dockerfile_parse import DockerfileParser
        except:
            raise Exception('dockerfile-parse python package not installed.')
        dfp = DockerfileParser()
        with open(self._dockerfile, 'r') as df:
            dfp.content = df.read()
        version = dfp.labels.get('version', None)
        if version is None:
            raise Exception('Dockerfile must have "LABEL version=..."')
        return version
    def prepare(self):
        if not self._prepared:
            self._tag = self._get_tag_from_dockerfile()
            dockerfile_dir = os.path.dirname(self._dockerfile)
            dockerfile_basename = os.path.basename(self._dockerfile)
            try:
                import docker
            except:
                raise Exception('docker python package not installed.')

            if _use_singularity():
                ss = ShellScript(f'''
                #!/bin/bash

                singularity pull docker://{self._name}:{self._tag}
                singularity build docker://{self._name}:{self._tag}
                ''')
                ss.start()
                ss.wait()
                self._prepared = True
            else:
                docker_client = docker.from_env()
                try:
                    docker_client.images.get(self._name + ':' + self._tag)
                    found_image = True
                except:
                    found_image = False
                if found_image:
                    # already built
                    self._prepared = True
                    return

                dockerfile_dir = os.path.dirname(self._dockerfile)
                dockerfile_basename = os.path.basename(self._dockerfile)

                # client = docker.from_env()
                # image = client.images.build(tag=self._name, path=dockerfile_dir, dockerfile=dockerfile_basename)
                
                ss = ShellScript(f'''
                #!/bin/bash

                cd {dockerfile_dir}
                docker build -t {self._name}:{self._tag} -f {dockerfile_basename} .
                ''')
                ss.start()
                ss.wait()
                self._prepared = True
    def is_prepared(self) -> bool:
        return self._prepared
    def get_name(self) -> str:
        return self._name
    def get_tag(self) -> str:
        assert self._tag is not None, 'self._tag is not None, image not prepared'
        return self._tag