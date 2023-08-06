#!/usr/bin/python
from ntnx_api.client import PrismApi


def test_api_connection_pe():
    """Test connectivity to prism element"""
    api_test = PrismApi(ip_address='192.168.1.7', username='admin', password='uwpOF!1pfQEbTWHWv*kv0HGLNL&QD^4u').test()
    assert api_test


def test_api_connection_pc():
    """Test connectivity to prism central"""
    api_test = PrismApi(ip_address='192.168.1.44', username='admin', password='fUUif4l0CF!iPVv2mpE6wbT9&Rf5tw').test()
    assert api_test
