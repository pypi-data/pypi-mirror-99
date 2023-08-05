__version__ = "0.0.1"

'''
////////////////////////////////////////////////////////////
//  Ver.0.0.1
////////////////////////////////////////////////////////////
●初版
'''
from acapy import acaplib2

class AcaPy():
    """description of class"""

    # クラス変数
    OK									= acaplib2.ACL_RTN_OK		# エラーなし
    ERROR							    = acaplib2.ACL_RTN_ERROR	# エラーあり

    def __init__(self, board_id = 0, ch = 1):
        '''デバイスの初期化
        board_no: ボード番号
        ch      : チャンネル番号        
        '''
        # ボード情報の取得
        ret, bdInfo = acaplib2.AcapGetBoardInfoEx()

        board_index = None
        self.__hHandle = acaplib2.INVALID_HANDLE_VALUE
        self.__ch = None
        self.__is_opened = False

        boardnum = bdInfo.nBoardNum
        if boardnum == 0:
            boardnum = 1 # Virtualを許容するため

        # 指定されたボード番号の検索
        for i in range(boardnum):
            if board_id == bdInfo.boardIndex[i].nBoardID:
                board_index = bdInfo.boardIndex[i]
                break

        if board_index is None:
            # 指定されたボード番号が見つからなかったとき
            return

        # チャンネル番号の確認
        if ch < 0 or ch > bdInfo.boardIndex[0].nChannelNum:
            return

        # プロパティの値を取得
        self.__board_id = board_id
        self.__board_name = board_index.pBoardName

        # ボードオープン
        self.__hHandle = acaplib2.AcapOpen(board_index.pBoardName, board_index.nBoardID, ch)
        self.__ch = ch

        self.__is_opened = True

        self.__width = 0

    def __del__(self):
        if self.__hHandle != acaplib2.INVALID_HANDLE_VALUE:
            acaplib2.AcapClose(self.__hHandle, self.__ch)
        print("AcapClose")

