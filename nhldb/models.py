from collections import defaultdict

class BaseType(object):
    __table_name = None

    def __init__(self, session):
        self.session = session

    @property
    def table(self):
        return self.__table_name


class Team(BaseType):
    __table_name = 'team'

    def __init__(self, session):
        super(Team, self).__init__(session)


class Game(BaseType):
    __table_name = 'game'

    def __init__(self, session):
        super(Game, self).__init__(session)

