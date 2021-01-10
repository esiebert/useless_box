# pylint: disable=[missing-module-docstring,missing-function-docstring,invalid-name]
from unittest.mock import patch, mock_open
from consumer.output_stream import FileOutputStream


def test_file_output_stream():

    with patch('builtins.open', mock_open()) as m:
        file_output_stream = FileOutputStream(
            filepath='/mocked/file.txt',
        )
        file_output_stream.write("a", "b", "c")

    m.assert_called_once_with('/mocked/file.txt', 'a')
    handle = m()
    handle.write.assert_called_once_with('a,b,c\n')
