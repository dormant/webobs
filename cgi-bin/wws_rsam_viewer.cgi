#!/usr/bin/env perl
#
# Perl script to serve a web page to create customisable 
# RSAM plots from a Winston Wave Server in a convenient form
#
# Paddy Smith, MVO, 11-Jul-2014
# adapted from wws_heli_viewer.cgi 
# 
#
use strict;
use CGI;
use Data::Dumper; # 2011-09-29
use LWP::Simple qw(!head);
use Time::Local;

# 2011-09-29 include WebObs modules
use readFile;
use readCfgFile;
use readConf;
use readGraph;
use fonctions;

# Set default values
		
# piton WWS 
#$server_url='http://172.20.0.163:16022/heli?';

# New winston1 WWS
my $server_url='http://172.17.102.60:16022/rsam';

my %stations = ( 
#    'ANWB' => { 'amp' => 1250, 'clip' => 12000, 'net' => 'CU', 'active' => 1 },
    'MBBY' => { 'plot_max' => 1000, 'plot_min' => 0 },
    'MBFL' => { 'plot_max' => 5000,  'plot_min' => 0, 'band' => 'HHZ', 'net' => 'MV_00'  },
    'MBFR' => { 'plot_max' => 1000, 'plot_min' => 0 },
    'MBGB' => { 'plot_max' => 5000, 'plot_min' => 0, 'band' => 'HHZ', 'net' => 'MV_00' },
    'MBGH' => { 'plot_max' => 5000, 'plot_min' => 0, 'band' => 'HHZ', 'net' => 'MV_00' },
    'MBHA' => { 'plot_max' => 1000, 'plot_min' => 0, 'band' => 'SHZ'}, # PJS 18-Dec-2013
#    'MBHA' => { 'amp' => 1000, 'clip' => 10000 },
    'MBLG' => { 'plot_max' => 5000, 'plot_min' => 0, 'band' => 'HHZ', 'net' => 'MV_00' },
    'MBLY' => { 'plot_max' => 5000, 'plot_min' => 0, 'band' => 'HHZ', 'net' => 'MV_00' },
    'MBRV' => { 'plot_max' => 1000,  'plot_min' => 0  },
    'MBRY' => { 'plot_max' => 1000, 'plot_min' => 0 },
    'MBWH' => { 'plot_max' => 1000, 'plot_min' => 0  },
    'MBWW' => { 'plot_max' => 1000, 'plot_min' => 0, 'band' => 'HHZ'},  # MBWW has a band that does not correspond to the norm
    );

my %stationsr = (
    'ABD' => { 'plot_max' => 1000, 'plot_min' => 0, 'band' => 'HHZ', 'net' => 'WI', 'long_name' => 'Anse Bertrand, Guadeloupe' },
    'ANWB' => { 'plot_max' => 1000,  'plot_min' => 0, 'long_name' => 'Willy Bob, Barbuda' },
    'GRGR' => { 'plot_max' => 1000, 'plot_min' => 0, 'long_name' => 'Grenville, Grenada'},
    'GRHS' => { 'plot_max' => 1000, 'plot_min' => 0, 'band' => 'HHZ', 'net' => 'TR',  'long_name' => 'Sauteurs, Grenada'},
    'GRSS' => { 'plot_max' => 1000, 'plot_min' => 0, 'band' => 'HHZ', 'net' => 'TR', 'long_name' => 'Sisters, The Grenadines'},
    'GRSS' => { 'plot_max' => 1000, 'plot_min' => 0, 'band' => 'EHZ', 'net' => 'TR', 'long_name' => 'Sisters (Short Period), The Grenadines'},
    'GRW' => { 'plot_max' => 1000, 'plot_min' => 0, 'band' => 'HHZ', 'net' => 'TR', 'long_name' => 'Mount Saint Catherine, Grenada'},
    'GCMP' => { 'plot_max' => 1000, 'plot_min' => 0, 'band' => 'HHZ', 'net' => 'TR', 'long_name' => 'Mt. Pleasant, Carriacou'},
    'SVB' => { 'plot_max' => 1000, 'plot_min' => 0, 'band' => 'HHZ', 'net' => 'TR', 'long_name' => 'Belmont, St Vincent'},
);

my %spiders = (
	'MSCP' => { 'plot_max' => 1000, 'plot_min' => 0 },
	'MSDE' => { 'plot_max' => 1000, 'plot_min' => 0 },
	'MSGL' => { 'plot_max' => 1000, 'plot_min' => 0 },
	'MSGE' => { 'plot_max' => 1000, 'plot_min' => 0 },
	'MSS1' => { 'plot_max' => 1000, 'plot_min' => 0 },
	'MSUH' => { 'plot_max' => 1000, 'plot_min' => 0, 'band' => 'SHZ'},
	);


my $sta_default = 'MBGH';
my $web_start_page = '/cgi-bin/wws_rsam_viewer.cgi';

# Things for web page
my $network = 'MVO';
my $title = join( ': ', $network, 'WWS RSAM plots' );
my $spaces = "&nbsp;";
my $markerl='<FONT COLOR="#FF0000">*</FONT>';
my $markerr='<FONT COLOR="#FF0000">*</FONT>';
my $markersp = '&nbsp;';
my $space1 = "&nbsp;&nbsp;";
my $space2 = "&nbsp;&nbsp;&nbsp;&nbsp;";
my $space4 = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";

# New thing
my $q = CGI->new;

if (param('proxyImage') == 1)
{
    proxyImage();
    exit;
}

my $css_for_timepicker = <<EOCSS;
/* css for timepicker */
.ui-timepicker-div .ui-widget-header{ margin-bottom: 8px; }
.ui-timepicker-div dl{ text-align: left; }
.ui-timepicker-div dl dt{ height: 25px; }
.ui-timepicker-div dl dd{ margin: -25px 0 10px 65px; }
.ui-timepicker-div td { font-size: 90%; }
EOCSS

# Print web page
print $q->header;
print $q->start_html( -title => " ".$title, 
                        -head => 
                                [
                                    $q->meta( {-http_equiv=>'REFRESH',-content=>'60'}),
                                    $q->Link({-rel=>'shortcut icon', -href=>'/heli/favicon.ico'}),
                                ],
                        -style => 
                                [
                                    { 'src' => "/JavaScripts/defaultsr.css" },
                                    { 'src'=>"/JavaScripts/jquery-ui-1.8.14.custom/css/ui-lightness/jquery-ui-1.8.14.custom.css" },
                                    { 'code' => $css_for_timepicker },
                                ],
                        -script => 
                                [ 
                                    { -language => 'javascript', -src => "/JavaScripts/jquery.js" },
                                    { -language => 'javascript', -src => "/JavaScripts/jquery-ui-1.8.14.custom/js/jquery-ui-1.8.14.custom.min.js" },
                                    { -language => 'javascript', -src => "/JavaScripts/jquery-ui-1.8.14.custom/development-bundle/ui/jquery-ui-timepicker-addon.js" },
                                    { -language => 'javascript', -src => "/JavaScripts/defaultsr.js" },
                                    { -language => 'javascript', -code => getJavascript() },
                                ],
                    );

# 2011-09-29 load WebObs config info
my $res = defined $q->url_param('reseau') ? $q->url_param('reseau') : 'MMB';
my %WEBOBS = readConfFile;
my @station_dirs = qx(/bin/ls $WEBOBS{RACINE_DATA_STATIONS});
my $codeRes=substr($res,length($res)-3,3);
my @subStationList=grep(/^$codeRes/,@station_dirs);

my $resp= defined $q->url_param('reseau') ? $q->url_param('reseau') : 'UMS';
my @spider_dirs = qx(/bin/ls $WEBOBS{RACINE_DATA_STATIONS});
my $codeResp=substr($resp,length($resp)-3,3);
my @subSpiderList=grep(/^$codeResp/,@spider_dirs);

#print Dumper( @subStationList );

my $today = qx(/bin/date +\%Y-\%m-\%d);
chomp($today);
my @stations = ();
foreach my $nm (@subStationList)
{
    $nm =~ s/\s+$//;
    
    my %config = readConfStation($nm);
    
    my $alias = $config{'ALIAS'};
    
    $stations{$alias}->{'name'} = $nm;
    $stations{$alias}->{'long_name'} = $config{'NOM'};
    
    $stations{$alias}->{'active'} = 1;
    if (($config{END_DATE} ne "NA" && $config{END_DATE} lt $today) || ($config{INSTALL_DATE} ne "NA" && $config{INSTALL_DATE} gt $today)) 
    {
	    $stations{$alias}->{'active'} = 0;
	    #$stations{$alias}->{'active'} = 0 unless exists $stations{$alias}->{'active'};
        next;
    }
    
    $stations{$alias}->{'band'} = 'BHZ' unless exists $stations{$alias}->{'band'};
    $stations{$alias}->{'net'} = 'MV' unless exists $stations{$alias}->{'net'};
    
    if ($config{'TYPE'} =~ /vertical/i && $config{'TYPE'} =~ /short/) #Vertical short-period
    {
        $stations{$alias}->{'band'} = 'SHZ' ; #unless exists $stations{$alias}->{'band'};
    }
    
    my $plot_nm = $alias.'_'.$stations{$alias}->{'band'}.'_'.$stations{$alias}->{'net'};
    $stations{$alias}->{'plot_nm'} = $plot_nm;
}

my @spiders = ();
foreach my $nm (@subSpiderList)
{
    $nm =~ s/\s+$//;
    
    my %config = readConfStation($nm);
    
    my $alias = $config{'ALIAS'};
	#print "$alias\n";
    
    $spiders{$alias}->{'name'} = $nm;
    $spiders{$alias}->{'long_name'} = $config{'NOM'};
    
    $spiders{$alias}->{'active'} = 1;
    if (($config{END_DATE} ne "NA" && $config{END_DATE} lt $today) || ($config{INSTALL_DATE} ne "NA" && $config{INSTALL_DATE} gt $today)) 
    {
	    $spiders{$alias}->{'active'} = 0;
	    #$stations{$alias}->{'active'} = 0 unless exists $stations{$alias}->{'active'};
        next;
    }
    
    $spiders{$alias}->{'band'} = 'SHZ' unless exists $spiders{$alias}->{'band'};
    $spiders{$alias}->{'net'} = 'MV' unless exists $spiders{$alias}->{'net'};
    
    #if ($config{'TYPE'} =~ /vertical/i && $config{'TYPE'} =~ /short/) #Vertical short-period
    #{
    #    $spiders{$alias}->{'band'} = 'SHZ' ; #unless exists $stations{$alias}->{'band'};
    #}
    
    my $plot_nms = $alias.'_'.$spiders{$alias}->{'band'}.'_'.$spiders{$alias}->{'net'};
    $spiders{$alias}->{'plot_nm'} = $plot_nms;
}

my @stationsr = ();
##my @stationsr = %stations_reg;
foreach my $nm (sort keys %stationsr)
{
    $nm =~ s/\s+$//;
#	print "$nm\n"; 
#    my %config = readConfStation($nm);
#    my $alias = $config{'ALIAS'};

	my $alias =  $nm;

    $stationsr{$alias}->{'name'} = $nm;
    $stationsr{$alias}->{'long_name'} = 'NAME' unless exists $stationsr{$alias}->{'long_name'};
#    
    $stationsr{$alias}->{'active'} = 1;

    $stationsr{$alias}->{'band'} = 'BHZ' unless exists $stationsr{$alias}->{'band'};
    $stationsr{$alias}->{'net'} = 'CU' unless exists $stationsr{$alias}->{'net'};
#    
    my $plot_nms = $alias.'_'.$stationsr{$alias}->{'band'}.'_'.$stationsr{$alias}->{'net'};
    $stationsr{$alias}->{'plot_nm'} = $plot_nms;
    #print "$plot_nms\n";
}

#print Dumper(%stations);

# setup data structures for combo box
my @stacodes = ();
my %stat_drop_down = ();
foreach my $alias (sort keys %stations)
{
    next unless $stations{$alias}->{'active'};
    
    push @stacodes, $alias;
    $stat_drop_down{$alias} = $stations{$alias}->{'long_name'};
}
# append spiders...
foreach my $alias (sort keys %spiders)
{
    next unless $spiders{$alias}->{'active'};
    
    push @stacodes, $alias;
    $stat_drop_down{$alias} = $spiders{$alias}->{'long_name'};
}
# append regional stations
foreach my $alias (sort keys %stationsr)
{
    push @stacodes, $alias;
    $stat_drop_down{$alias} = $stationsr{$alias}->{'long_name'};
}


#print Dumper(@stacodes);

# parameters for URL of heli
my $station_to_plot = $sta_default;
my $url_to_plot;
my $width = 800;
my $height = 400;
#my $nmins = 30;
my $ndays = 1;
my $t_end = 'now';
my $despike = 0;
my $dsp;
my $detrend = 0;
my $runmed = 0;
my $rmp;
my $plot_max;
my $plot_min;
my $last_url;

$station_to_plot = $q->param('stat_f')  if defined $q->param('stat_f');
#$nmins           = $q->param('nmins_f') if defined $q->param('nmins_f');
$ndays            = $q->param('ndays_f')  if defined $q->param('ndays_f');
$plot_max         = defined $q->param('plot_max_f') ? $q->param('plot_max_f') : $stations{$station_to_plot}->{'plot_max'};
$plot_min         = defined $q->param('plot_min_f') ? $q->param('plot_min_f') : $stations{$station_to_plot}->{'plot_min'};
$width           = $q->param('width_f') if defined $q->param('width_f');
$height          = $q->param('height_f')  if defined $q->param('height_f');
$despike         = $q->param('despike') if defined $q->param('despike');
$dsp		 = $q->param('dsp_f') if defined $q->param('dsp_f');
$detrend         = $q->param('detrend') if defined $q->param('detrend');
$runmed          = $q->param('runmed') if defined $q->param('runmed');
$rmp		 = $q->param('rmp_f') if defined $q->param('rmp_f');
$t_end           = $q->param('t_end_f') if defined $q->param('t_end_f');

$t_end =~ s/\s+//g;


# get the last URL for station links
$last_url = $ENV{'REQUEST_URI'};

print "<TT>\n";
print "<BR>\n";
print "<B>MVO: </B>", $spaces, "\n";

# print out the station selector menu
foreach my $station ( sort keys %stations )
{
    next unless $stations{$station}->{'active'};
    
    my $s_plot_max = $stations{$station}->{'plot_max'};
    my $s_plot_min = $stations{$station}->{'plot_min'};
    
    my $link = $last_url;	
    $link =~ s/stat_f=(.*?)\&/stat_f=$station\&/;	 	# change station
    $link =~ s/plot_max_f=(.*?)\&/plot_max_f=$s_plot_max\&/;	# change plot_max
    $link =~ s/plot_min_f=(.*?)\&/plot_min_f=$s_plot_min\&/;    # change plot_min
    
    if( $station eq $station_to_plot) {
        print $markerl;
    } else {
        print $markersp;
    }
    print $q->a({href=>$link},$station);
    if( $station eq $station_to_plot) {
        print $markerr, $spaces, $spaces;
    } else {
        print $markersp, $spaces, $spaces;
    }
    print "\n";
}

print "</TT>\n";
print "<BR>\n";
print "<BR>\n";

#### SPIDERS! PJS, 20-Jun-2014
print "<TT>\n";
print "<B>Spi: </B>", $spaces, "\n";

# print out the spider selector menu
foreach my $spider ( sort keys %spiders )
{
	next unless $spiders{$spider}->{'active'};
    
    my $s_plot_max = $spiders{$spider}->{'plot_max'};
    my $s_plot_min = $spiders{$spider}->{'plot_min'};
    
    my $link = $last_url;	
    $link =~ s/stat_f=(.*?)\&/stat_f=$spider\&/;		# change station
    $link =~ s/plot_max_f=(.*?)\&/plot_max_f=$s_plot_max\&/;	# change amp
    $link =~ s/plot_min_f=(.*?)\&/plot_min_f=$s_plot_min\&/;	# change clip
    
    if( $spider eq $station_to_plot) {
        print $markerl;
    } else {
        print $markersp;
    }
    print $q->a({href=>$link},$spider);
    if( $spider eq $station_to_plot) {
        print $markerr, $spaces, $spaces;
    } else {
        print $markersp, $spaces, $spaces;
    }
    print "\n";
}
#### Regional stations, PJS, 14-Mar-2018
print "<TT>\n";
print "<B>Sta: </B>", $spaces, "\n";

# print out the spider selector menu
foreach my $stationr ( sort keys %stationsr )
{
	next unless $stationsr{$stationr}->{'active'};
    
    my $s_plot_max = $stationsr{$stationr}->{'plot_max'};
    my $s_plot_min = $stationsr{$stationr}->{'plot_min'};
    
    my $link = $last_url;	
    $link =~ s/stat_f=(.*?)\&/stat_f=$stationr\&/;		# change station
    $link =~ s/plot_max_f=(.*?)\&/plot_max_f=$s_plot_max\&/;	# change amp
    $link =~ s/plot_min_f=(.*?)\&/plot_min_f=$s_plot_min\&/;	# change clip
    
    if( $stationr eq $station_to_plot) {
        print $markerl;
    } else {
        print $markersp;
    }
    print $q->a({href=>$link},$stationr);
    if( $stationr eq $station_to_plot) {
        print $markerr, $spaces, $spaces;
    } else {
        print $markersp, $spaces, $spaces;
    }
    print "\n";
}
print "</TT>\n";
print "<BR>\n";
print "<BR>\n";

# Print the form
print $q->start_form( -action => $web_start_page, -method => 'get' ), "\n";
# Station drop-down
#print $q->popup_menu( -name => 'stat_f', -values => \@stacodes, -labels => \%stations, -default=>@stacodes[4] );
print $q->popup_menu( -name => 'stat_f', -values => \@stacodes, -labels => \%stat_drop_down, -default=>@stacodes[4] );
print $space1;
# Days to plot
print "Days: ", $space1;
print $q->textfield(
        -name      => 'ndays_f',
        -default   => $ndays,
        -size      => 2,
        -maxlength => 3,
    );
print $space1;
## width of line
#print "Line width [mins]: ", $space1;
#print $q->textfield(
#        -name      => 'nmins_f',
#        -default     => $nmins,
#        -size      => 2,
#        -maxlength => 3,
#    );
#print $space1;
# max amplitude
print "Max. Amp [counts]: ", $space1;
print $q->textfield(
        -name      => 'plot_max_f',
        -default     => $plot_max,
        -size      => 4,
        -maxlength => 6,
    );
print $space1;
# clip
print "Min Amp. [counts]: ", $space1;
print $q->textfield(
        -name      => 'plot_min_f',
        -default    => $plot_min,
        -size      => 5,
        -maxlength => 6,
    );
print $space1;
# image width
print "Width [pixels]: ", $space1;
print $q->textfield(
        -name      => 'width_f',
        -default    => $width,
        -size      => 4,
        -maxlength => 4,
    );
print $space1;
# image height
print "Height [pixels]: ", $space1;
print $q->textfield(
        -name      => 'height_f',
	-default   => $height,
        -size      => 3,
        -maxlength => 4,
    );
# new line  - looks tidier on smaller screen resolutions
print "<BR>\n";
# optional end time
print "End time [YYYYMMDDHHMM UTC]: ", $space1;
print $q->textfield(
        -name      => 't_end_f',
        #-default    => 'now',
        #-size      => 3,
        #-maxlength => 12,
        -id        => 't_end_f',
    );
print <<"EOJ";
        <SCRIPT>
        \$(function()
        {
        \$("#t_end_f").datetimepicker({
                dateFormat: 'yymmdd',
                timeFormat: 'hhmm',
                showSecond: false,
	            ampm: false,
                });
        });
        </SCRIPT>
EOJ
print $space1;
# Despike checkbox 
print $q->checkbox(
        -name    => 'despike',
        -checked => 1,
        -value   => '1',
        -label   => 'Despike',
    );
print $space1;
# Despike period 
print "Period: ", $space1;
print $q->textfield(
        -name      => 'dsp_f',
        -default    => 0,
        -size      => 4,
        -maxlength => 4,
    );
print $space1;
# Detrend checkbox
print $q->checkbox(
        -name    => 'detrend',
        -checked => 1,
        -value   => '1',
        -label   => 'Detrend',
    );
print $space1;
# Running median checkbox
print $q->checkbox(
        -name    => 'runmed',
        -checked => 1,
        -value   => '1',
        -label   => 'Running median',
    );
print $space1;
# Running median period 
print "Period: ", $space1;
print $q->textfield(
        -name      => 'rmp_f',
        -default    => 0,
        -size      => 4,
        -maxlength => 4,
    );
print $space1;
# submit button
print $q->submit( -name => 'submit' );
# end the form
print $q->end_form, "\n";

# display refresh message
print "This page refreshes automatically every minute.<BR>\n";

#print Dumper($station_to_plot);
#print Dumper($stations{$station_to_plot});
#print Dumper($spiders{$station_to_plot});

# combine list of stations + spiders + regional_stations:
my %stat_spi_reg = (%stations, %spiders, %stationsr); 

# create URL of image to pass to WWS webserver		
#$url_to_plot = join ( '', $server_url, 'code=', $stations{$station_to_plot}->{'plot_nm'}, '&w=', $width, '&h=', $height, '&tc=', $nmins, '&t1=-', $nhrs, '&t2=', $t_end, '&tz=America/Montserrat&lb=', $show_label, '&sc=', $show_clip, '&br=', $amp, '&cv=', $clip_value, ''); 
$url_to_plot = join ( '', $q->url, '?proxyImage=1&','code=', $stat_spi_reg{$station_to_plot}->{'plot_nm'}, '&w=', $width, '&h=', $height, '&t1=-', $ndays, '&t2=', $t_end, '&tz=UTC&ds=', $despike, '&dsp=', $dsp,'&dt=', $detrend, '&rm=', $runmed , '&rmp=', $rmp, '&max=', $plot_max, '&min=', $plot_min, ''); 
		
# add image
		print $q->img({-src=>"$url_to_plot"});	
		print "<BR>\n";
# display url of image - may be useful...
print "Image url: ".a({-href=>$url_to_plot}, $url_to_plot)."\n";	
# end web page
print $q->end_html;



exit;  # end main

#################################################
# since the EarthWorm server cannot be reached from outside
# this function provides an image proxy
sub proxyImage()
{
    
    my $url = $q->url();
    my $query = $q->self_url();  #url(-query=>1);
    
    $query =~ s/\;/\&/g;
    $query =~ s/proxyImage=1&//;
    $query =~ s/$url/$server_url/;
    $query =~ s/\%2F/\//g;
    
    # for debugging you can uncomment below and hit with URL like
    # http://webobs.mvo.ms/cgi-bin/wws_heli_viewer.cgi?proxyImage=1&code=MBLG_BHZ_MV&w=1568&h=605&tc=30&t1=-24&t2=now&tz=America/Montserrat&lb=1&sc=1&br=6000&cv=40000
    if (1 == 2)
    {
        print $q->header();
        print "url: $url<br>\n";
        print "query: $query<br>\n";
        exit;
    }
    
    print $q->header('image/png');
    
    getprint($query);
    
    exit;
    
}

#################################################
sub getJavascript()
{
    my $js = <<"EOJ";
    
\$(document).ready(function() {
    var myRegExp = /width_f=/;
    var href = window.location.href;
    var matchPos = href.search(myRegExp);

    if(matchPos == -1)
    {
        var winW = 630, winH = 460;
        if (document.body && document.body.offsetWidth) {
         winW = document.body.offsetWidth;
         winH = document.body.offsetHeight;
        }
        if (document.compatMode=='CSS1Compat' &&
            document.documentElement &&
            document.documentElement.offsetWidth ) {
         winW = document.documentElement.offsetWidth;
         winH = document.documentElement.offsetHeight;
        }
        if (window.innerWidth && window.innerHeight) {
         winW = window.innerWidth;
         winH = window.innerHeight;
        }
        //var fw = parent.document.getElementById("bas").width;
        //var fh = parent.document.getElementById("bas").height;
        var w = Math.round(0.98 * winW);
        var h = Math.round(0.825 * winH);
        if (w < 640) 
        {
            w = 640;
            h = 480;
        }
        var suffix = "&stat_f=$sta_default&despike=0&detrend=0&runmed=0";
        if (window.location.search.length <= 1)
        {
            //window.location.search = "width_f=" + w + "&height_f=" + h + suffix;
            window.location.replace(href + "?width_f=" + w + "&height_f=" + h + suffix);
        }
        else
        {   
            window.location.replace(href + "&width_f=" + w + "&height_f=" + h + suffix);
        }
    }
});

EOJ

    return $js;
}

