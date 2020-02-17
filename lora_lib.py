from ctypes import *

# liblora = cdll.LoadLibrary('build/lib.linux-armv6l-3.5/liblora.cpython-35m-arm-linux-gnueabihf.so')
liblora = cdll.LoadLibrary('./liblora.so')

class LoRaResult():
	LORA_SUCCESS				= 0
	LORA_ERR_INVALID_HANDLE	    = -1		# 無効なインスタンスハンドル
	LORA_ERR_INVALID_ARG		= -2		# 引数不正
	LORA_ERR_TX_BUSY			= -3		# LoRa送信実行中（レスポンス待ち）
	LORA_ERR_RX_BUSY			= -4		# LoRa受信中
	LORA_ERR_RX_OVERFLOW		= -5		# 受信バッファオーバーフロー
	LORA_ERR_RX_TIMEOUT		    = -6		# LoRa受信タイムアウト
	LORA_ERR_NO_RESPONSE		= -7		# LoRa未応答
	LORA_ERR_READ_CONFIG		= -8		# LoRaコンフィグレーションファイルの読み込みエラー

	LORA_ERR_INTERNAL		    = -100

	# LoRa送信レスポンスNG
	LORA_NG_NO_ACK			    = 1		    # 送信レスポンスNG：ACK未受信
	LORA_NG_DETECT_CS		    = 2		    # 送信レスポンスNG：キャリアセンス検出
	LORA_NG_TX_ERROR			= 3		    # 送信レスポンスNG：送信異常
	LORA_NG_CONFIG_OPT	    	= 4	    	# コンフィグレスポンスNG：オプション値異常
	LORA_NG_RESPONSE			= 5			# スポンスNG：その他


# LoRaコンフィグレーション・パラメータ
class LORA_CONFIG_PARAM(Structure):
    __fields__ = [
        ('nodeType', c_int),        # ノード種別 1:Coordinator, 2:EndDevice
        ('bw', c_int),              # 帯域幅
        ('sf', c_int),              # 拡散率
        ('ch', c_int),              # 無線チャンネル
        ('panID', c_int),           # 自PANID
        ('ownID', c_int)]           # 自ネットワークアドレス

class LORA:

    # 使用するAPIの引数と戻り値の登録

    #  インスタンス生成
    #  int LibLoRa_Create(void);
    liblora.LibLoRa_Create.argtypes = (None)    # 引数の型
    liblora.LibLoRa_Create.restype = c_int      # 返り値の型

    # インスタンス開放
    # void LibLoRa_Destroy(int handle);
    # liblora.LibLoRa_Destroy.argtypes = (c_int)  # 引数の型
    liblora.LibLoRa_Destroy.restype = None      # 返り値の型

    # コンフィグレーション実行
    # int LibLoRa_Configration(int handle, int nodeType, int bw, int sf, int ch, int panID, int ownID);
    liblora.LibLoRa_Configration.argtypes = (c_int, c_int, c_int, c_int, c_int, c_int, c_int)   # 引数の型
    liblora.LibLoRa_Configration.restype = c_int                                                # 返り値の型

    # パラメータファイルからコンフィグレーション実行
    # int LibLoRa_ConfigrationFromFile(int handle, char *path);
    # liblora.LibLoRa_ConfigrationFromFile.argtypes = (c_int, c_wchar_p)  # 引数の型
    # liblora.LibLoRa_ConfigrationFromFile.restype = c_int                # 返り値の型

    # 送信実行
    # int LibLoRa_Send(int handle, int destOwnID, char *paylod, int length);
    cptr = POINTER(c_char)  # charポインタ型として型を定義しておく
    liblora.LibLoRa_Send.argtypes = (c_int, c_int, c_int, cptr, c_int) # 引数の型
    liblora.LibLoRa_Send.restype = c_int                        # 返り値の型

    # 受信データ取得
    # int LibLoRa_Receive(int handle, int *rssi, int *panID, int *ownID, char *payload/*[LORA_PAYLOAD_SIZE]*/, int *length);
    iptr = POINTER(c_int)  # intポインタ型として型を定義しておく
    liblora.LibLoRa_Receive.argtypes = (c_int, iptr, iptr, iptr, cptr, iptr)    # 引数の型
    liblora.LibLoRa_Receive.restype = c_int                                     # 返り値の型

    # Recv Call Back
    # LoRa_Recv_Call_Back = CFUNCTYPE(None, c_int, c_int, c_int, POINTER(c_char), c_int)
    LoRa_Recv_Call_Back = CFUNCTYPE(None, c_int, c_int, c_int, POINTER(c_char), c_int)
    liblora.LibLoRa_Regist_ReceiveCb.argtypes = (c_int, LoRa_Recv_Call_Back, c_int)
    liblora.LibLoRa_Regist_ReceiveCb.restype = c_int

    # Send Call Back
    # LoRa_Send_Call_Back = CFUNCTYPE(c_int, POINTER(c_int), POINTER(c_int), POINTER(c_char), POINTER(c_int), c_int)
    LoRa_Send_Call_Back = CFUNCTYPE(c_int, POINTER(c_int), POINTER(c_int), POINTER(c_char), POINTER(c_int), c_int)
    liblora.LibLoRa_SendCb.argtypes = (c_int, LoRa_Send_Call_Back, c_int, c_int)
    liblora.LibLoRa_SendCb.restype = c_int

    handle = 0

    RX_rssi = 0
    RX_panID = 0
    RX_ownID = 0
    RX_length = 0
    RX_payload = 0
    MAX_LORA_PAYLOAD_SIZE = 50

    rx_call_back = None
    tx_call_back = None

    def __init__(self):
        super().__init__()

    def __call__(self, *args, **kwargs):
        print('call')

    def LoRa_Create(self) -> int:
        self.handle = liblora.LibLoRa_Create()
        if self.handle == 0:
            print('Create Error.')
            return -1

        return 0

    def LoRa_Destroy(self):
        liblora.LibLoRa_Destroy(c_int(self.handle))
    
    def LoRa_Configration(self, nodeType, bw, sf, ch, panID, ownID) -> int:
        err = liblora.LibLoRa_Configration(self.handle, nodeType, bw, sf, ch, panID, ownID)
        return err
    
    def LoRa_Receive(self) -> int:
        rssi = c_int(0)
        panID = c_int(0)
        ownID = c_int(0)
        length = c_int(0)
        payload = bytes(self.MAX_LORA_PAYLOAD_SIZE)

        err = liblora.LibLoRa_Receive(self.handle, byref(rssi), byref(panID), byref(ownID), payload, byref(length))

        self.RX_rssi = rssi.value-0x10000
        self.RX_panID = panID.value
        self.RX_ownID = ownID.value
        self.RX_length = length.value
        self.RX_payload = payload
        return err
    
    def LoRa_Send(self, panID, destID, payload, length) -> int:
        err = liblora.LibLoRa_Send(self.handle, panID, destID, payload, length)
        return err

    def LoRa_Wait_Response(self) -> int:
        err = liblora.LibLoRa_Wait_Response(c_int(self.handle))
        return err

    def LoRa_Regist_ReceiveCb(self, func) -> int:
        point_func = self.LoRa_Recv_Call_Back(func)
        cast(point_func, POINTER(c_int))
        err = liblora.LibLoRa_Regist_ReceiveCb(self.handle, point_func, 0)
        return err
    
    def LoRa_SendCb(self, func, interval) -> int:
        point_func = self.LoRa_Send_Call_Back(func)
        cast(point_func, POINTER(c_int))
        err = liblora.LibLoRa_SendCb(self.handle, point_func, interval, 0)
        return err
