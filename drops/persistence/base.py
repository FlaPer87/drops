class StoreBase(object):

    def get(self, col, uuid, **kwargs):
        pass

    def upsert(self, col, uuid, **kwargs):
        pass

    def delete(self, col, uuid, **kwargs):
        pass
