def pytest_itemcollected(item):
    marker = item.get_closest_marker("display_name")
    if marker:
        item._nodeid = marker.args[0]
