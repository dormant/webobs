#!/usr/bin/bash

./seismic_plot_viewer.cgi.3.1 mvo MBGH today heli summary > summary_heli.txt
./seismic_plot_viewer.cgi.3.1 mvo MBGH today sgram summary > summary_sgram.txt
./seismic_plot_viewer.cgi.3.1 mvo MBGH today pan summary > summary_pan.txt
./seismic_plot_viewer.cgi.3.1 mvo MBGH today heliwide summary > summary_heliwide.txt
./seismic_plot_viewer.cgi.3.1 mvo MBGH today helimulti summary > summary_helimulti.txt
./seismic_plot_viewer.cgi.3.1 mvo MBGH today heliscan summary > summary_heliscan.txt
./seismic_plot_viewer.cgi.3.1 mvo MBGH today helidisp summary > summary_helidisp.txt
