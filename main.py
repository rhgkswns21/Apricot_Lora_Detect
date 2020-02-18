import time
import datetime

import lora_lib

########## LoRa Data Param & LoRa info ##########
send_param = {'index':0, 'length':0, 'retry':0, 'sum':0, 'data':bytes}
recv_param = {}

LoRa_PanID = 0x0110
LoRa_OwnID = 0x000000
LoRa_DestID = 0x000000

## BW 
## 6 = 500khz
## 5 = 250khz
## 4 = 125khz
## 3 = 62.5khz

LoRa_BW = 6
LoRa_SF = 7
LoRa_CH = 1

Time_Interval = 900

########## Create LORA ##########
LORA = lora_lib.LORA()
result = LORA.LoRa_Create()
if result != 0:
    print(str(datetime.datetime.now()) + '\t' + 'LoRa Create Error.(', result, ')')
    sys.exit()

LORA_Result = lora_lib.LoRaResult()

configParam = lora_lib.LORA_CONFIG_PARAM()
configParam.nodeType = 2
configParam.bw = LoRa_BW
configParam.sf = LoRa_SF
configParam.ch = LoRa_CH
configParam.panID = LoRa_PanID
configParam.ownID = LoRa_OwnID

########## Configration LORA ##########
result = LORA.LoRa_Configration(configParam.nodeType, configParam.bw, configParam.sf, configParam.ch, configParam.panID, configParam.ownID)
if result != 0:
    print(str(datetime.datetime.now()) + '\t' + "LoRa configration error.")
    sys.exit()

########## LORA Recevie Call Back ##########
def recv_call_back(rssi, panID, srcID, payload, length) -> int:
    print(str(datetime.datetime.now()) + '\t' + 'Rx> ', end='')
    for i in range(length):
        print(payload[i].hex() + ' ', end='')
    print('')

LORA.LoRa_Regist_ReceiveCb(recv_call_back)

time_count = 0
sample_count = 0

########## Main Loop ##########
try:
    while True:
        if time_count >= Time_Interval:

            ########## Write Paylod ##########
            if sample_count >= 0xFF:
                print(str(datetime.datetime.now()) + '\t' +'sampling count overflow...')
                sample_count = 0

            time_stamp = (int(time.time()) + 32400)
            command = 160
            end_data = 0

            payload = sample_count.to_bytes(1, 'little') + command.to_bytes(1, 'little') + time_stamp.to_bytes(4, 'little') + end_data.to_bytes(2, 'little')
            
            ########## LoRa Send ##########
            result = LORA.LoRa_Send(configParam.panID, LoRa_DestID, payload, 8)

            ########## Result ##########
            if result == 0:
                print(str(datetime.datetime.now()) + '\t' + 'Tx>', end=' ')
                for i in payload:
                    print('%02X' % (i), end=' ')
                print('')
            elif result == LORA_Result.LORA_NG_NO_ACK:
                print(str(datetime.datetime.now()) + '\t' + 'Send failed(', result,')', ' : No ack received.')
            else:
                print(str(datetime.datetime.now()) + '\t' + 'Send failed(', result,').')
            time_count = 0
            sample_count = sample_count + 1
        
        else:
            time_count = time_count + 1
            time.sleep(1)
    
    LORA.LoRa_Destroy()

except Exception as e:
    print(str(datetime.datetime.now()) + '\t' + e)
    LORA.LoRa_Destroy()
