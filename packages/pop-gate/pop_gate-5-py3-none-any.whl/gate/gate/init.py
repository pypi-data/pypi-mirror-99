import json
from typing import List, Dict, Any


def __init__(hub):
    hub.pop.sub.add(dyne_name="tree")
    hub.pop.sub.load_subdirs(hub.gate, recurse=True)


def cli(hub):
    hub.pop.config.load(["gate"], cli="gate")
    hub.pop.loop.create()
    coro = hub.gate.init.start(
        gate_server=hub.OPT.gate.server,
        host=hub.OPT.gate.host,
        port=hub.OPT.gate.port,
        matcher_plugin=hub.OPT.gate.matcher,
        prefix=hub.OPT.gate.prefix,
        refs=hub.OPT.gate.refs,
    )
    hub.pop.Loop.run_until_complete(coro)


async def start(
    hub,
    gate_server: str,
    host: str,
    port: int,
    matcher_plugin: str,
    prefix: str,
    refs: List[str],
):
    return await hub.gate.srv[gate_server].start(
        host=host, port=port, matcher_plugin=matcher_plugin, prefix=prefix, refs=refs
    )


async def tree(
    hub, prefix: str = None, refs: List[str] = None, matcher_plugin: str = None
) -> Dict[str, Any]:
    """
    Get details of all references that are exposed through the gate API
    """
    if prefix is None:
        prefix = hub.OPT.gate.prefix
    if matcher_plugin is None:
        matcher_plugin = hub.OPT.gate.matcher
    if refs is None:
        refs = hub.OPT.gate.refs

    _tree: Dict[str, Any] = hub.tree.init.traverse()

    def _get_ref(t: Dict[str, Any]):
        rf = t.get("ref")
        if (
            rf
            and isinstance(rf, str)
            and hub.gate.matcher[matcher_plugin].match(
                t["ref"], prefix=prefix, refs=refs
            )
        ):
            # This item has a ref and is available to the api
            return t
        else:
            r = {}
            for k, v in t.items():
                if isinstance(v, Dict):
                    sub_ref = _get_ref(v)
                    if sub_ref:
                        r[k] = sub_ref
            return r

    ret = _get_ref(_tree)

    return json.loads(hub.output.json.display(ret))


async def stop(hub, gate_server: str):
    hub.log.debug("Shutting down gate server")
    return await hub.gate.srv[gate_server].stop()


async def join(hub, gate_server):
    return await hub.gate.srv[gate_server].join()


async def test(hub, *args, **kwargs):
    """
    The test function for gate
    """
    return {"args": args, "kwargs": kwargs}
