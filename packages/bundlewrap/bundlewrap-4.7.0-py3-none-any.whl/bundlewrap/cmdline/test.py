from copy import copy
from sys import exit

from ..deps import ItemDependencyLoop
from ..exceptions import FaultUnavailable
from ..itemqueue import ItemTestQueue
from ..metadata import check_for_metadata_conflicts, metadata_to_json
from ..repo import Repository
from ..utils.cmdline import count_items, get_target_nodes
from ..utils.dicts import diff_value, diff_value_text
from ..utils.text import bold, green, mark_for_translation as _, red, yellow
from ..utils.ui import io, QUIT_EVENT


def test_items(nodes, ignore_missing_faults, quiet):
    io.progress_set_total(count_items(nodes))
    for node in nodes:
        if QUIT_EVENT.is_set():
            break
        if not node.items:
            io.stdout(_("{x} {node}  has no items").format(node=bold(node.name), x=yellow("!")))
            continue
        item_queue = ItemTestQueue(node)
        while not QUIT_EVENT.is_set():
            try:
                item = item_queue.pop()
            except KeyError:  # no items left
                break
            try:
                item._test()
            except FaultUnavailable:
                if ignore_missing_faults:
                    io.progress_advance()
                    io.stderr(_("{x} {node}  {bundle}  {item}  ({msg})").format(
                        bundle=bold(item.bundle.name),
                        item=item.id,
                        msg=yellow(_("Fault unavailable")),
                        node=bold(node.name),
                        x=yellow("»"),
                    ))
                else:
                    io.stderr(_("{x} {node}  {bundle}  {item}  missing Fault:").format(
                        bundle=bold(item.bundle.name),
                        item=item.id,
                        node=bold(node.name),
                        x=red("!"),
                    ))
                    raise
            except Exception:
                io.stderr(_("{x} {node}  {bundle}  {item}").format(
                    bundle=bold(item.bundle.name),
                    item=item.id,
                    node=bold(node.name),
                    x=red("!"),
                ))
                raise
            else:
                if item.id.count(":") < 2:
                    # don't count canned actions
                    io.progress_advance()
                if not quiet:
                    io.stdout("{x} {node}  {bundle}  {item}".format(
                        bundle=bold(item.bundle.name),
                        item=item.id,
                        node=bold(node.name),
                        x=green("✓"),
                    ))
        if item_queue.items_with_deps and not QUIT_EVENT.is_set():
            raise ItemDependencyLoop(item_queue.items_with_deps)
    io.progress_set_total(0)


def test_subgroup_loops(repo, quiet):
    checked_groups = []
    for group in repo.groups:
        if QUIT_EVENT.is_set():
            break
        if group in checked_groups:
            continue
        with io.job(_("{group}  checking for subgroup loops").format(group=bold(group.name))):
            checked_groups.extend(group.subgroups)  # the subgroups property has the check built in
        if not quiet:
            io.stdout(_("{x} {group}  has no subgroup loops").format(
                x=green("✓"),
                group=bold(group.name),
            ))


def test_metadata_conflicts(node, quiet):
    with io.job(_("{node}  checking for metadata conflicts").format(node=bold(node.name))):
        check_for_metadata_conflicts(node)
    if not quiet:
        io.stdout(_("{x} {node}  has no metadata conflicts").format(
            x=green("✓"),
            node=bold(node.name),
        ))


def test_orphaned_bundles(repo):
    orphaned_bundles = set(repo.bundle_names)
    for node in repo.nodes:
        if QUIT_EVENT.is_set():
            break
        for bundle in node.bundles:
            if QUIT_EVENT.is_set():
                break
            orphaned_bundles.discard(bundle.name)
    for bundle in sorted(orphaned_bundles):
        io.stderr(_("{x} {bundle}  is an unused bundle").format(
            bundle=bold(bundle),
            x=red("✘"),
        ))
    if orphaned_bundles:
        exit(1)


def test_empty_groups(repo):
    empty_groups = set()
    for group in repo.groups:
        if QUIT_EVENT.is_set():
            break
        if not group.nodes:
            empty_groups.add(group)
    for group in sorted(empty_groups):
        io.stderr(_("{x} {group}  is an empty group").format(
            group=bold(group),
            x=red("✘"),
        ))
    if empty_groups:
        exit(1)


def test_determinism(repo, nodes, iterations_config, iterations_metadata, quiet):
    """
    Generate configuration a couple of times for every node and see if
    anything changes between iterations
    """
    first_run_nodes = {}
    io.progress_set_total(len(nodes) * (iterations_config + iterations_metadata))

    iter_config_todo = iterations_config
    iter_metadata_todo = iterations_metadata

    while iter_config_todo > 0 or iter_metadata_todo > 0:
        if QUIT_EVENT.is_set():
            break

        iteration_repo = Repository(repo.path)

        iteration_nodes = [iteration_repo.get_node(node.name) for node in nodes]
        for node in iteration_nodes:
            if QUIT_EVENT.is_set():
                break

            first_run_nodes.setdefault(node.name, node)

            if iter_config_todo > 0:
                with io.job(_("{node}  generating configuration ({i}/{n})").format(
                    i=iterations_config - iter_config_todo,
                    n=iterations_config,
                    node=bold(node.name),
                )):
                    result = node.hash()
                if first_run_nodes[node.name].hash() != result:
                    io.stderr(_(
                        "{x} Configuration for node {node} changed when generated repeatedly"
                    ).format(node=node.name, x=red("✘")))
                    heisenitems = set(node.items).symmetric_difference(
                        set(first_run_nodes[node.name].items))
                    if heisenitems:
                        io.stderr(_(
                            "{x} These items appeared or disappeared on {node} between runs:\n"
                            "\t{items}"
                        ).format(
                            x=red("✘"),
                            node=node.name,
                            items="\n\t".join(sorted({item.id for item in heisenitems})),
                        ))
                        exit(1)
                    for item in node.items:
                        previous_item = first_run_nodes[node.name].get_item(item.id)
                        if item.ITEM_TYPE_NAME == "action":
                            continue  # actions don't hash :'(
                        if item.hash() != previous_item.hash():
                            current_cdict = item.display_on_create(item.cdict().copy())
                            current_cdict_keys = set(current_cdict.keys())
                            previous_cdict = previous_item.display_on_create(previous_item.cdict().copy())
                            previous_cdict_keys = set(previous_cdict.keys())
                            assert current_cdict_keys == previous_cdict_keys, \
                                "cdict mismatch: " + str(
                                    current_cdict_keys.symmetric_difference(previous_cdict_keys)
                                )
                            output = _("{x} {node}  {item} changed:\n").format(
                                x=red("✘"),
                                node=bold(node.name),
                                item=item.id,
                            )
                            diff = "\n"
                            for key in sorted(current_cdict_keys):
                                if current_cdict[key] != previous_cdict[key]:
                                    diff += diff_value(
                                        key,
                                        current_cdict[key],
                                        previous_cdict[key],
                                    ) + "\n"
                            for line in diff.splitlines():
                                output += "{x} {line}\n".format(
                                    line=line,
                                    x=red("│"),
                                )
                            output += red("╵")
                            io.stderr(output)
                    exit(1)
                io.progress_advance()

            if iter_metadata_todo > 0:
                with io.job(_("{node}  generating metadata ({i}/{n})").format(
                    i=iterations_metadata - iter_metadata_todo,
                    n=iterations_metadata,
                    node=bold(node.name),
                )):
                    result = node.metadata_hash()
                if first_run_nodes[node.name].metadata_hash() != result:
                    io.stderr(_(
                        "{x} Metadata for node {node} changed when generated repeatedly"
                    ).format(node=bold(node.name), x=red("✘")))
                    previous_json = metadata_to_json(first_run_nodes[node.name].metadata)
                    current_json = metadata_to_json(node.metadata)
                    io.stderr(diff_value_text("", previous_json, current_json))
                    exit(1)
                io.progress_advance()

        if iter_config_todo > 0:
            iter_config_todo -= 1
        if iter_metadata_todo > 0:
            iter_metadata_todo -= 1

    io.progress_set_total(0)
    if not quiet:
        if iterations_config > 0:
            io.stdout(_("{x} Configuration remained the same after being generated {n} times").format(
                n=iterations_config,
                x=green("✓"),
            ))
        if iterations_metadata > 0:
            io.stdout(_("{x} Metadata remained the same after being generated {n} times").format(
                n=iterations_metadata,
                x=green("✓"),
            ))


def test_reactor_provides(repo, nodes, quiet):
    repo._verify_reactor_provides = True
    for node in nodes:
        if QUIT_EVENT.is_set():
            break
        node.metadata.get(())
    else:
        if not quiet:
            io.stdout(_("{x} No reactors violated their declared keys").format(
                x=green("✓"),
            ))


def bw_test(repo, args):
    options_selected = (
        args['determinism_config'] > 1 or
        args['determinism_metadata'] > 1 or
        args['hooks_node'] or
        args['hooks_repo'] or
        args['items'] or
        args['metadata_conflicts'] or
        args['orphaned_bundles'] or
        args['reactor_provides'] or
        args['empty_groups'] or
        args['subgroup_loops']
    )
    if args['targets']:
        nodes = get_target_nodes(repo, args['targets'])
        if not options_selected:
            args['hooks_node'] = True
            args['items'] = True
            args['metadata_conflicts'] = True
            args['metadata_keys'] = True
            args['reactor_provides'] = True
    else:
        nodes = copy(list(repo.nodes))
        if not options_selected:
            args['hooks_node'] = True
            args['hooks_repo'] = True
            args['items'] = True
            args['metadata_conflicts'] = True
            args['metadata_keys'] = True
            args['reactor_provides'] = True
            args['subgroup_loops'] = True

    if args['reactor_provides'] and not QUIT_EVENT.is_set():
        test_reactor_provides(repo, nodes, args['quiet'])

    if args['subgroup_loops'] and not QUIT_EVENT.is_set():
        test_subgroup_loops(repo, args['quiet'])

    if args['empty_groups'] and not QUIT_EVENT.is_set():
        test_empty_groups(repo)

    if args['orphaned_bundles'] and not QUIT_EVENT.is_set():
        test_orphaned_bundles(repo)

    if args['metadata_conflicts'] and not QUIT_EVENT.is_set():
        io.progress_set_total(len(nodes))
        for node in nodes:
            if QUIT_EVENT.is_set():
                break
            test_metadata_conflicts(node, args['quiet'])
            io.progress_advance()
        io.progress_set_total(0)

    if args['items']:
        test_items(nodes, args['ignore_missing_faults'], args['quiet'])

    if (
        (args['determinism_config'] > 1 or args['determinism_metadata'] > 1) and
        not QUIT_EVENT.is_set()
    ):
        test_determinism(
            repo,
            nodes,
            args['determinism_config'],
            args['determinism_metadata'],
            args['quiet'],
        )

    if args['hooks_node'] and not QUIT_EVENT.is_set():
        io.progress_set_total(len(nodes))
        for node in nodes:
            if QUIT_EVENT.is_set():
                break
            repo.hooks.test_node(repo, node)
            io.progress_advance()
        io.progress_set_total(0)

    if args['hooks_repo'] and not QUIT_EVENT.is_set():
        repo.hooks.test(repo)
