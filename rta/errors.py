
import traceback

class Errors(object):
    """ class hosts error code constants """
    # general errors
    UNKNOWN_ERROR = 1
    FILE_NOT_EXIST = 2
    FILE_EXIST = 3
    UNDEFINED_METHOD = 4

    NETWORK_ERROR = 100
    NETWORK_400_ERROR = 101

    INDEX_RANGE_ERROR = 200
    INVALID_DAM_TYPE = 201

    STOCK_SYMBOL_ERROR = 300
    STOCK_PARSING_ERROR = 301

    #tickFeeder
    FEEDER_INVALID_ERROR = 600
    SYMBOL_EXIST = 601
    INVALID_TYPE = 602
    SYMBOL_NOT_IN_SOURCE = 604
    FEEDER_TIMEOUT = 605

    #trading error
    INVALID_ACCOUNT = 901

    #outputSaver
    TABLENAME_NOT_SET = 1300
    TABLENAME_ALREADY_SET = 1301
    INVALID_SAVER_NAME = 1302

class UfException(Exception):

    def __init__(self, error, errorMsg):
        """ constructor  """
        super(UfException, self).__init__()
        self.__error = error
        self.__errorMsg = errorMsg

    def __str__(self):
        """ string """
        return repr(self.__errorMsg)

    def getCode(self):
        """ accessor """
        return self.__error

    def getMsg(self):
        """ accessor """
        return "%s: %s" % (self.__errorMsg, traceback.format_exc(5))
