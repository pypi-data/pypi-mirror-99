
from tendril.structures.base import StructureBase


class BasicContainer(StructureBase):
    def __init__(self, owner=None, vctx=None):
        self._contents = []
        super(BasicContainer, self).__init__(owner, vctx)

    def insert(self, item):
        self._contents.append(item)

    def contents(self):
        return self._contents

    def json(self):
        return [entity.json() for entity in self.contents()]


class GroupsAwareContainerMixin(object):
    def __init__(self):
        self._groups = []

    def insert(self, item):
        # TODO Ensure item is GroupsAware, if not recast and set to Default
        super(GroupsAwareContainerMixin, self).insert(item)

    def contents(self):
        # TODO Return List of Contents filtered by group
        return super(GroupsAwareContainerMixin, self).contents()


# class IndexedContainer(StructureBase):
#     def __init__(self, context):
#         self._contents = {}
#         super(IndexedContainer, self).__init__(context)
#
#     def insert(self, item, idx):
#         if idx in self._contents.keys():
#             raise KeyError()
#         self._contents[idx] = item
#
#     def contents(self):
#         # TODO Return List of Values Ordered by Key
#         return self._contents
