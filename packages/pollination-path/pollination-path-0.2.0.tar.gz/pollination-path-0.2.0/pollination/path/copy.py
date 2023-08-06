from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class Copy(Function):
    """Copy a file or folder to a destination."""

    src = Inputs.path(
        description='Path to a input file or folder.', path='input_path'
    )

    @command
    def copy_file(self):
        return 'echo copying input path...'

    dst = Outputs.path(
        description='Output file or folder.', path='input_path'
    )


@dataclass
class CopyMultiple(Function):
    """Copy a file or folder to multiple destinations."""

    src = Inputs.path(
        description='Path to a input file or folder.', path='input_path'
    )

    @command
    def copy_file(self):
        return 'echo copying input path...'

    dst_1 = Outputs.path(description='Output 1 file or folder.', path='input_path')

    dst_2 = Outputs.path(description='Output 2 file or folder.', path='input_path')

    dst_3 = Outputs.path(description='Output 3 file or folder.', path='input_path')

    dst_4 = Outputs.path(description='Output 4 file or folder.', path='input_path')

    dst_5 = Outputs.path(description='Output 5 file or folder.', path='input_path')
