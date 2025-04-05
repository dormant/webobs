#!/usr/bin/env perl
### Change above to below on webobs
###!/home/webobs/opt/perl/bin/perl
# Perl script to serve a web page to view seismic monthly plot files in
# a convenient form
#
# Version 1: 2023-07-14
#
# Rod Stewart, UWI/SRC/MVO
#
#

use strict;
use warnings;
use Time::Local;
use DateTime;
use File::Basename;
use Sys::Hostname;
use CGI ':standard';
use CGI::Carp qw/fatalsToBrowser/;



## ============================================================================ 
##         INITIALISATION 
##


my $hostname;			# Machine being run on, set to either 'webobs' or 'opsproc3'
$hostname = hostname();

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Get todays date and time (UTC)
#
my ($year, $month, $day) = (gmtime())[5,4,3];
$year = 1900 + $year;
$month++;
my $today = sprintf( '%04s%02s%02s', $year, $month, $day );


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Directories
#
my $share_data; 			# Where we look for data in file hierarchy

my @stations_to_plot = qw( MBBY-seismic MBFL-seismic MBFR-seismic MBGB-seismic MBGH-seismic MBHA-seismic MBLG-seismic MBLY-seismic MBRV-seismic MBRY-seismic MSS1-seismic );


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Variables
#
my $debug;			# extra output for debugging
my $output;			# output format
#
#
# Variables used in output
#
my $web_start_page = '/cgi-bin/seismic_plot_viewer.cgi';
my $title = 'Monthly Seismic Helicorder Plots'; 
my $break;			# New line
my $marker;			# Symbol to marker header element in use
my $space;			# Single space
my $gap;
my $plot_width;      		# Width of plot on page
my $lgap = 2;


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Values for host-dependent variables
#
if( $hostname eq 'opsproc3' ) {
    $debug = 1;
    $output = 'text';
    $share_data = '/mnt/mvofls2/Seismic_Data/monitoring_data/helicorder_plots_station_month';
} else {
    $debug = 0;
    $output = 'html';
    $share_data = '/mnt/mvofls2/Seismic_Data/monitoring_data/helicorder_plots_station_month';
}


if( $output eq 'text' ) {
    $break = "\n";
    $space = ' ';
    $gap = $space x $lgap;
} else {
    $break = "\n<BR>\n";
    $space = '&nbsp;';
    $gap = $space x $lgap;
}



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Start new CGI thing
#
my $q;
if( not $debug ){
    $q = CGI->new;
}


#
if( $output eq 'html' ) {
    print $q->header, "\n";
	print $q->start_html( -title => $title ), "\n";
    print "<TT>\n";
    print "Click on image for full-size. If the image fails to load properly, click on Shift-Reload.", $break;
    print "<HR>";
} else {
	print $title, "\n";
}



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Loop trough months
#
my $start = DateTime->new(year => 1996, month => 10);
my $end   = DateTime->new(year => $year, month => $month);

if( $output eq 'text' ){
    print $gap;
    foreach my $statype (@stations_to_plot) {
        my ($sta,$type) = split /\-/, $statype;
        print $sta, $gap;
    }
    print "\n";
} else {
    print '<TABLE width="100%", border="1">', "\n";
    print "<TR>\n";
    print "<TD>Month</TD>\n";
    foreach my $statype (@stations_to_plot){
        my ($sta,$type) = split /\-/, $statype;
        my $statype2 = $statype;
        $statype2 =~ s/\-/<BR>/;
        print "<TD>$sta</TD>\n";
    }
    print "</TR>\n";
}

while ($start <= $end) {

    if( $output eq 'text' ){
        print $start->strftime("%Y-%m"), $gap;
    } else {
        if( $start->month == 1 ) {
            print "<TR>\n";
            print "<TD>Month</TD>\n";
            foreach my $statype (@stations_to_plot){
                my ($sta,$type) = split /\-/, $statype;
                my $statype2 = $statype;
                $statype2 =~ s/\-/<BR>/;
                print "<TD>$sta</TD>\n";
            }
            print "</TR>\n";
        }
        print "<TR>\n";
        my $ym = $start->strftime("%b %Y");
        print "<TD>$ym</TD>\n";

        foreach my $statype (@stations_to_plot) {
            #            my ($sta,$type) = split /\-/, $statype;
            my $image_file = join( '--', $statype, $start->strftime("%Y-%m"), $start->strftime("%B_%Y") );
            $image_file = join( '.', $image_file, 'png' );
            $image_file = join( '/', $share_data, $start->strftime("%Y"), $image_file );
            my $image_file_web = $image_file;
            $image_file_web =~ s/^.*monitoring_data/\/mvofls2\/monitoring_data/;
            my $image_file_web_thumb = $image_file_web;
            $image_file_web_thumb =~ s/\/19\d+\//\/0-thumbnails\//;
            $image_file_web_thumb =~ s/\/20\d+\//\/0-thumbnails\//;
            if( $debug ) {
                print $image_file, $gap;
        	    print $image_file_web, $gap;
            } else {
                print "<TD>\n";
                if( -e $image_file ) {
                    print $q->a({href=>$image_file_web}, img {src=>$image_file_web_thumb, align=>"LEFT", border=>"0"});
                } else {
                }
                print "</TD>\n";
            }
        }
        print "</TR>\n";
    }
    $start->add(months => 1);
}



# End of web page
if( not $debug ) {
    print "<TR>\n";
    print "<TD>Month</TD>\n";
    foreach my $statype (@stations_to_plot){
        my ($sta,$type) = split /\-/, $statype;
        my $statype2 = $statype;
        $statype2 =~ s/\-/<BR>/;
        print "<TD>$sta</TD>\n";
    }
    print "</TR>\n";
    print "</TABLE>\n";
    print "</TT>\n";
    print $q->end_html;
}
