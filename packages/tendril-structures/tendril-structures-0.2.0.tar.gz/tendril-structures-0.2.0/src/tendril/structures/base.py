

from tendril.validation.base import ValidatableBase


class StructureBase(ValidatableBase):
    def __init__(self, owner=None, vctx=None):
        self._owner = owner
        self._defined = False
        super(StructureBase, self).__init__(vctx)

    def insert(self, *args, **kwargs):
        raise NotImplementedError

    def contents(self):
        # Return immediate list of children
        raise NotImplementedError

    def flattened_contents(self):
        # TODO Generate and return BOM-like Object
        raise NotImplementedError

    def structured_contents(self):
        return {
            self.contents()
        }

    def define(self):
        self._defined = True

    def _validate(self):
        pass
