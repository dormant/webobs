# webobs

Scripts for webobs.

## Description

Various scripts written for the webobs installation at MVO.

## Getting Started

### Dependencies

* Webobs

### Installing on *webobs* server.

* CGI scripts go in */mvo/webobs/WWW/cgi-bin*.
* HTML scripts go in */mvo/webobs/WWW/html*.
* */home/wwebobs/src/seismic_plot_viewer*.

## Directories

| Directory       | Function |
| -------------| -------------------|
| *html* | Various standalone html pages to view seismic data.|
| *seismic_plot_viewer* | Interactive viewer for helicorder plots and lots, lots more.|
| *webobs-misc* | Miscellaneous stuff.|
| *wws_heli_viewer* | Dynamic helicorder creation tool.|

## seismic_plot_viewer

| File       | Function |
| -------------| -------------------|
| *about.txt* | Help text for viewer.. |
| *bands.txt*   | Pseudo-channel codes used by the different plot types. |
| *check_holdings.pl* | Perl script to update detailed list of plot files in *holdings_detailed.txt*. |
| *check_holdings.sh* | Shell script to run check_holdings.pl and update list of holdings in *holdings.txt*.|
| *crontab.txt* | Entries for crontab to run update scripts.|
| *find_img.pl* | Standalone Perl script to find plot files.|
| *getStations.sh* | WTF! |
| *holdings.txt* | List of plot types, stations and channels with first and last dates present in database. Updated daily by *check_holdings.sh* cronjob. |
| *holdings_detailed.txt* | Detailed list of every plot file in database. Updated daily by *check_holdings.sh* cronjob.|
| *\*.dbfile* | Database indexes created by *update_mlocate.pl*. |
| *networks.txt* | List of pseudo-networks used to group plot files.|
| *seismic_monthly_plot_viewer.cgi* | WTF?.|
| *seismic_plot_viewer.cgi* | Main perl script.|
| *stations.txt* | List of all station codes.|
| *update_mlocate.pl* | Script to update mlocate databases. Runs once a day as a cronjob.|

## Author

Roderick Stewart, Dormant Services Ltd

rod@dormant.org

https://services.dormant.org/

## Version History

* 1.0-dev
    * Working version

## License

This project is licensed to Montserrat Volcano Observatory.
