from io import StringIO

import gevent

DATA = '''29-Dec-17 07:18:43    99      66      12                     
29-Dec-17 07:18:45    99      66      17    MO               
29-Dec-17 07:18:47    99      66      18    MO               
29-Dec-17 07:18:49    99      66      52                     
29-Dec-17 07:18:51    99      66      61    MO               
29-Dec-17 07:18:53    99      66      13    MO               
29-Dec-17 07:18:55    99      66       8    MO               
29-Dec-17 07:18:57    89*     66     201    MO SL            
29-Dec-17 07:18:59    83*     66     200    MO SL            
29-Dec-17 07:19:01    79*     66      18    MO SL       AS   
29-Dec-17 07:19:03    77*     66      30    MO SL       AS   
29-Dec-17 07:19:05    77*     66       8    MO SL       AS   
29-Dec-17 07:19:07    77*     70       8       SL       AS   
29-Dec-17 07:19:09    78*     70      29    MO SL       AS   
29-Dec-17 07:19:11    78*     70      25    MO SL       AS   
29-Dec-17 07:19:13    78*     70       4    MO SL       AS   
29-Dec-17 07:19:15    77*     70       4    MO SL       AS   
29-Dec-17 07:19:17    75*     71       9    MO SL       AS   
29-Dec-17 07:19:19    73*     71       9    MO SL       AS   
N-560    VERSION 1.56.00    CRC:XXXX  SpO2 Limit: 90-100%    PR Limit: 60-170BPM
                             ADULT            0SAT-S 
TIME                 %SpO2   BPM     PA     Status
29-Dec-17 07:19:21    74*     70      11    MO SL       AS   
29-Dec-17 07:19:23    73*     70      36    MO SL       AS   
29-Dec-17 07:19:25    73*     70      44    MO SL       AS   
29-Dec-17 07:19:27    73*     70      12    MO SL       AS   
29-Dec-17 07:19:29   ---     ---     ---    SD          AS   
29-Dec-17 07:19:31   ---     ---     ---    SD          AS   
29-Dec-17 07:19:33   ---     ---     ---    SD          AS   
29-Dec-17 07:19:35   ---     ---     ---    SD          AS   
29-Dec-17 07:19:37   ---     ---     ---    SD          AS   
29-Dec-17 07:19:39   ---     ---     ---    SD          AS   
29-Dec-17 07:19:41   ---     ---     ---    SD          AS   
29-Dec-17 07:19:43   ---     ---     ---    SD          AS   
29-Dec-17 07:19:45   ---     ---     ---    SD          AS   
29-Dec-17 07:19:47   ---     ---     ---    SD          AS   
29-Dec-17 07:19:49   ---     ---     ---    SD          AS   
29-Dec-17 07:19:51   ---     ---     ---    SD          AS   
29-Dec-17 07:19:53   ---     ---     ---    SD          AS   
29-Dec-17 07:19:55   ---     ---     ---    SD          AS   
29-Dec-17 07:19:57   ---     ---     ---    SO          AS   
29-Dec-17 07:19:59   ---     ---     ---    SO               
29-Dec-17 07:20:01   ---     ---     ---    SO               
29-Dec-17 07:20:03   ---     ---     ---    SO               
N-560    VERSION 1.56.00    CRC:XXXX  SpO2 Limit: 90-100%    PR Limit: 60-170BPM
                             ADULT            0SAT-S 
TIME                 %SpO2   BPM     PA     Status
29-Dec-17 07:20:05   ---     ---     ---    SO               
29-Dec-17 07:20:07   ---     ---     ---    SO               
29-Dec-17 07:20:09   ---     ---     ---    SO               
29-Dec-17 07:20:11   ---     ---     ---    SO               
29-Dec-17 07:20:13   ---     ---     ---    SO               
29-Dec-17 07:20:15   ---     ---     ---    SO               
29-Dec-17 07:20:17   ---     ---     ---    SO               
29-Dec-17 07:20:19   ---     ---     ---    SO               
29-Dec-17 07:20:21   ---     ---     ---    SO               
29-Dec-17 07:20:23   ---     ---     ---    SO               
29-Dec-17 07:20:25   ---     ---     ---    SO               
29-Dec-17 07:20:27     0       0     ---    PS               
29-Dec-17 07:20:29     0       0     ---    PS               
29-Dec-17 07:20:31     0       0     ---    PS               
29-Dec-17 07:20:33     0       0     ---    PS               
29-Dec-17 07:20:35     0       0     ---    PS               
29-Dec-17 07:20:37     0       0     ---    PS               
29-Dec-17 07:20:39     0       0     ---    PS               
29-Dec-17 07:20:41     0       0     ---    PS               
29-Dec-17 07:20:43    94     119       5                     
29-Dec-17 07:20:45    94     103       4                     
29-Dec-17 07:20:47    94      92       4                     
N-560    VERSION 1.56.00    CRC:XXXX  SpO2 Limit: 90-100%    PR Limit: 60-170BPM
                             ADULT            0SAT-S 
TIME                 %SpO2   BPM     PA     Status
29-Dec-17 07:20:49    94      91       4    MO               
29-Dec-17 07:20:51    95      88       4    MO               
29-Dec-17 07:20:53    95      83       5                     
29-Dec-17 07:20:55    95      77       4                     
29-Dec-17 07:20:57    95      72       4                     
29-Dec-17 07:20:59    96      70       4                     
29-Dec-17 07:21:01    97      68       5                     
29-Dec-17 07:21:03    97      65       5                     
29-Dec-17 07:21:05    97      63       6                     
29-Dec-17 07:21:07    97      63       5                     
29-Dec-17 07:21:09    97      63       5    MO               
29-Dec-17 07:21:11    96      63       7    MO               
29-Dec-17 07:21:13    96      63     ---    PS                  
'''


class DemoStream:

    def readlines(self):
        while True:
            for line in StringIO(DATA).readlines():
                gevent.sleep(2)
                yield line

