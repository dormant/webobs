#!/bin/bash

for sta in MBFL_HHZ MBGB_HHZ MBGH_HHZ MBHA_SHZ MBLG_HHZ MBLY_HHZ MBRV_BHZ MBRY_BHZ MBWH_BHZ MSS1_SHZ MBBY_HHZ; do

    cp $(ls /mnt/earthworm00/monitoring_data/helicorder_plots/${sta}*.gif | tail -1) /var/www/html/heli/${sta}.gif

done
