```
lspci | grep -i raid
```
```
lspci -vmmnn
```
# Check adapter - raid controller
To get <device number of adapter>
```
./MegaCli64 -AdpGetPciInfo -aAll
```
```
./MegaCli64 -EncInfo -a<device number of adapter>
```
```
./MegaCli64 -LdPdInfo -a<device number of adapter>
```
```
./MegaCli64 -LDInfo -Lall -a<device number of adapter>
```
# Get hardware structure
```
./MegaCli64 -LdPdInfo -a<device number of adapter> | grep -E "Virtual Drive:|Slot Number:" | xargs | sed -r 's/(Slot Number:)(\s[0-9]+)/\2,/g' | sed 's/(Target Id: .)/Physical Drives ids:/g' | sed 's/Virtual Drive:/\nVirtual Drive:/g'
```
# Check BBU
```
./MegaCli64  -AdpBbuCmd -aALL
```
