#!/usr/bin/perl

##################################################################
#	Scott Thompson - scottt@interchange.ubc.ca
##################################################################
### Opening Stuff. Modules and all that. nothin' much interesting.

use lib '/usr/local/apache/tnmc/';
use tnmc;
require 'movies/MOVIES.pl';

	#############
	### Main logic
	
	#my (%movie);
	%movie=();
	&db_connect();

	$sql = "SELECT NOW()";
	$sth = $dbh_tnmc->prepare($sql);
	$sth->execute();
	($timestamp) = $sth->fetchrow_array();
	$sth->finish;
	
	#
	# This script should get run every tuesday evening at about 10 pm 
	# (or just after we watch the movie).
	#

	#
	# (1) Set this week's movie to "seen"
	#

	$movieID = &get_general_config('movie_current_movie');

	if ($movieID)
	{
		&get_movie($movieID, \%movie);
		$movie{'statusSeen'} = "1";
		$movie{'date'} = $timestamp;
		&set_movie(%movie);
		&set_general_config('movie_current_movie', 0);
 	}

	#
	# (2) Set last week's new releases to just "showing"
	#

	$sql = "UPDATE Movies SET statusNew = '0' WHERE statusShowing = '1'";
	$sth = $dbh_tnmc->prepare($sql);
	$sth->execute();
	$sth->finish;

	#
	# (3) Advance the MovieAttendance Dates.
	#

	# $sql = "SELECT DATE_ADD(NOW(), INTERVAL ((9 - DATE_FORMAT(NOW(), 'w') ) % 7) DAY)";
	# $sth = $dbh_tnmc->prepare($sql);
	# $sth->execute();
	# ($this_tuesday) = $sth->fetchrow_array();
	
	$sql = "SELECT DATE_ADD(NOW(), INTERVAL '21' DAY)";
	$sth = $dbh_tnmc->prepare($sql);
	$sth->execute();
	($far_tuesday) = $sth->fetchrow_array();
	
	$sql = "SELECT DATE_FORMAT(NOW(), '%Y%m%d') DATE_FORMAT('$far_tuesday', '%Y%m%d')";
	$sth = $dbh_tnmc->prepare($sql);
	$sth->execute();
	($oldMovieDate, $newMovieDate) = $sth->fetchrow_array();
	
	$sql = "ALTER TABLE MovieAttendance ADD movie$newMovieDate char(20), DROP COLUMN movie$oldMovieDate";
	$sth = $dbh_tnmc->prepare($sql);
	$sth->execute();
	
	# $sql = "UPDATE MovieAttendance SET movie$newMovieDate = 'Default'";
	# $sth = $dbh_tnmc->prepare($sql);
	# $sth->execute();


	# the end.

	&db_disconnect();

