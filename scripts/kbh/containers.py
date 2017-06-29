from baelfire.dependencies import AlwaysTrue
from baelfire.dependencies import FileChanged
from baelfire.dependencies import TaskRebuilded

from kbh.docker import ContainerBuilder
from kbh.docker import ContainerRunner


class BackendContainerBuild(ContainerBuilder):
    output_name = 'backend_dockerfile_flag'
    container_name = 'backend'

    def create_dependecies(self):
        super().create_dependecies()
        self.build_if(FileChanged('backend_setuppy'))


class RunBackendContainer(ContainerRunner):
    container_name = 'backend'

    def create_dependecies(self):
        self.build_if(TaskRebuilded(BackendContainerBuild()))
        self.build_if(AlwaysTrue())


class RunNginxContainer(ContainerRunner):
    container_name = 'nginx'

    def create_dependecies(self):
        self.build_if(TaskRebuilded(BackendContainerBuild()))
        self.build_if(AlwaysTrue())