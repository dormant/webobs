#!/usr/bin/env perl
#
# Perl script to serve a web page to view seismic plot files in
# a convenient form. This allows full selection, and two plots.
#
# Assumes all files are in form: STA_CODE_NET.yyyymmddhh.gif/png
#
# Version 1.0, for webobs installation
#
# Rod Stewart, UWI/SRC, 2010-06-10
# 
# modified by PJS 2011-07-04. 
# Included pan plots in menu for single figure mode. Increased years_in_dir to include older data.
# This version further modified by PJS 2011-09-14.
# Only list station codes - script now identifies correct channel code for the given date/station
#
# Modified by PJS 2011-12-13:
# In order to dramtically speed up locating image files, this script now calls /usr/local/bin/heli_nearest.pl
# to get filename from daily updated database - rather than globbing filename from the folder for each call.

use strict;
use CGI;
use CGI::Carp qw/fatalsToBrowser/;
use Time::Local;

my $network = 'MVO';

my $dir_data_ew = '/mnt/earthworm00/monitoring_data';
my $dir_data = '/mnt/volcano01/Seismic_Data/monitoring_data';
my $dir_data_web_ew ='/monitoring';
my $dir_data_web = '/seismic/monitoring_data';
my $ext = 'gif';
my $layout;
my $web_start_page = '/cgi-bin/seismic_plot_viewer_2.cgi';
my $web_other_page = '/cgi-bin/seismic_plot_viewer.cgi';
my $plot_width = 500;
my $date_to_plot_1_yr;
my $date_to_plot_2_yr;
my $date_to_plot_1_mo;
my $date_to_plot_2_mo;
my $date_to_plot_1_da;
my $date_to_plot_2_da;
my $what_to_plot_1;
my $what_to_plot_2;
my $stat_to_plot_1;
my $stat_to_plot_2;
my $file_to_plot_1;
my $file_to_plot_2;
my $file_to_plot_web_1;
my $file_to_plot_web_2;
#my $years_in_dir = 16;

my $date_to_plot_2;

# Get date and time (UTC)
my ($year, $month, $day) = (gmtime())[5,4,3];
$year = 1900 + $year;
$month++;

my $years_in_dir = ($year - 1996 + 1);

# For menus
my %stations = (
					ANWB => 'Willy Bob, Antigua (ANWB)',
					MBBE => 'Bethel (MBBE)',
					MBBY => 'Broderick\'s Yard (MBBY)',
					MBFL => 'Flemmings (MBFL)',
					MBFR => 'Fergus Ridge (MBFR)',
					MBGA => 'Gages (MBGA)',
					MBGB => 'Garibaldi Hill (MBGB)',
					MBGE => 'Galways Estate (MBGE)',
					MBGH => 'St Georges\' Hill (MBGH)',
					MBHA => 'Harris (MBHA)',
					MBLG => 'Long Ground (MBLG)',
					MBLY => 'Lee\'s Yard (MBLY)',
                                        MBMH => 'Mongo Hill (MBMH)',
					MBRY => 'Roache\'s Yard (MBRY)',
					MBRV => 'Rendezvous (MBRV)',
					MBSS => 'South Soufriere (MBSS)',
					MBWW => 'Waterworks (MBWW)',
					MBWH => 'Windy Hill (MBWH)',
					MSCP => 'Chance\'s Peak, Spider (MSCP)',
					MSS1 => 'Scar 1, Spider (MSS1)',
					MSUH => 'Upper Hermitage, Spider (MSUH)',
				);
my @stacodes = sort( keys %stations );

my $sta_default = 'MBGH';
my @whats = qw( heli sgram pan );
my @months = qw( 01 02 03 04 05 06 07 08 09 10 11 12 );
my @days = qw( 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 );
my @years = ();
for( my $i=$year; $i>$year-$years_in_dir; $i-- ) {
	push( @years, sprintf( '%04s', $i ) );
}

# Default values for plotting
$layout = 'one';
$what_to_plot_1 = 'heli';
$stat_to_plot_1 = $sta_default;
$date_to_plot_1_yr = sprintf( '%04s', $year );
$date_to_plot_1_mo = sprintf( '%02s', $month );
$date_to_plot_1_da = sprintf( '%02s', $day );
$what_to_plot_2 = 'sgram';
$stat_to_plot_2 = $stat_to_plot_1;
$date_to_plot_2_yr = $date_to_plot_1_yr;
$date_to_plot_2_mo = $date_to_plot_1_mo;
$date_to_plot_2_da = $date_to_plot_1_da;

# New thing
my $q = CGI->new;

# Get values from form
if ($q->param()) { 
	$layout = $q->param('layout');
	$what_to_plot_1 = $q->param('wha1');
	$stat_to_plot_1 = $q->param('sta1');
	$date_to_plot_1_yr = $q->param('yr1');
	$date_to_plot_1_mo = $q->param('mo1');
	$date_to_plot_1_da = $q->param('da1');
	if( $layout eq 'two' ){
		$what_to_plot_2 = $q->param('wha2');
		$stat_to_plot_2 = $q->param('sta2');
		$date_to_plot_2_yr = $q->param('yr2');
		$date_to_plot_2_mo = $q->param('mo2');
		$date_to_plot_2_da = $q->param('da2');
	}
}

# File for plot 1
my $dir_data_sub;
if( $what_to_plot_1 eq 'heli' ) {
	$dir_data_sub = 'helicorder_plots';
	$ext = 'gif';
}
elsif( $what_to_plot_1 eq 'sgram' ) {
	$dir_data_sub = 'sgram';
	$ext = 'gif';
}
elsif( $what_to_plot_1 eq 'pan' ) {
	$dir_data_sub = 'pan_plots';
	$ext = 'png';
}
# choose ew directory if plot is for today:
my $mo = sprintf( '%02s', $month );
my $da = sprintf( '%02s', $day );
if ( ($date_to_plot_1_yr eq $year) && ($date_to_plot_1_mo eq $mo ) && ($date_to_plot_1_da eq $da) ){
	$dir_data = $dir_data_ew;
	$dir_data_web = $dir_data_web_ew;
}

my $plot_dir = join( '/', $dir_data, $dir_data_sub );
my $plot_dir_web = join( '/', $dir_data_web, $dir_data_sub );
my $date_to_plot = join( '', $date_to_plot_1_yr, $date_to_plot_1_mo, $date_to_plot_1_da);
#
#if( $what_to_plot_1 eq 'pan' ) {
#	$file_to_plot_1 = join( '.', $stat_to_plot_1, join( '', $date_to_plot ), $ext );
#} else {
	#$file_to_plot_1 = join( '.', $stat_to_plot_1, join( '', $date_to_plot, '00' ), $ext );

	#my $glob_str="$plot_dir/$stat_to_plot_1\*Z\*$date_to_plot*$ext";
	#$file_to_plot_1 = glob($glob_str);
	#$file_to_plot_1 = `heli_nearest.pl $what_to_plot_1 $stat_to_plot_1 $date_to_plot`;
	
	# if more than one image is returned (e.g. displacement channels) choose first:
	$file_to_plot_1 = `heli_nearest.pl $what_to_plot_1 $stat_to_plot_1 $date_to_plot | head -1`;
	# PJS, 16-Feb-2015
	#
	# try to trim any whitespace
	$file_to_plot_1 =~ s/^\s+|\s+$//g;
	
	$file_to_plot_1 = (split /\//, $file_to_plot_1)[-1];
#}
#print "file_to_plot_1 = $file_to_plot_1\n";
#"file_to_plot_1 = $file_to_plot_1\n";
#$file_to_plot_1 = join( '.', $stat_to_plot_1, join( '', $date_to_plot, '00' ), $ext );
$file_to_plot_web_1 = join( '/', $plot_dir_web, $file_to_plot_1 );
$file_to_plot_1 = join( '/', $plot_dir, $file_to_plot_1 );

# File for plot 2
if( $layout eq 'two' ) {

	# choose ew directory if plot is for today:
	my $mo = sprintf( '%02s', $month );
	my $da = sprintf( '%02s', $day );
	if ( ($date_to_plot_2_yr eq $year) && ($date_to_plot_2_mo eq $mo ) && ($date_to_plot_2_da eq $da) ){
	$dir_data = $dir_data_ew;
	$dir_data_web = $dir_data_web_ew;
	}

	if( $what_to_plot_2 eq 'heli' ) {
		$dir_data_sub = 'helicorder_plots';
	}
	elsif( $what_to_plot_2 eq 'sgram' ) {
		$dir_data_sub = 'sgram';
	}
	my $plot_dir = join( '/', $dir_data, $dir_data_sub );
	my $plot_dir_web = join( '/', $dir_data_web, $dir_data_sub );
	$date_to_plot_2 = join( '', $date_to_plot_2_yr, $date_to_plot_2_mo, $date_to_plot_2_da);
#	$file_to_plot_2 = join( '.', $stat_to_plot_2, join( '', $date_to_plot, '00' ), $ext );
#	my $glob_str="$plot_dir/$stat_to_plot_2\*Z\*$date_to_plot_2*$ext";
#	$file_to_plot_2 = glob($glob_str);
	$file_to_plot_2 = `heli_nearest.pl $what_to_plot_2 $stat_to_plot_2 $date_to_plot_2`;
	# try to trim any whitespace
	$file_to_plot_2 =~ s/^\s+|\s+$//g;
	$file_to_plot_2 = (split /\//, $file_to_plot_2)[-1];
#	
	$file_to_plot_web_2 = join( '/', $plot_dir_web, $file_to_plot_2 );
	$file_to_plot_2 = join( '/', $plot_dir, $file_to_plot_2 );
}

# Things for web page
my $title = join( ': ', $network, 'Helicorders and Spectrograms' );
my $space1 = "&nbsp;&nbsp;";
my $space2 = "&nbsp;&nbsp;&nbsp;&nbsp;";
my $space4 = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";

# Print web page
print $q->header, "\n";
#print $q->start_html( -title => $title, -head => $q->meta( {-http_equiv=>'REFRESH',-content=>'60'}) );
print $q->start_html( -title => $title );
print "\n";
# Print form
print $q->start_form( -action => $web_start_page, -method => 'post' ), "\n";

print "Plots: ", $space1;
print $q->radio_group( -name => 'layout', -values => ['one','two'] );
print $space4;
print $space4;
print $space4;
print $q->submit( -name => 'submit' );

# Link to other page
print $space2, $space2, $space2;
print $space2, $space2, $space2;
print $space2, $space2, $space2;
print $space2, $space2, $space2;
print $space2, $space2, $space2;
print $space2, $space2, $space2;
print $space2, $space2, $space2;
print $space2, $space2, $space2;
print $space2, $space2, $space2;
print $space2, $space2, $space2;
print $space2, $space2, $space2;
print $space2, $space2, $space2;
print $space2, $space2, $space2;
print $q->a({href=>$web_other_page},'No Menus');
print "<BR>\n";

print $q->popup_menu( -name => 'wha1', -values => \@whats, -default=>$what_to_plot_1);
print $space2;
print $q->popup_menu( -name => 'sta1', -values => \@stacodes, -labels => \%stations, -default=>$stat_to_plot_1 );
print $space2;
print $q->popup_menu( -name => 'yr1', -values => \@years, -default=>$date_to_plot_1_yr);
print $space2;
print $q->popup_menu( -name => 'mo1', -values => \@months, -default=>$date_to_plot_1_mo);
print $space2;
print $q->popup_menu( -name => 'da1', -values => \@days, -default=>$date_to_plot_1_da);

print $space4;

print $q->popup_menu( -name => 'wha2', -values => \@whats, -default=>$what_to_plot_2);
print $space2;
print $q->popup_menu( -name => 'sta2', -values => \@stacodes, -labels => \%stations, -default=>$stat_to_plot_2 );
print $space2;
print $q->popup_menu( -name => 'yr2', -values => \@years, -default=>$date_to_plot_2_yr);
print $space2;
print $q->popup_menu( -name => 'mo2', -values => \@months, -default=>$date_to_plot_2_mo);
print $space2;
print $q->popup_menu( -name => 'da2', -values => \@days, -default=>$date_to_plot_2_da);

print $q->end_form, "\n";
print "This page does not refresh automatically.<BR>\n";
print $q->hr(), "\n";

# Set date in nice format
my $datenice1 = join('-', substr($date_to_plot,0,4), substr($date_to_plot,4,2), substr($date_to_plot,6,2));
# Print plots
if( $layout eq 'two') {
	my $datenice2 = join('-', substr($date_to_plot_2,0,4), substr($date_to_plot_2,4,2), substr($date_to_plot_2,6,2));
	if( -f $file_to_plot_1 ) {
		print $q->img({-src=>$file_to_plot_web_1,-align=>'LEFT',-width=>$plot_width,-style=>'25px solid white'});
	}else{
		#print "$file_to_plot_1 not found<BR>\n";
		print "No plot for $stat_to_plot_1 on $datenice1.\n";

	}
	if( -f $file_to_plot_2 ) {
		print $q->img({-src=>$file_to_plot_web_2,-align=>'LEFT',-width=>$plot_width,-style=>'25px solid white'});
	}else{
		#print "$file_to_plot_2 not found<BR>\n";
		print "No plot for $stat_to_plot_2 on $datenice2.\n";
	}
	# if one or other of the stations are unavailable give list:
	if (! -f $file_to_plot_1 || ! -f $file_to_plot_2){
	## now print a list of available stations for that day:	
		
		my @available_stats = `heli_nearest.pl $what_to_plot_1 MB $date_to_plot`;
		my $size = scalar(@available_stats);
		my $size1 = length(@available_stats[0]);

		if ( $size > 1 || ( ($size == 1) && ($size1 > 1) ) ){

		print "The following stations are available on $datenice1:\n<BR>\n<BR>\n";

			foreach my $avstat (@available_stats) {
		# try to trim any whitespace
		$avstat =~ s/^\s+|\s+$//g;
		# get station codes
		$avstat = ( split /\//, $avstat )[-1];
		$avstat = ( split/\./, $avstat )[0];
		$avstat = ( substr $avstat, 0, 4 );	
		print "$avstat\n<BR>\n";
			}
		}
		else {
		print "No plots are available for $datenice1.\n";
		}
	}
}
else {
	if( -f $file_to_plot_1 ) {

		if( $what_to_plot_1 eq 'pan' ) {
			my $plot_width = 852;
			print $q->a({href=>$file_to_plot_web_1},'Full size'), "<BR>\n";
			print $q->img({-src=>$file_to_plot_web_1,-align=>'LEFT',-width=>$plot_width,-style=>'25px solid white'});
			} else {
			print $q->img({-src=>$file_to_plot_web_1,-align=>'LEFT',-style=>'25px solid white'});
			#print "file_to_plot_1 = $file_to_plot_1\n";
			#print "No plot for $stat_to_plot_1 on $datenice1.\n";
			}
	}else{
		print "No plot for $stat_to_plot_1 on $datenice1.\n<BR>\n<BR>\n";

		## now print a list of available stations for that day:	
		
		my @available_stats = `heli_nearest.pl $what_to_plot_1 MB $date_to_plot`;
		my $size = scalar(@available_stats);
		my $size1 = length(@available_stats[0]);

		if ( $size > 1 || ( ($size == 1) && ($size1 > 1) ) ){

		print "The following stations are available on $datenice1:\n<BR>\n<BR>\n";

			foreach my $avstat (@available_stats) {
		# try to trim any whitespace
		$avstat =~ s/^\s+|\s+$//g;
		# get station codes
		$avstat = ( split /\//, $avstat )[-1];
		$avstat = ( split/\./, $avstat )[0];
		$avstat = ( substr $avstat, 0, 4 );	
		print "$avstat\n<BR>\n";
			}
		}
		else {
		print "No plots are available for $datenice1.\n";
		}
	}
}
#print "file_to_plot_1 = $file_to_plot_1\n";
#print "glob_str = $glob_str\n";
print $q->end_html, "\n";

