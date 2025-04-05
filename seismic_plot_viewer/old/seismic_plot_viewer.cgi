#!/usr/bin/env perl
#
# Perl script to serve a web page to view seismic plot files in
# a convenient form
#
# Assumes all files are in form: STA_CODE_NET.yyyymmddhh.gif/png
#
# Version 1.1, for webobs installation
# Version 1.2, adds pan_plot functionality
# Version 1.3, larger fonts for Blackberriers in concise mode
# Version 2.0, tidied up lots
#
# Rod Stewart, UWI/SRC, 2010-06-10, 2010-10-19, 2020-05-05

use strict;
use CGI;
use CGI qw/:standard/;
use Time::Local;

my $dir_data;
my $dir_data_web;

my $network = 'MVO';
my $dir_data_mon = '/mnt/earthworm00/monitoring_data';
#my $dir_data_mon = '/mnt/volcano01/Seismic_Data/monitoring_data';
my $dir_data_mon_web = '/monitoring'; 
#my $dir_data_mon_web = '/seismic/monitoring_data';
my $dir_data_pan = '/mnt/volcano01/Seismic_Data/monitoring_data';
my $dir_data_pan_web = '/seismic/monitoring_data';
my $dir_data_sub;
my $ext;
my $ext_mon = 'gif';
my $ext_pan = 'png';

my $station_to_plot;
my $date_to_plot;
my $what_to_plot;
my $layout;

my @stations;
my @regstations;

my @regstations_mon = qw( ABD_HHZ_WI ANWB_BHZ_CU GRGR_BHZ_CU GRHS_HHZ_TR 
			  GRSS_HHZ_TR GRSS_EHZ_TR GRW_HHZ_TR GCMP_HHZ_TR 
			  SVB_HHZ_TR SABA_BHZ_NA );

#my @stations_mon = qw( 	MBBY_BHZ_MV 
#			MBFL_SHZ_MV MBFR_BHZ_MV 
#			MBGB_BHZ_MV MBGH_BHZ_MV MBHA_BHZ_MV 
#			MBLG_BHZ_MV MBLY_BHZ_MV
#			MBRY_BHZ_MV MBWH_BHZ_MV MBWW_HHZ_MV );
my @stations_mon = qw( 	MBBY_BHZ_MV 
			MBFL_HHZ_MV_00 MBFR_BHZ_MV 
			MBGB_BHZ_MV MBGH_HHZ_MV_00 MBHA_BHZ_MV 
			MBLG_BHZ_MV MBLY_HHZ_MV_00
			MBRY_BHZ_MV MBWH_BHZ_MV );

#my @stations_pan = qw( 	MBBY_BHZ_MV MBFR_BHZ_MV 
#					MBGB_BHZ_MV MBGH_BHZ_MV MBHA_BHZ_MV 
#					MBLG_BHZ_MV MBLY_BHZ_MV
#					MBRY_BHZ_MV MBWH_BHZ_MV MBWW_HHZ_MV );
my @stations_pan = qw( 	MBBY_BHZ_MV MBFR_BHZ_MV 
					MBGB_BHZ_MV MBGH_BHZ_MV MBHA_BHZ_MV 
					MBLG_BHZ_MV MBLY_BHZ_MV
					MBRY_BHZ_MV MBWH_BHZ_MV );
my $sta_default = 'MBGH_HHZ_MV_00';
#my $sta_default = 'MBLY_BHZ_MV';

# Spiders added 05-Jun-2014, PJS
my @spiders;
#my @spiders_mon = qw( MSCP_SHZ_MV MSDE_SHZ_MV MSGL_SHZ_MV MSGS_SHZ_MV 
#			MSMX_SHZ_MV MSNW_SHZ_MV MSS1_SHZ_MV MSUH_SHZ_MV ) ;
my @spiders_mon = qw( MSS1_SHZ_MV_-- MSUH_SHZ_MV ) ;
# 
#  Splitting regional stations into groups
#  RCS, 18-Jun-2019
my @regstationsd;
my @regstationsd_mon  = qw( DLPL_HHZ_TR DSLB_HHZ_TR DWS_HHZ_TR MDN_HHZ_TR ); 

# Test stations
# RCS, 5-May-2020
my @teststations;
my @teststations_mon = qw( MBFL_HHZ_MV_-- MBGH_HHZ_MV_-- MBLY_HHZ_MV_-- );

my @dates = ();
my @whats = qw( heli sgram pan );

my $web_start_page = '/cgi-bin/seismic_plot_viewer.cgi';
my $web_other_page = '/cgi-bin/seismic_plot_viewer_2.cgi';
my $plot_width;
$plot_width = '500';

# Get date and time (UTC)
my ($year, $month, $day) = (gmtime())[5,4,3];
$year = 1900 + $year;
$month++;
my $today = sprintf( '%04s-%02s-%02s', $year, $month, $day );

# New thing
my $q = CGI->new;

# Get parameters from url
$station_to_plot = $q->param('station');
$date_to_plot = $q->param('date');
$what_to_plot = $q->param('what');
$layout = $q->param('layout');

if( $date_to_plot eq 'default' ) {
	$date_to_plot = $today;
}
elsif( $date_to_plot eq '' ){
	$date_to_plot = $today;
}

if( $what_to_plot eq 'default' ) {
	$what_to_plot = 'heli';
}
elsif( $what_to_plot eq '' ) {
	$what_to_plot = 'heli';
}

if( $station_to_plot eq 'default' ) {
	$station_to_plot = $sta_default;
}
elsif( $station_to_plot eq '' ) {
	$station_to_plot = $sta_default;
}

if( $layout eq 'default' ) {
	$layout = 'normal';
}
elsif( $layout eq '' ) {
	$layout = 'normal';
}

# Data directory
if( $what_to_plot eq 'heli' ) {
	$ext = $ext_mon;
	$dir_data = $dir_data_mon;
	$dir_data_web = $dir_data_mon_web;	
	$dir_data_sub = 'helicorder_plots';
	@stations = @stations_mon;
	# PJS
	@spiders = @spiders_mon;
	@regstations = @regstations_mon;
	@regstationsd = @regstationsd_mon;
	@teststations = @teststations_mon;
}
elsif( $what_to_plot eq 'sgram' ) {
	$ext = $ext_mon;
	$dir_data = $dir_data_mon;
	$dir_data_web = $dir_data_mon_web;	
	$dir_data_sub = 'sgram';
	@stations = @stations_mon;
	# PJS
	@spiders = @spiders_mon;
	@regstations = @regstations_mon;
	@regstationsd = @regstationsd_mon;
}
elsif( $what_to_plot eq 'pan' ) {
	$ext = $ext_pan;
	$dir_data = $dir_data_pan;
	$dir_data_web = $dir_data_pan_web;	
	$dir_data_sub = 'pan_plots';
	@stations = @stations_pan;
}

my $plot_dir = join( '/', $dir_data, $dir_data_sub );
my $plot_dir_web = join( '/', $dir_data_web, $dir_data_sub );

my $sec_in_day = 60 * 60 * 24;
my( $year, $month, $day ) = split( /-/, $today );
my $daynum_today = int( timegm(0,0,0,$day,$month-1,$year-1900) / $sec_in_day );
my( $year, $month, $day ) = split( /-/, $date_to_plot );
my $daynum_date_to_plot = int( timegm(0,0,0,$day,$month-1,$year-1900) / $sec_in_day );

# fudge to fix change of MBHA channel code from BHZ -> SHZ
# PJS 18-Dec-2013

# date of channel code change (i.e. 17-Dec-2013)
my $daynum_MBHA = int( timegm(0,0,0,17,12-1,2013-1900) / $sec_in_day );
# if after that date replace BHZ with SHZ
if ( $daynum_date_to_plot gt $daynum_MBHA ){
	$station_to_plot =~ s/MBHA_BHZ/MBHA_SHZ/;
	@stations = map {$_ =~ s/MBHA_BHZ/MBHA_SHZ/; $_} @stations;
} else {
	$station_to_plot =~ s/MBHA_SHZ/MBHA_BHZ/;
	@stations = map {$_ =~ s/MBHA_SHZ/MBHA_BHZ/; $_} @stations;
}

my $days_to_show;
if( $layout eq 'normal') {
	if( $what_to_plot eq 'pan' ) {
		$days_to_show = 29;
	} else {
		$days_to_show = 55;		
	}
}
elsif( $layout eq 'concise') {
	$days_to_show = 11;
}

my $days_ahead = ($daynum_today - $daynum_date_to_plot);
if( $days_ahead > int( $days_to_show/2 ) ) {
	$days_ahead = int( $days_to_show/2 );
}

for(my $i=0;$i<$days_to_show;$i++) {
	my $iday = $daynum_date_to_plot + $days_ahead - $i;
	my ($year, $month, $day) = (gmtime($iday*$sec_in_day))[5,4,3];
	$year = 1900 + $year;
	$month++;
	my $day = sprintf( '%04s-%02s-%02s', $year, $month, $day );
	
	$dates[$i] = $day;
}
if( $dates[0] ne $today ) {
	@dates = ($today,@dates);
}

my $file_to_plot;
my $file_to_plot_web;

my $date_filename;
if( $what_to_plot eq 'pan' ) {
	$date_filename = join( '', split( /-/, $date_to_plot) );
} else {
	$date_filename = join( '', split( /-/, $date_to_plot), '00' );
}

$file_to_plot = join( '.', $station_to_plot, $date_filename, $ext );

$file_to_plot_web = join( '/', $plot_dir_web, $file_to_plot );
$file_to_plot = join( '/', $plot_dir, $file_to_plot );

# Things for web page
my $title = join( ': ', $network, 'Helicorders, Spectrograms and Pan Plots' );
my $spaces = "&nbsp;";
my $markerl='<FONT COLOR="#FF0000">*</FONT>';
my $markerr='<FONT COLOR="#FF0000">*</FONT>';
my $markersp = '&nbsp;';

# Print web page
print $q->header, "\n";
print $q->start_html( -title => $title, -head => $q->meta( {-http_equiv=>'REFRESH',-content=>'60'}) );
print "\n";

if( $layout eq 'normal' ) {
	print "<TT>\n";
}

# Print whats across page
if( $layout eq 'concise' ) {
	print "<FONT SIZE=+1>";
}
print "<B>What:</B>", $spaces, "\n";
foreach my $what (@whats) {
	my $link = sprintf( "%s?station=%s&date=%s&what=%s&layout=%s", 
			$web_start_page, $station_to_plot, $date_to_plot, $what, $layout );
	if( $what eq $what_to_plot ) {
		print $markerl;
	} else {
		print $markersp;
	}
	print $q->a({href=>$link},$what);
	if( $what eq $what_to_plot ) {
		print $markerr, $spaces, $spaces;
	} else {
		print $markersp, $spaces, $spaces;
	}
	print "\n";	
}
if( $layout eq 'concise' ) {
	print "</FONT>\n";
}

# Link to other page
print $spaces, $spaces, $spaces;
print $spaces, $spaces, $spaces;
print $spaces, $spaces, $spaces;
print $spaces, $spaces, $spaces;
if( $layout eq 'normal' ) {
	print $spaces, $spaces, $spaces;
	print $spaces, $spaces, $spaces;
	print $spaces, $spaces, $spaces;
	print $spaces, $spaces, $spaces;
	print $spaces, $spaces, $spaces;
	print $spaces, $spaces, $spaces;
	print $spaces, $spaces, $spaces;
	print $spaces, $spaces, $spaces;
}

if( $layout eq 'concise' ) {
	print "<FONT SIZE=+1>\n";
}
print $q->a({href=>$web_other_page},'Full Menu Selection');
if( $layout eq 'concise' ) {
	print "</FONT>\n";
}
print "<BR>\n";

# Print stations across page
if( $layout eq 'concise' ) {
	print "<FONT SIZE=+1>\n";
}
print "<B>MVO:  </B>", $spaces, "\n";

	foreach my $station ( @stations ) {
		my ($station_nice,$dum1,$dum2) = split /_/, $station;
		my $link = sprintf( "%s?station=%s&date=%s&what=%s&layout=%s", 
			$web_start_page, $station, $date_to_plot, $what_to_plot, $layout );
		#print "$station\n";
		#print "$station_to_plot\n";
		if( $station eq $station_to_plot) {
			print $markerl;
		} else {
			print $markersp;
		}
		print $q->a({href=>$link},$station_nice);
		if( $station eq $station_to_plot) {
			print $markerr, $spaces, $spaces;
		} else {
			print $markersp, $spaces, $spaces;
		}
		print "\n";
	}
print "<BR>\n";
print "<B>Spi:  </B>", $spaces, "\n";

	foreach my $spider ( @spiders ) {
		my ($spider_nice,$dum1,$dum2) = split /_/, $spider;
		my $link = sprintf( "%s?station=%s&date=%s&what=%s&layout=%s", 
			$web_start_page, $spider, $date_to_plot, $what_to_plot, $layout );
		#print "$station\n";
		#print "$station_to_plot\n";
		if( $spider eq $station_to_plot) {
			print $markerl;
		} else {
			print $markersp;
		}
		print $q->a({href=>$link},$spider_nice);
		if( $spider eq $station_to_plot) {
			print $markerr, $spaces, $spaces;
		} else {
			print $markersp, $spaces, $spaces;
		}
		print "\n";
	}


print "<BR>\n";
print "<B>Reg:  </B>", $spaces, "\n";

	foreach my $regstation ( @regstations ) {
		my ($regstation_nice,$dum1,$dum2) = split /_/, $regstation;
		my $link = sprintf( "%s?station=%s&date=%s&what=%s&layout=%s", 
			$web_start_page, $regstation, $date_to_plot, $what_to_plot, $layout );
		#print "$station\n";
		#print "$station_to_plot\n";
		if( $regstation eq $station_to_plot) {
			print $markerl;
		} else {
			print $markersp;
		}
		print $q->a({href=>$link},$regstation_nice);
		if( $regstation eq $station_to_plot) {
			print $markerr, $spaces, $spaces;
		} else {
			print $markersp, $spaces, $spaces;
		}
		print "\n";
	}

	
print "<BR>\n";
print "<B>Dom:  </B>", $spaces, "\n";

	foreach my $regstationd ( @regstationsd ) {
		my ($regstationd_nice,$dum1,$dum2) = split /_/, $regstationd;
		my $link = sprintf( "%s?station=%s&date=%s&what=%s&layout=%s", 
			$web_start_page, $regstationd, $date_to_plot, $what_to_plot, $layout );
		#print "$station\n";
		#print "$station_to_plot\n";
		if( $regstationd eq $station_to_plot) {
			print $markerl;
		} else {
			print $markersp;
		}
		print $q->a({href=>$link},$regstationd_nice);
		if( $regstationd eq $station_to_plot) {
			print $markerr, $spaces, $spaces;
		} else {
			print $markersp, $spaces, $spaces;
		}
		print "\n";
	}


print "<BR>\n";
print "<B>Test: </B>", $spaces, "\n";

	foreach my $teststation ( @teststations ) {
		my ($teststation_nice,$dum1,$dum2) = split /_/, $teststation;
		my $link = sprintf( "%s?station=%s&date=%s&what=%s&layout=%s", 
			$web_start_page, $teststation, $date_to_plot, $what_to_plot, $layout );
		#print "$station\n";
		#print "$station_to_plot\n";
		if( $teststation eq $station_to_plot) {
			print $markerl;
		} else {
			print $markersp;
		}
		print $q->a({href=>$link},$teststation_nice);
		if( $teststation eq $station_to_plot) {
			print $markerr, $spaces, $spaces;
		} else {
			print $markersp, $spaces, $spaces;
		}
		print "\n";
	}




if( $layout eq 'concise' ) {
	print "</FONT>\n";
}

if( $layout eq 'concise' ) {
	# Print dates across page
	print "<FONT SIZE=+1>\n";
	print "<BR>\n";
	print "<B>Date:</B>", $spaces, "\n";

	foreach my $date ( @dates ) {
		my ($year, $month, $day) = split( /-/, $date );
		my $date_nice = join ( '/', $day, $month );
		my $link = sprintf( "%s?station=%s&date=%s&what=%s&layout=%s", 
			$web_start_page, $station_to_plot, $date, $what_to_plot, $layout );
		if( $date eq $date_to_plot) {
			print $markerl;
		} else {
			print $markersp;
		}
		print $q->a({href=>$link},$date_nice);
		if( $date eq $date_to_plot) {
			print $markerr, $spaces;
		} else {
			print $markersp, $spaces;
		}

		print "\n";
	}
	print "</FONT>\n";
}

if( $layout eq 'normal' ) {
	print "</TT>\n";
}
print "<BR>\n";
print "This page refreshes automatically every minute.<BR>\n";


if( $layout eq 'concise' ) {

	if( -e $file_to_plot ) {	

		# if concise layout, resize image to browser width and use as hyperlink to full size helicorder
		# should load faster if viewed on mobile broswer
		# PJS, 23-Jul-2012		
		print $q->a({href=>$file_to_plot_web}, img {src=>$file_to_plot_web, align=>"LEFT", width=>"100%", border=>"0"});
	}else{
	print "$file_to_plot not found<BR>\n";
	}

} else {
	if( -e $file_to_plot ) {
		if( $what_to_plot eq 'pan' ) {
		my $plot_width = 852;
		print $q->a({href=>$file_to_plot_web},'Full size'), "<BR>\n";
		print $q->img({-src=>$file_to_plot_web,-align=>'LEFT',-width=>$plot_width,-style=>'25px solid white'});
		} else {
		print $q->img({-src=>$file_to_plot_web,-align=>'LEFT',-style=>'25px solid white'});
		}
	}else{
	print "$file_to_plot not found<BR>\n";
	}
}

if( $layout eq 'normal' ) {
	print "<TT>\n";
	
	# Print to right of image
	print "<BR><B>Date:</B><BR>", "\n";

	foreach my $date ( @dates ) {
		my ($year, $month, $day) = split( /-/, $date );
		my $date_nice = join ( '/', $day, $month );
		my $link = sprintf( "%s?station=%s&date=%s&what=%s&layout=%s", 
			$web_start_page, $station_to_plot, $date, $what_to_plot, $layout );
		if( $date eq $date_to_plot) {
			print $markerl;
		} else {
			print $markersp;
		}
		print $q->a({href=>$link},$date_nice);
		if( $date eq $date_to_plot) {
			print $markerr, $spaces;
		} else {
			print $markersp, $spaces;
		}
		print "<BR>\n";
	}
	print "</TT>\n";
}

print $q->end_html;

