#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pop.hub


def start():
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="doc")
    hub.pop.sub.add(dyne_name="tree")

    hub.pop.config.load(["pop_doc", "pop_tree", "rend"], cli="pop_doc")

    ref = hub.OPT.pop_doc.ref
    split = ref.split(".")
    dyne = split[0]

    if not hasattr(hub, dyne):
        hub.pop.sub.add(dyne_name=dyne)
        should_recurse = len(split) > 3 and not hasattr(hub, ref)
        hub.pop.sub.load_subdirs(getattr(hub, dyne), recurse=should_recurse)

    tree = hub.tree.init.traverse()
    refs = hub.tree.init.refs(tree)

    if ref in refs:
        ret = refs[ref]
    else:
        try:
            ret = tree
            for r in split:
                ret = ret[r]
        except KeyError:
            ret = getattr(hub, ref)

    if not ret:
        raise KeyError(f"Reference does not exist on the hub: {ref}")

    print(hub.output[hub.OPT.rend.output].display(ret))
