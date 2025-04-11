from asyncio import Semaphore

from src.clients.web_driver_client.schemas import VmHostConfig, VmHosts, WebConfig

config = WebConfig(
    hosts=VmHosts(
        vm_list=[
            VmHostConfig(
                url="http://remote_vm_host:4444",
                description="",
                max_sessions=Semaphore(16),
            ),
            VmHostConfig(
                url="http://remote_vm_host2:4444",
                description="",
                max_sessions=Semaphore(1),
            ),
        ],
        localhost=VmHostConfig(
            url="http://host.docker.internal:4444",
            description="Local Selenium standalone",
            max_sessions=Semaphore(8),
        ),
    ),
    capabilities={
        "browserName": "chrome",
        "pageLoadStrategy": "normal",
        "goog:chromeOptions": {"extensions": [], "args": []},
    },
)
