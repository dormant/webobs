#!/usr/bin/env perl
#
# Perl script to find image files
#
# Rod Stewart, UWI/SRC, 2023-01-27

use strict;
use warnings;

my $dir_data; 			# Where we look for data in file hierarchy

# Variables used in looking for plots
my $plot_type;
my $share_data;			# where data is shared, usually two choices

# Choices for above variables
my @plot_types = qw( heli heliwide sgram pan helimulti heliscan helidisp vlp );

# Set up directories using function
my ($sdRef, $ptdRef) = setDataDir();
my @shares_data = @$sdRef;
my %plot_type_dirs = %$ptdRef;

my @staStrings = qw( MSS1 MSCP MSUH MSMX MSNW TRC2 TRC3 MBBE MBET MBBY MBFL );

$share_data = $shares_data[1];

my $line;

for my $staString (@staStrings) {

    print "\n$staString\n";

    for $plot_type (@plot_types) {



		    $dir_data = join( '/', $share_data, $plot_type_dirs{ $plot_type } );
		    my $dbfile = join( '/', $dir_data, '.dbfile' );
		    $dbfile =~ s/^\///;
		    $dbfile =~ s/\/\./\./;
		    $dbfile =~ s/\//_/g;
		    my $command = join( ' ', '/usr/bin/find', $dir_data, '-name', join( '', $staString, '*'), '| head -1'  );
            #print $command, "\n";
            $line = `$command`;
            chomp $line;
            my @x = split(/\//, $line);
		    $command = join( ' ', '/usr/bin/find', $dir_data, '-name', join( '', $staString, '*'), '| tail -1'  );
            #print $command, "\n";
            $line = `$command`;
            chomp $line;
            my @y = split(/\//, $line);
            printf "%-30s from %-40s to %-40s\n", $x[5], $x[-1], $y[-1];
		

    }
}


# Function to set up directories
sub setDataDir {

	my @shares_data = qw( /mnt/earthworm3/monitoring_data /mnt/mvofls2/Seismic_Data/monitoring_data );

	my %plot_type_dirs = ( 	'heli' => 'helicorder_plots',
				'heliwide' => 'helicorder_plots_wide',
				'sgram' => 'sgram',
				'pan' => 'pan_plots',
				'helimulti' => 'helicorder_plots_multi',
				'heliscan' => 'helicorder_plots_scanned',
				'helidisp' => 'helicorder_plots_displacement',
                'vlp' => 'vlp_plots' );

	return( \@shares_data, \%plot_type_dirs );
}
