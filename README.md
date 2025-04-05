# webobs

Scripts for webobs.

## Description

Various scripts written for the webobs installation at MVO.

## Installing on *webobs* server.

* CGI scripts go in */mvo/webobs/WWW/cgi-bin*.
* HTML scripts go in */mvo/webobs/WWW/html*.
* */home/webobs/src/seismic_plot_viewer*.

## crontab.txt

This contains the crontab entries to be run by user *wwsuser* on *winston1*.

## Directories

| Directory       | Function |
| -------------| -------------------|
| *cgi-bin* | Various cgi scripts.|
| *html* | Various standalone html pages to view seismic data.|
| *seismic_plot_viewer* | Interactive viewer for helicorder plots and lots, lots more.|
| *webobs-misc* | Miscellaneous stuff.|
| *wws_heli_viewer* | Dynamic helicorder creation tool.|

## cgi-bin

### Scripts

| File       | Function |
| -------------| -------------------|
| *mvo_alarms_last.cgi* | List recent alarms created by seismic system.|
| *wws_rsam_viewer.cgi* | View RSAM data.|

## seismic_plot_viewer

### Description

seismic_plot_viewer is an interactive CGI script to view by date a variety of images of seismic, and other, data in webobs. It is viewable using the *Seismology | Helicorders etc* tab.

These are the different kinds of plots that it serves up.
* Helicorders
* Short-period helicorders
* Wide short-period helicorders
* Multi-station helicorder montages
* Spectrograms
* Pan plots
* Scanned paper helicorders
* Displacement helicorders
* VLP waveforms
* Strain waveforms
* Strain pan plots
* Infrasound helicorders

### Modes

The script should run in two modes, "normal" and "mobile". The second is a stripped-down version for use on mobile phones.

This feature is not currently working and a hacked version of the main script, *seismic_plot_viewer_mob.cgi*, can be used instead.

### Data sources

The main script, *seismic_plot_viwer.pl*, searches for plots in these directories in order.
1. */mnt/earthworm3/monitoring_data*
2. */mnt/mvofls2/Seismic_Data/monitoring_data*

To speed up the search, *mlocate* databases for the above directories are created once a day by *update_mlocate.pl*. These are stored in the *\*.dbfile* files.

These static text files are used by the script.
* *about.txt*
* *bands.txt*
* *networks.txt*
* *stations.txt* 

These text files summarize what plots are available and are updated once a day.
* *holdings.txt*
* *holdings_detailed.txt*

### Scripts

| File       | Function |
| -------------| -------------------|
| *check_holdings.pl* | Script to update *holdings_detailed.txt*. |
| *check_holdings.sh* | Script to run *check_holdings.pl* and update *holdings.txt*. Runs once a day as a cronjob.|
| *find_img.pl* | Standalone Perl script to find plot files (only used in debugging).|
| *seismic_plot_viewer.cgi* | Main script.|
| *seismic_plot_viewer_mob.cgi* | Temporary version of script for use on mobile devices.|
| *update_mlocate.pl* | Script to update mlocate databases. Runs once a day as a cronjob.|

## webobs-misc

### Scripts

| File       | Function |
| -------------| -------------------|
| *copy_heli.sh* | Script to copy today's helicorder plots to *notWebobs*. Runs as a cronjob every minute. Currently disabled.|

## Author

Roderick Stewart, Dormant Services Ltd

rod@dormant.org

https://services.dormant.org/

## Version History

* 1.0-dev
    * Working version

## License

This project is the property of Montserrat Volcano Observatory.
