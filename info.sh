# To find current frequency of CPU
temp=$(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq)
echo "Frequency: ${temp}"

# To get CPU temperature

vcgencmd measure_temp
