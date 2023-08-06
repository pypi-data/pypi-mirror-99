from shlex import quote

from bundlewrap.exceptions import BundleError
from bundlewrap.items import Item
from bundlewrap.utils.text import mark_for_translation as _


def svc_start(node, svcname):
    return node.run("initctl start --no-wait -- {}".format(quote(svcname)), may_fail=True)


def svc_running(node, svcname):
    result = node.run("initctl status -- {}".format(quote(svcname)), may_fail=True)
    if result.return_code != 0:
        return False
    return " start/" in result.stdout_text


def svc_stop(node, svcname):
    return node.run("initctl stop --no-wait -- {}".format(quote(svcname)), may_fail=True)


class SvcUpstart(Item):
    """
    A service managed by Upstart.
    """
    BUNDLE_ATTRIBUTE_NAME = "svc_upstart"
    ITEM_ATTRIBUTES = {
        'running': True,
    }
    ITEM_TYPE_NAME = "svc_upstart"

    def __repr__(self):
        return "<SvcUpstart name:{} running:{}>".format(
            self.name,
            self.attributes['running'],
        )

    def fix(self, status):
        if self.attributes['running'] is False:
            svc_stop(self.node, self.name)
        else:
            svc_start(self.node, self.name)

    def get_canned_actions(self):
        return {
            'stop': {
                'command': "stop {0}".format(self.name),
                'needed_by': {self.id},
            },
            'stopstart': {
                'command': "stop {0} && start {0}".format(self.name),
                'needs': {self.id},
            },
            'restart': {
                'command': "restart {}".format(self.name),
                'needs': {
                    # make sure we don't restart and stopstart simultaneously
                    f"{self.id}:stopstart",
                    # with only the dep on stopstart, we might still end
                    # up reloading if the service itself is skipped
                    # because the stopstart action has cascade_skip False
                    self.id,
                },
            },
            'reload': {
                'command': "reload {}".format(self.name),
                'needs': {
                    # make sure we don't restart and reload simultaneously
                    f"{self.id}:restart",
                    # with only the dep on restart, we might still end
                    # up reloading if the service itself is skipped
                    # because the restart action has cascade_skip False
                    self.id,
                },
            },
        }

    def sdict(self):
        return {'running': svc_running(self.node, self.name)}

    @classmethod
    def validate_attributes(cls, bundle, item_id, attributes):
        if not isinstance(attributes.get('running', True), bool):
            raise BundleError(_(
                "expected boolean for 'running' on {item} in bundle '{bundle}'"
            ).format(
                bundle=bundle.name,
                item=item_id,
            ))
