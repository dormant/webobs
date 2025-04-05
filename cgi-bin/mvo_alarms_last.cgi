#!/usr/bin/env perl
#
# Perl script to print last N alarms from the earthworm system at MVO.
# Designed to work in WebObs at MVO.
# Outputs a fragment of HTML code.
#
# Version 1.0
#
# Rod Stewart, UWI/SRC, 2010-06-14

use strict;

# Alarm directory
my $dir_alarms = '/mnt/mvofls2/Seismic_Data/monitoring_data/status/log';

# Number of alarms to print
my $last_n = 5;

# Command to get alarm text
my $command = sprintf( "cat %s/sound_alarm_2*.log | grep _UTC_ | tail -5", $dir_alarms );

my @alarms = `$command`;
chomp @alarms;

print "Content-type: text/html", "\n\n";

print "<B>Last $last_n earthworm alarms</B><P>\n";
print "<TT>\n";

foreach my $alarm (@alarms) {
	my ($datim,$dum1,$dum2,$dum3,$dum4, $dum5, $dum6 ) = split( ' ', $alarm, 7 );
	my $alarm_text = join( ' ', $dum2, $dum3, $dum4 );
	if( $dum2 eq 'TEST' ) {
		$alarm_text = $dum2;
	}
	$datim =~ s/_UTC_/ /g;
	
	print join( ' ', $datim, $alarm_text ), "\n";
	print "<BR>\n";
}

print "</TT>\n"
