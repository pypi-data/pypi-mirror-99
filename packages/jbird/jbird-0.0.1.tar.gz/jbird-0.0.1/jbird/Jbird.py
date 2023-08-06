import os


class Jbird:

    # # path of the data storage
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

    # set variables, create directory and files
    def _prepare(self):

        # create working directory if not exists
        if not os.path.exists(self.path):
            os.mkdir(self.path)


    def j(self):
        print('j')