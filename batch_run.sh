#!/bin/bash

symbols=(
    'MSFT' 'AAPL' 'NVDA' 'AMZN' 'META' 'GOOG' 'TSLA' 'AVGO' # 8 giants
    'NRG' 'CEG' 'VST' 'NNE' 'LBRT' 'LEU' 'SMR' 'OKLO' # nuclear power
    'INOD' 'PLTR' 'VERI' 'UPST' 'SOUN' 'GDS' 'BBAI' 'CIFR' # AI
    'BE' 'ENPH' 'SES' 'VTS' 'FSLR' 'AES' 'PLUG' 'TMDE' 'FLNC' 'JKS' 'ETN' 'NVT' 'EOSE' 'GEV' 'NVTS' 'QS' 'ARM' # AI electric power
    'INTC' 'PXLW' 'APH' 'ALAB' 'QCOM' 'AMSC' 'AMAT' 'VRT' 'DELL' 'MRVL' 'TSM' 'NOK' 'ON' 'KLAC' 'ASML' 'AMD' 'SMCI' 'CRDO' 'LAES' 'CBRS' 'WOLF' 'BNC' 'POET' # semiconducter
    'CORZ' 'CIFR' 'COHR' 'SEI' 'TSEM' 'RIOT' 'CRWV' 'LITE' # Leopold Aschenbrenner
    'BTBT' 'BVC' 'NAKA' 'FIG' 'CRCL' 'GEMI' 'XYZ' 'TRON' 'HOOD' 'BKKT' 'MSTR' 'ABTC' 'HUT' 'MARA' 'COIN' 'APLD' 'IREN' 'BLSH' 'BMNR' 'BTCS' 'BTBT' # stablecoin, cryptocoin, itcoin
    'RGTI' 'QUBT' 'IONQ' 'ARQQ' 'QMCO' 'QBTS' # quantum 
    'SHOP' 'VZ' 'S' 'CRWD' 'SE' 'SNOW' 'SOFI' 'DXYZ' 'DJT' 'GME' 'BKKT' 'SPOT' 'RUM' 'APP' 'GME' 'RBLX' 'OPEN' # software
    'ANET' 'PATH' 'IOT' 'GTLB' 'DASH' 'ORCL' 'NMAX' 'CRM' 'MNDY' 'MDB' 'DDOG' 'DBX' 'PANW' 'RDDT' 'TWLO' 'U' 'SNPS' # software
    'DOCN' 'PDYN' 'FSLY' 'KEEL' 'CLSK' 'GAME' 'AIIO' # software
    'RKLB' 'GE' 'HEI' 'SIDU' 'MNTS' 'RCAT' 'JOBY' 'BWXT' 'GE' 'EH' 'DFNS' 'AIRO' 'UMAC' 'VOYG' 'KULR' 'ACHR' # rocket
    'LLY' 'NVO' 'VKTX' 'CRSP' 'ATNM' 'NCNA' 'RGC' 'WGS' 'GENB' 'HIMS' 'CELC' 'BMY' 'DRUG' 'ILMN' 'ELV' 'PFE' 'MRNA' # medical
    'NVO' 'ATNM' 'NVAX' 'RXRX' 'ONC' 'CRSP' 'VKTX' 'CAI' 'MDLN' 'LUNR' 'PSTV' # medical
    'BIDU' 'JD' 'PDD' 'EDU' 'CHA' 'NIO' 'XPEV' 'LI' 'HSAI' 'GDS' 'PONY' 'BABA' 'KC' 'BILI' 'WRD' 'NIU' # China
    'MU' 'SNDK' 'STX' 'WDC' 'SIMO' 'RMBS' # storage
    'MP' 'LAC' 'CRML' 'FCX' # metal
    'SATS' 'ASTS' 'HPE' 'ONDS' 'UI' 'AAOI' # communication
    'SPOT' 'ROKU' # internet
    'UBER' 'INVZ' 'CYN' 'MBLY' 'LCID' 'STLA' 'RIVN' 'ECX' 'AUR' 'MVIS' # self-driving
    'STNE' 'CHYM' 'PYPL' 'AFRM' 'NU' # financial
    'RR' 'SERV' 'KITT' 'ARBE' # robot
)

# 设置默认值
if [ -z "$1" ]; then
    period="1y"
else
    period="$1"
fi

if [ -z "$2" ]; then
    interval="1d"
else
    interval="$2"
fi

if [ -z "$3" ]; then
    save_root="/Users/chengxian/Desktop/buy_sell_images"
else
    save_root="$3"
fi

for symbol in "${symbols[@]}"
do
#    echo "$symbol"
#    python candle_dark.py --symbol $symbol --period ${period} --interval ${interval}
   python candle_dark_doubao.py --symbol $symbol --period ${period} --interval ${interval} --save_root ${save_root}
done
echo "plot end..."