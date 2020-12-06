g++ -E $1 > temp
sed '/^# [0-9]* ".*" 1 3/,/# [0-9]* ".*" 2$/d' temp > temp1
sed '/^#/d' temp1 > temp
rm temp1
