# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" aiohttp Framework Adapter
"""
import sys

from ....rules_callbacks import BindingAccessorProvideData


class AioHTTPFrameworkAdapter(object):

    def instrumentation_callbacks(self, runner, storage):
        if sys.version_info[0] < 3:
            return []
        return [
            BindingAccessorProvideData.from_rule_dict({
                "name": "ecosystem_request_aiohttp",
                "data": {
                    "values": [
                        ["pre", [
                            ["server.request.client_ip", "#.client_ip"],
                            ["server.request.method", "#.method"],
                            ["server.request.uri.raw", "#.request_uri"],
                            ["server.request.headers.no_cookies", "#.headers_no_cookies"],
                            ["server.request.cookies", "#.cookies_params"],
                            ["server.request.query", "#.query_params"],
                            ["server.request.body", "#.body_params"],
                            ["server.request.body.raw", "#.body"],
                            ["server.request.path_params", "#.view_params"],
                        ]]
                    ]
                },
                "rulespack_id": "ecosystem/transport",
                "block": True,
                "hookpoint": {
                    "klass": "sqreen.instrumentation.middlewares.aiohttp_middleware::AioHTTPMiddleware",
                    "method": "handle",
                    "strategy": "aiohttp_hook",
                },
                "priority": 100,
            }, runner, storage),
            BindingAccessorProvideData.from_rule_dict({
                "name": "ecosystem_install_aiohttp_middleware",
                "data": {
                    "values": []
                },
                "rulespack_id": "ecosystem/transport",
                "block": False,
                "hookpoint": {
                    "klass": "aiohttp.web::Application",
                    "method": "freeze",
                    "strategy": "aiohttp_install"
                },
                "priority": 40,
            }, runner, storage),
            BindingAccessorProvideData.from_rule_dict({
                "name": "ecosystem_patch_asyncio_event_loop",
                "data": {
                    "values": []
                },
                "rulespack_id": "ecosystem/transport",
                "block": False,
                "hookpoint": {
                    "klass": "asyncio.base_events",
                    "method": "BaseEventLoop",
                    "strategy": "async_event_loop"
                },
                "priority": 30,
            }, runner, storage),
            BindingAccessorProvideData.from_rule_dict({
                "name": "ecosystem_patch_uvloop_event_loop",
                "data": {
                    "values": []
                },
                "rulespack_id": "ecosystem/transport",
                "block": False,
                "hookpoint": {
                    "klass": "uvloop",
                    "method": "Loop",
                    "strategy": "async_event_loop"
                },
                "priority": 30,
            }, runner, storage),
        ]
