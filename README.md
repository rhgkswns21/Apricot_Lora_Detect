Apricot Lora Detecter
==========

# How To Use

1. Set the LoRa information.
    - PanID, OwnID, DestID, BW, SF, CH.
2. Set the Check Time Interval.
3. Run the Program or crontap
    - python3 main.py
    - Set the crontap

# Etc.
- Cautions when setting up LoRa information.
  BW    
   3 = 62.5khz    
   4 = 125khz    
   5 = 250khz    
   6 = 500khz    

  CH    
   62.5khz and 125khz = 1 ~ 15 Ch    
   250khz = 1 ~ 7 Ch    
   500khz = 1 ~ 5Ch    

make by mtesNN / KoHanjun
2020.02.17
