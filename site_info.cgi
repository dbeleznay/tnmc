#!/usr/bin/perl

##################################################################
#	Jeff Steinbok - steinbok@interchange.ubc.ca
##################################################################
### Opening Stuff. Modules and all that. nothin' much interesting.

use DBI;
use CGI;

use lib '/usr/local/apache/tnmc/';
use tnmc;


	#############
	### Main logic

	&db_connect();

	&header();

	&show_heading("site info");

	$cgih = new CGI;

	print qq 
	{	<TABLE>

		<TR>
		<TD VALIGN=TOP><B>Hosting:</B></TD>
		<TD>tnmc.webct.com is hosted by Alex. <br>
			It was previously on <a href="http://steinbok.lvwr.com">steinbok.lvwr.com</a> <BR>
		</TR>

		<TR>
		<TD VALIGN=TOP><B>Site & DB Design:</B></TD>
		<TD>Scott</TD>
		</TR>

		<TR>
		<TD VALIGN=TOP><B>Implementation:</B></TD>
		<TD>Jeff & Scott</TD>
		</TR>

		<TR>
		<TD VALIGN=TOP><B>Contributed Code:</B></TD>
		<TD>Alex</TD>
		</TR>

		<TR>
		<TD VALIGN=TOP><B>Browsers Supported:</B></TD>
		<TD>	
			Netscape 4+ on a pc<br>
			Netscape 4+ on unix<br>
			Macs are unreliable at best<br>
			Explorer might work<br>
			....or it might not.<br>
			</TD>
		</TR>

		<TR>
		<TD VALIGN=TOP><B>Techie Stuff:</B></TD>
		<TD>	The site is written in perl, is served by an
			Apache web server, and interfaces with a mySQL
			database. The whole she-bang is running on a FreeBSD box.
			
		</TR>

		<TR>
		<TD VALIGN=TOP><B>Stats:</B></TD>
		<TD>
	};

	open (LINES, 'cat /usr/local/apache/logs/access_log.tnmc | grep -v gif | grep -v ^199.60.1.27 | grep -v ^24.113.3.42 | wc -l |');
	$proper_requests = <LINES>;
	close (LINES);

	open (LINES, 'cat /usr/local/apache/logs/access_log.tnmc | grep -v ^199.60.1.27 | grep -v ^24.113.3.42 | wc -l |');
	$total_files = <LINES>;
	close (LINES);

	open (LINES, 'cat /usr/local/apache/logs/access_log.tnmc | grep -v gif | wc -l |');
	$total_cgi = <LINES>;
	close (LINES);

	open (LINES, 'du -b /var/lib/mysql/tnmc |');
	$bytes_of_data = <LINES>;
	$bytes_of_data =~ s/\D//g;
	close (LINES);
	$bytes_of_data = 'an unknown number of ';

	open (LINES, 'cat /usr/local/apache/tnmc/* | wc -l |');
	$lines_of_code = <LINES>;
	close (LINES);

        @file_status = stat("/usr/local/apache/tnmc/tnmc.tar.gz");
        use POSIX qw(strftime);
        $flastmod = strftime "%b %e, %Y", gmtime $file_status[9];
        
	print qq{
			$lines_of_code lines of perl code<br>
			$bytes_of_data bytes of data stored<br>
                        $proper_requests cgi requests<br>
			$total_files files served<br>
			</TD>
		</TR>

 	
		<TR>
		<TD valign="top" nowrap><B><a href="tnmc.tar.gz">Download Source Code</a></b><br>
			(as of $flastmod)<br>
		</TD>
		<TD>
			<b>TNMC<i>Online</i> is open source! :)</b>
			<p>
			If you want to use the code, please send
			an email to scottt @ interchange.ubc.ca


			<pre>
Copyright (C) 1999-2000  Scott Thompson, Jeff Steinbok and the rest of TNMC

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
<a href="http://www.fsf.org/copyleft/gpl.html#SEC3">GNU General Public License</a> for more details.
			</pre>
		</TD>
		</TR>

		</TABLE>
		<P>
	};	
	&footer();

	&db_disconnect();
