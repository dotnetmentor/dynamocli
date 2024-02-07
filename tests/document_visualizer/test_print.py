import pytest
from unittest.mock import Mock
from rich.console import Console

from src.document_visualizer import DocumentVisualizer


@pytest.fixture(scope='function')
def console():
    mock_console = Mock(spec=Console)
    yield mock_console


@pytest.fixture(scope='function')
def dataset():
    items = [
        {'capacity': 12, 'pk': 'test#room',
            'room': 'Meeting Room 1', 'sk': 'test#room#2'},
        {'capacity': 4, 'pk': 'test#room', 'name': 'Kitchen', 'sk': 'test#room#12'},
        {'capacity': 4, 'pk': 'test#room', 'room': 'Office 2', 'sk': 'test#room#13'}]
    yield items


@pytest.fixture(scope='function')
def colors():
    yield ["turquoise2",
           "green1",
           "spring_green2",
           "spring_green1",
           "medium_spring_green",
           "cyan2"]


def test_print_items_calls_print_table(console: Console, dataset, colors):
    visualizer = DocumentVisualizer(console=console)
    visualizer.print_items(dataset)
    console.print.assert_called_once()
    args, _ = console.print.call_args
    tree = args[0]
    assert tree.label == 'Items'
    children = tree.children
    assert len(children) == 3
    for i, child in enumerate(children):
        assert child.label == str(i)
        assert len(child.children) == 4
        for j, grandchild in enumerate(child.children):
            assert grandchild.label.startswith(
                '[{}]'.format(colors[j % len(colors)-1]))
